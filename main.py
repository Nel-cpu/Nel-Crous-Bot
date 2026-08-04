import requests
import re


print("🤖 Recherche endpoint CROUS réel")


URL = "https://trouverunlogement.lescrous.fr/tools/47/search?maxPrice=400&minArea=9&bounds=3.8070597_43.6533542_3.9413208_43.5667088&locationName=Montpellier"



headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}



try:


    response = requests.get(
        URL,
        headers=headers,
        timeout=20
    )


    print(
        "Code HTTP :",
        response.status_code
    )


    html = response.text


    print(
        "Taille HTML :",
        len(html)
    )



    # Recherche des URLs API
    patterns = [

        r'https://[^"\']+/api/[^"\']+',

        r'/api/[^"\']+',

        r'api/[^"\']+'

    ]



    trouve = set()



    for pattern in patterns:


        resultats = re.findall(
            pattern,
            html
        )


        for r in resultats:

            trouve.add(r)



    print("\n🔎 Endpoints trouvés :")


    if trouve:

        for url in trouve:

            print(
                "➡️",
                url
            )

    else:

        print(
            "Aucun endpoint trouvé dans HTML"
        )



except Exception as e:


    print(
        "Erreur :",
        e
    )



print(
    "\n✅ Analyse terminée"
)
