import requests
import json


print("🤖 Test API CROUS Montpellier")


API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search/47"


PARAMS_LIST = [

    {
        "maxPrice":400,
        "minArea":9,
        "page":0,
        "pageSize":100,
        "bounds":"3.8070597_43.6533542_3.9413208_43.5667088",
        "locationName":"Montpellier"
    },


    {
        "maxPrice":400,
        "minArea":9,
        "page":0,
        "pageSize":100,
        "city":"Montpellier"
    },


    {
        "maxPrice":400,
        "minArea":9,
        "page":0,
        "pageSize":100,
        "location":"Montpellier"
    },


    {
        "maxPrice":400,
        "minArea":9,
        "page":0,
        "pageSize":100,
        "search":"Montpellier"
    }

]



for index, params in enumerate(PARAMS_LIST):


    print("\n====================")
    print("TEST", index+1)
    print(params)


    try:

        response = requests.post(

            API_URL,

            json=params,

            headers={
                "User-Agent":"Mozilla/5.0",
                "Accept":"application/json"
            },

            timeout=20

        )


        data=response.json()


        logements=data.get(
            "results",
            {}
        ).get(
            "items",
            []
        )


        print(
            "Nombre logements :",
            len(logements)
        )



        for logement in logements[:5]:


            residence=logement.get(
                "residence",
                {}
            )


            print(
                "➡️",
                residence.get("label"),
                "|",
                residence.get("address")
            )


    except Exception as e:

        print(
            "Erreur :",
            e
        )


print("\n✅ Diagnostic terminé")
