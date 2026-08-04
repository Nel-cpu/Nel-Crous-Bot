import requests
import os
import json
from math import radians, sin, cos, sqrt, atan2
from telegram import send_message


print("🤖 CROUS Alert Perso démarre !")


# ==============================
# CONFIGURATION
# ==============================

API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search/47"

PARAMS = {
    "maxPrice": 400,
    "minArea": 9,
    "page": 0,
    "pageSize": 100,
    "bounds": "3.8070597_43.6533542_3.9413208_43.5667088"
}


FILE_MEMORY = "seen.json"


# Coordonnées Faculté de Pharmacie Montpellier
FACULTE_LAT = 43.6319
FACULTE_LON = 3.8617



# ==============================
# MEMOIRE
# ==============================

def load_seen():

    if os.path.exists(FILE_MEMORY):

        with open(FILE_MEMORY, "r", encoding="utf-8") as f:
            return json.load(f)

    return []



def save_seen(data):

    with open(FILE_MEMORY, "w", encoding="utf-8") as f:
        json.dump(data, f)



# ==============================
# DISTANCE GPS
# ==============================

def distance_km(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)

    a = (
        sin(dlat/2)**2
        +
        cos(radians(lat1))
        *
        cos(radians(lat2))
        *
        sin(dlon/2)**2
    )

    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return round(R*c, 1)



# ==============================
# RECHERCHE CROUS
# ==============================

def get_accommodations():

    try:

        response = requests.post(
            API_URL,
            json=PARAMS,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )


        response.raise_for_status()

        data = response.json()


        logements = data["results"]["items"]


        # Filtre Montpellier
        logements_montpellier = []


        for logement in logements:


            residence = logement.get("residence", {})

            adresse = residence.get(
                "address",
                ""
            ).lower()


            entity = residence.get(
                "entity",
                {}
            ).get(
                "name",
                ""
            ).lower()



            if (
                "montpellier" in adresse
                or "hérault" in adresse
                or "herault" in adresse
                or "montpellier" in entity
            ):

                logements_montpellier.append(logement)



        return logements_montpellier



    except Exception as e:

        print("Erreur CROUS :", e)

        return []



# ==============================
# TRAITEMENT
# ==============================


seen = load_seen()


logements = get_accommodations()


print(
    f"{len(logements)} logement(s) Montpellier trouvé(s)"
)



nouveaux = []



for logement in logements:


    logement_id = logement.get("id")


    if logement_id not in seen:

        nouveaux.append(logement)

        seen.append(logement_id)



# ==============================
# TELEGRAM
# ==============================


if nouveaux:


    message = (
        "🏠 Nouveau(x) logement(s) CROUS Montpellier !\n\n"
    )



    for logement in nouveaux:


        residence = logement.get(
            "residence",
            {}
        )


        nom = residence.get(
            "label",
            "Résidence inconnue"
        )


        adresse = residence.get(
            "address",
            "Adresse inconnue"
        )


        surface = logement.get(
            "area",
            {}
        )


        surface_text = (
            f"{surface.get('min')} m²"
            if surface.get("min") == surface.get("max")
            else
            f"{surface.get('min')} - {surface.get('max')} m²"
        )



        loyer = logement.get(
            "occupationModes",
            []
        )


        if loyer:

            prix = loyer[0]["rent"]["min"]

            prix = round(prix / 100, 2)

        else:

            prix = "NC"



        location = residence.get(
            "location",
            {}
        )


        if location:


            distance = distance_km(
                FACULTE_LAT,
                FACULTE_LON,
                location.get("lat"),
                location.get("lon")
            )

        else:

            distance = "NC"



        logement_id = logement.get("id")



        message += f"""
🏢 {nom}

📍 {adresse}

💰 Loyer : {prix} €
📐 Surface : {surface_text}

🎓 Distance faculté : {distance} km

🔗 https://trouverunlogement.lescrous.fr/tools/47/accommodations/{logement_id}

--------------------
"""



    send_message(message)


    print("🚨 Alerte Telegram envoyée !")



else:


    print("Aucun nouveau logement.")




save_seen(seen)


print("✅ Surveillance terminée.")
