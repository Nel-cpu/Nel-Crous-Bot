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


# Faculté de Pharmacie Montpellier
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
# DISTANCE
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


        # On garde uniquement Montpellier
        logements_montpellier = []


        for logement in logements:

            residence = logement.get(
                "residence",
                {}
            )


            location = residence.get(
                "location",
                {}
            )


            lat = location.get("lat")
            lon = location.get("lon")


            if lat and lon:

                distance = distance_km(
                    FACULTE_LAT,
                    FACULTE_LON,
                    lat,
                    lon
                )


                # Montpellier et alentours
                if distance < 20:

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



        occupation = logement.get(
            "occupationModes",
            []
        )


        if occupation:

            prix = occupation[0]["rent"]["min"] / 100

        else:

            prix = "NC"



        location = residence.get(
            "location",
            {}
        )


        distance = distance_km(
            FACULTE_LAT,
            FACULTE_LON,
            location.get("lat"),
            location.get("lon")
        )



        logement_id = logement.get("id")



        message += f"""
🏢 {nom}

📍 {adresse}

💰 Loyer : {prix} €
📐 Surface : {surface_text}

🎓 Faculté pharmacie : {distance} km

🔗 https://trouverunlogement.lescrous.fr/search/47

🆔 Référence logement : {logement_id}

--------------------
"""



    send_message(message)

    print("🚨 Alerte Telegram envoyée !")



else:

    print("Aucun nouveau logement.")



save_seen(seen)


print("✅ Surveillance terminée.")
