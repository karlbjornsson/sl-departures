# Hitta hpllplats ID

import requests
import json

response = requests.get("https://transport.integration.sl.se/v1/sites?expand=true")

data = response.json()

hallplats = "Ropsten"

for i in data:
    if hallplats.lower() in i["name"].lower():
        print(f"Hållplats: {i['name']} | siteID: {i['id']}")

