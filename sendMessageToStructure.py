from alright import WhatsApp
import requests
import re

BASE_URL = "https://minesecdrh.cm/api/personnels/contacts/structures"

messenger = WhatsApp()

structure_id = input("Veuillez entrer le numero de la structure")

response = requests.get(f'{BASE_URL}/{structure_id}')
if response.status_code != 200:
    raise SystemExit("Erreur l'ors de la recuperation des donnees")

# A list of personnel
personnels = response.json()

for personnel in personnels:
    if re.match(r"^237[0-9]{9}$", personnel["phone"]):
        messenger.send_message1(personnel["phone"], f'Bien le bonjour et bon dimanche aux personnels du {personnel["structure"]}')
    else:
        print(f"le numero {personnel['phone']} n'a pas de compte WhatsApp ou est mal saisie")
