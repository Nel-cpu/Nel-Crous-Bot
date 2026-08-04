import requests
import os
import json
from telegram import send_message


print("🤖 CROUS Alert Perso démarre !")


# ==============================
# CONFIGURATION
# ==============================

API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search/47"


BASE_PARAMS = {
    "maxPrice": 400,
    "minArea": 9,
    "pageSize": 100,
    "bounds": "3.8070597_43.6533542_3.9413208_43.5667088"
}


FILE_MEMORY = "seen.json"


VILLES_AUTORISEES = [
    "montpellier",
    "lattes",
    "castelnau-le-lez",
    "jacou",
    "le crès",
    "le cres",
    "saint-jean-de-védas",
    "saint jean de vedas",
    "juvignac",
    "grabels"
]



# ==============================
# MEMOIRE
# ==============================

def load_seen():

    if os.path.exists(FILE_MEMORY):

        try:

            with open(FILE_MEMORY, "r", encoding="utf-8") as f:
                return json.load(f)

        except:

            return []

    return []



def save_seen(data):

    with open(FILE_MEMORY, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )



# ==============================
# RECHERCHE CROUS
# ==============================

def get_accommodations():

    logements_total = []


    try:

        # Scan de plusieurs pages
        for page in range(10):

            params = BASE_PARAMS.copy()

            params["page"] = page


            response = requests.post(

                API_URL,

                json=params,

                timeout=20,

                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/json"
                }
            )


            response.raise_for_status()


            data = response.json()


            items = data.get(
                "results",
                {}
            ).get(
                "items",
                []
            )


            print(
                f"📄 Page {page} : {len(items)} logements"
            )


            if not items:

                break


            logements_total.extend(items)



        print(
            f"\n🏢 Total API CROUS : {len(logements_total)} logements"
        )



        logements_montpellier = []



        print(
            "\n🔎 Recherche Montpellier :"
        )



        for logement in logements_total:


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
                ""
            )


            print(
                "➡️",
                nom,
                "|",
                adresse
            )



            adresse_lower = adresse.lower()



            for ville in VILLES_AUTORISEES:

                if ville in adresse_lower:

                    logements_montpellier.append(logement)

                    break



        return logements_montpellier



    except Exception as e:

        print(
            "❌ Erreur CROUS :",
            e
        )

        return []



# ==============================
# TRAITEMENT
# ==============================

seen = load_seen()


logements = get_accommodations()



print(
    f"\n🏠 {len(logements)} logement(s) Montpellier trouvé(s)"
)



nouveaux = []



for logement in logements:


    logement_id = logement.get(
        "id"
    )


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



        occupation = logement.get(
            "occupationModes",
            []
        )



        if occupation:

            prix = occupation[0].get(
                "rent",
                {}
            ).get(
                "min",
                "NC"
            )

            if prix != "NC":

                prix = prix / 100


        else:

            prix = "NC"



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
