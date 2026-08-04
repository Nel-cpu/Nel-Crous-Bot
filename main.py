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
    "pageSize": 24,

    # Zone Montpellier élargie
    "bounds": "3.8070597_43.6533542_3.9413208_43.5667088",

}


FILE_MEMORY = "seen.json"


# ==============================
# MEMOIRE DES LOGEMENTS
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
    url,
    json=params,
    timeout=20
)

        response.raise_for_status()

        data = response.json()

        return data["results"]["items"]


    except Exception as e:

        print("Erreur CROUS :", e)

        return []



# ==============================
# TRAITEMENT
# ==============================

seen = load_seen()

logements = get_accommodations()


print(
    f"{len(logements)} logement(s) trouvé(s)"
)


nouveaux = []


for logement in logements:


    logement_id = logement.get("id")


    if logement_id not in seen:

        nouveaux.append(logement)

        seen.append(logement_id)



# ==============================
# ALERTE TELEGRAM
# ==============================

if nouveaux:


    message = "🏠 Nouveau(x) logement(s) CROUS Montpellier !\n\n"


    for logement in nouveaux:


        nom = logement.get(
            "name",
            "Résidence inconnue"
        )

        message += f"""
🏢 {nom}

💰 Loyer : {logement.get('rent', 'NC')} €
📐 Surface : {logement.get('area', 'NC')} m²

🔗 https://trouverunlogement.lescrous.fr/accommodations/{logement_id}

--------------------
"""


    send_message(message)

    print("🚨 Alerte envoyée !")


else:

    print("Aucun nouveau logement.")



save_seen(seen)


print("✅ Surveillance terminée.")
