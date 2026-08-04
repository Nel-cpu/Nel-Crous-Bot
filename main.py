import asyncio
from playwright.async_api import async_playwright


print("🤖 CROUS Diagnostic Playwright démarre !")


URL = (
    "https://trouverunlogement.lescrous.fr/"
    "tools/47/search?"
    "maxPrice=400"
    "&minArea=9"
    "&bounds=3.8070597_43.6533542_3.9413208_43.5667088"
    "&locationName=Montpellier"
)



async def main():


    async with async_playwright() as p:


        browser = await p.chromium.launch(
            headless=True
        )


        page = await browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )
        )


        print("🌐 Ouverture CROUS...")


        await page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )


        print("⏳ Attente chargement JavaScript...")


        await page.wait_for_timeout(
            10000
        )


        print(
            "📄 URL finale :",
            page.url
        )


        html = await page.content()


        texte = await page.locator(
            "body"
        ).inner_text()



        with open(
            "page_debug.html",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)



        with open(
            "texte_debug.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(texte)



        print(
            "💾 Fichiers diagnostic créés"
        )



        print("\n===== TEXTE VISIBLE =====\n")


        print(
            texte[:3000]
        )


        print(
            "\n===== RECHERCHE MOTS CLES ====="
        )



        mots = [
            "Résidence",
            "Residence",
            "Montpellier",
            "Loyer",
            "€",
            "m²",
            "Disponible",
            "Logement",
            "Studio"
        ]



        for mot in mots:


            if mot.lower() in texte.lower():

                print(
                    "✅ trouvé :",
                    mot
                )

            else:

                print(
                    "❌ absent :",
                    mot
                )



        # récupération des gros blocs de texte
        elements = await page.locator(
            "body *"
        ).all()



        print(
            "\nNombre éléments DOM :",
            len(elements)
        )



        compte = 0


        print(
            "\n===== BLOCS INTERESSANTS ====="
        )


        for element in elements:


            try:

                contenu = await element.inner_text(
                    timeout=500
                )


                if (
                    "€" in contenu
                    or
                    "m²" in contenu
                    or
                    "Résidence" in contenu
                    or
                    "Studio" in contenu
                ):

                    print(
                        "\n---\n",
                        contenu[:500]
                    )


                    compte += 1



                    if compte >= 10:

                        break


            except:

                pass



        await browser.close()



    print(
        "\n✅ Diagnostic terminé"
    )



if __name__ == "__main__":

    asyncio.run(
        main()
    )
