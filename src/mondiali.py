#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#----------------------------------------------------------------------------
# version     : 0.2.2
# Created By  : Davide Gibilisco
# Created Date: 24/08/2022
# ---------------------------------------------------------------------------

""" 
Presenta le partite odierne e ne mostra il risultato
----------------
"""  

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import requests
import json
from pprint import pprint
from time import sleep
from datetime import date
import configparser
import pathlib
from getpass import getpass
from icecream import ic

ic.disable()

day = int(date.today().strftime("%d")) - 19
nl = "\n"
url = f"http://api.cup2022.ir/api/v1/bymatch/{day}"
url_reg = f"http://api.cup2022.ir/api/v1/user"
url_login = f"http://api.cup2022.ir/api/v1/user/login"
headers = {'Content-Type': 'application/json'}
bot = "WorldCup2022: "
ok_list = ["si", "yes", "ok", "va bene"]
no_list = ["no", "ko", "non"]

config = configparser.ConfigParser()
file = pathlib.Path("worldcup2022.ini")
if file.exists():
    config.read(file)
    io = config["DEFAULT"]["Name"]
    token = config["DEFAULT"]["APIToken"]
else:
    io = input(f"{bot}Ciao sono il bot dei mondiali Qatar 2022, tu come ti chiami?{nl}???: ")
    while True:
        if not io:
            io = input(f"{bot}Non hai specificato il nome, riprova{nl}??? :")
        else:
            break
    print(f"{bot}Ciao {io}! E' la prima volta che avvii il programma! Ti aiutero' a configurarlo...")
    email = input(f"{bot}Dammi un idirizzo email (anche finto) per registrarti alle API di 'http://cup2022.ir'{nl}{io}: ")
    while True:
        if not email:
            email = input(f"{bot}Non hai specificato il tuo indirizzo email, ritenta{nl}{io}: ")
        elif "@" not in email or "." not in email.partition("@")[2] or not email.partition("@")[2][0].isalnum():
            email = input(f"{bot}Hai specificato un indirizzo email non valido, ritenta{nl}{io}: ")
        else:
            break
    print(f"{bot}Adesso inventa una password (almeno 8 caratteri con qualche numero)")
    while True:
        password = getpass()
        confirm = getpass(prompt="Conferma: ")
        if password == confirm:
            break
        else:
            print(f"{bot}le password inserite non corrispondono")
            sleep(1)
    print(f"{bot}Provo la registrazione alle API di http://cup2022.ir")

    payload_reg = {"name": io,
                "email": email,
                "password": password,
                "passwordConfirm": password}
    try_req = 0
    while try_req < 4:
        resp = requests.request("POST", url_reg, headers=headers, data=json.dumps(payload_reg))
        if resp.status_code == 504:
            sleep(3)
            try_req = try_req + 1
            continue
        else:
            break
    if resp.status_code == 200:
        print(f"{bot}{resp.json()['message']}")
        print(f"{bot}Eseguo il login")
        payload_login = {"email": email,
                    "password": password}

        resp = requests.request("POST", url_login, headers=headers, data=json.dumps(payload_login))
        status = resp.json()["status"]
        if status == "success":
            token = resp.json()["data"]["token"]
            print(f"{bot}Registrazione avvenuta correttamente")
    elif "shorter than the minimum" in resp.text:
        print(f"{bot}Scegli una password di almeno 8 caratteri e con qualche numero")
        exit(2)
    else:
        print(f"{bot}Qualcosa non ha funzionato durante la registrazione; errore:")
        print(f"{resp.text}")
        exit(2)

    config['DEFAULT'] = {
                        'Name': io,
                        'APIToken': token
                        }

    with open(file, 'w') as configfile:
        config.write(configfile)

auth = f"Bearer {token}"
payload={}
headers = {
          'Authorization': auth,
          'Content-Type': 'application/json'
          }

comando = input(f"{bot}Ciao {io}! Cosa posso fare per te?{nl}{io}: ")
while True:
    if "risult" in comando:
        print(f"{bot}Ok! Seleziona una partita...{nl}")
        break
    else:
        yesOrNo = input(f"{bot}Non ho capito! Vuoi vedere i risultati delle partite di oggi?{nl}{io}: ")
        while True:
            if yesOrNo in ok_list:
                print(f"{bot}Ok! Seleziona una partita...{nl}")
                break
            elif yesOrNo in no_list:
                yesOrNo = input(f"{bot}Al momento so fare solo questo, quindi vuoi vedere i risultati delle partite di oggi?{nl}{io}: ")
            else:
                yesOrNo = input(f"{bot}Non sono programmato per queste cose, quindi vuoi vedere i risultati delle partite di oggi?{nl}{io}: ")
        break

resp = requests.request("GET", url, headers=headers, data=payload)
if resp.status_code != 200:
    print(f"{bot}Il server ha restituito un errore:{nl}{resp.text}")
    exit(2)

matches = resp.json()["data"]

#pprint(matches)

count = 0
match_list = []
for match in matches:
    count = count + 1
    match_list.append(f'{count}. {match["home_team_en"]} - {match["away_team_en"]}')

count = count + 1
match_list.append(f'{count}. tutte le partite di oggi')

while True:
    choice = input(f'{nl.join(match_list)}{nl}{io}: ')
    for match in match_list:
        if match.startswith(choice):
            break
    else:
        print(f"{nl}{bot}Hai inserito una scelta non valida, ritenta...{nl}")
        sleep(1)
        continue
    if "tutte le partite" in match:
        print(f"{bot}Ecco i risultati di oggi: ")
        for match in matches:
            print(f"{match['home_team_en']} - {match['away_team_en']}: ", end= '')
            print(f"{match['home_score']} - {match['away_score']}")
            if not "null" in match['home_scorers']:
                home_scorers = match['home_scorers'][0].split(",")
                print(f"-> Marcatori {match['home_team_en']}: {', '.join(home_scorers)}")
            else:
                print(f"-> Marcatori {match['home_team_en']}: nessuno")
            if not "null" in match['away_scorers']:
                away_scorers = match['away_scorers'][0].split(",")
                print(f"-> Marcatori {match['away_team_en']}: {', '.join(away_scorers)}")
            else:
                print(f"-> Marcatori {match['away_team_en']}: nessuno")
            print("-----")
    else:
        print(f"{bot}Il risultato di {match[2:]} e' di: ", end = '')
        selector = int(choice) - 1
        print(f"{matches[selector]['home_score']} - {matches[selector]['away_score']}")
        if not "null" in matches[selector]['home_scorers']:
            home_scorers = matches[selector]['home_scorers'][0].split(",")
            print(f"-> Marcatori {matches[selector]['home_team_en']}: {', '.join(home_scorers)}")
        else:
            print(f"-> Marcatori {matches[selector]['home_team_en']}: nessuno")
        if not "null" in matches[selector]['away_scorers']:
            away_scorers = matches[selector]['away_scorers'][0].split(",")
            print(f"-> Marcatori {matches[selector]['away_team_en']}: {', '.join(away_scorers)}")
        else:
            print(f"-> Marcatori {matches[selector]['away_team_en']}: nessuno")

    sleep(1)
    continua = input(f"{nl}{bot}Vuoi vedere un altro risultato?{nl}{io}: ")
    if continua in ["Si", "si", "Yes", "yes"]:
        continue
    else:
        break
print(f"{bot}Perfetto! Alla prossima!")
exit = input(f"Premi un tasto per uscire")
