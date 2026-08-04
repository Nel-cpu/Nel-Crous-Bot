import os
import json
import asyncio
from math import radians, sin, cos, sqrt, atan2

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from telegram import send_message


print("🤖 CROUS Alert Perso Playwright démarre !")


# ==============================
# CONFIGURATION
# ==============================

URL = (
    "https://trouverunlogement.lescrous.fr/"
    "tools/47/search?"
    "maxPrice=400"
    "&minArea=9"
    "&bounds=3.8070597_43.6533542_3.9413208_43.5667088"
    "&locationName=Montpellier"
)


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

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        +
        cos(radians(lat1))
        *
        cos(radians(lat2))
        *
        sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return round(R * c, 1)



# ==============================
# SCRAPING CROUS
# ==============================

async def get_accommodations():


    logements = []


    async with async_playwright() as p:


        browser = await p.chromium.launch(
            headless=True
        )


        page = await browser.new_page(
            user_agent=
            "Mozilla/5.0 Windows Chrome"
        )


        print("🌐 Ouverture CROUS...")


        await page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )


        await page.wait_for_timeout(
            5000
        )


        html = await page.content()


        await browser.close()



    soup = BeautifulSoup(
        html,
        "html.parser"
    )



    # récupération des cartes logements
    cartes = soup.find_all(
        "article"
    )


    print(
        "Cartes trouvées :",
        len(cartes)
    )



    for carte in cartes:


        texte = carte.get_text(
            " ",
            strip=True
        )


        logements.append(
            {
                "texte": texte
            }
        )



    return logements



# ==============================
# PROGRAMME PRINCIPAL
# ==============================

async def main():


    seen = load_seen()


    logements = await get_accommodations()



    print(
        f"{len(logements)} logement(s) détecté(s)"
    )



    nouveaux = []



    for logement in logements:


        identifiant = logement["texte"]


        if identifiant not in seen:


            nouveaux.append(
                logement
            )

            seen.append(
                identifiant
            )



    if nouveaux:


        message = (
            "🏠 Nouveau logement CROUS Montpellier !\n\n"
        )


        for logement in nouveaux:


            message += (
                "📌 "
                +
                logement["texte"]
                +
                "\n\n"
                "----------------\n"
            )



        send_message(
            message
        )


        print(
            "🚨 Telegram envoyé"
        )


    else:

        print(
            "Aucun nouveau logement"
        )



    save_seen(
        seen
    )



    print(
        "✅ Surveillance terminée"
    )



if __name__ == "__main__":

    asyncio.run(
        main()
    )
