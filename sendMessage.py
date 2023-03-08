from alright import WhatsApp
import requests

BASE_URL = "https://minesecdrh.cm/api/personnels/contacts/"

messenger = WhatsApp()
matricules = [ '731174-G', '731171-X', '545702-Q', '545834-S']

for matricule in matricules:
    response = requests.get(f'{BASE_URL}{matricule}')
    if response.status_code != 200:
        pass
    personnel = response.json()
    messenger.find_user(personnel["phone"])
    messenger.send_message(f'xa multiplie mes messages, je ne sais pourquoi')

#div#pane-side div[aria-rowcount] > div
#/html/body/div[1]/div/div/div[4]/div/div[2]/div/div[2]/div[3][last()]
""" open emoji panel
open button
//button[@data-testid='compose-btn-emoji'] 
smiley emoji
//div[contains(@title, 'Smileys & People')]
specific emoji
//div[@data-testid='list-item-{i}']/div/div/div/span[@data-emoji-index='{i}']
"""