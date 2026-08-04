import requests
import os
import json
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
    "bounds": "3.8070597_43.6533542_3.9413208_43.5667088",
    "locationName": "Montpellier"
}


FILE_MEMORY = "seen.json"



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
# RECHERCHE CROUS
# ==============================

def get_accommodations():

    try:

        response = requests.post(
            API_URL,
            json=PARAMS,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )


        response.raise_for_status()


        data = response.json()


        logements = data["results"]["items"]


        print(
            f"API CROUS : {len(logements)} logements reçus"
        )


        for logement in logements:

            residence = logement.get(
                "residence",
                {}
            )

            print(
                "➡️",
                residence.get("label"),
                "|",
                residence.get("address")
            )


        return logements



    except Exception as e:

        print(
            "Erreur CROUS :",
            e
        )

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



        logement_id = logement.get(
            "id"
        )



        message += f"""
🏢 {nom}

📍 {adresse}

💰 Loyer : {prix} €

📐 Surface : {surface_text}

🔗 https://trouverunlogement.lescrous.fr/tools/47/search

🆔 ID logement : {logement_id}

--------------------
"""



    send_message(message)


    print(
        "🚨 Alerte Telegram envoyée !"
    )



else:


    print(
        "Aucun nouveau logement."
    )



save_seen(seen)



print(
    "✅ Surveillance terminée."
)
