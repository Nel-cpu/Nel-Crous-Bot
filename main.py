import asyncio

from playwright.async_api import async_playwright


print("🤖 CROUS Recherche humaine Playwright démarre !")


URL = "https://trouverunlogement.lescrous.fr/tools/47/search"



async def main():

    async with async_playwright() as p:


        browser = await p.chromium.launch(
            headless=True
        )


        page = await browser.new_page()


        print("🌐 Ouverture CROUS")


        await page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )


        await page.wait_for_timeout(
            5000
        )


        print("🔎 Recherche de Montpellier")


        # champ de recherche ville
        inputs = await page.locator(
            "input"
        ).all()


        print(
            "Nombre inputs :",
            len(inputs)
        )


        for i, inp in enumerate(inputs):

            try:

                placeholder = await inp.get_attribute(
                    "placeholder"
                )

                print(
                    i,
                    placeholder
                )

            except:

                pass



        await browser.close()



if __name__ == "__main__":

    asyncio.run(main())
