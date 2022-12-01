#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#----------------------------------------------------------------------------
# version     : 0.1.0
# Created By  : Davide Gibilisco
# e-mail      : m3rlinux.it@gmail.com
# Created Date: 30/11/2022
# ---------------------------------------------------------------------------

""" 
Programmino che mostra i risutati delle partite di oggi

"""  

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import requests
import json
from time import sleep
import configparser
import pathlib
from getpass import getpass
from datetime import (datetime, timedelta)

__version__ = "0.1.0"

day_start = datetime.strptime("20/11/2022", "%d/%m/%Y")
now = datetime.now()
delta_days = (day_start - now).days
day = int(abs(delta_days))
nl = "\n"
url = f"http://api.cup2022.ir/api/v1/bymatch/{day}"
url_reg = f"http://api.cup2022.ir/api/v1/user"
url_login = f"http://api.cup2022.ir/api/v1/user/login"
headers = {'Content-Type': 'application/json'}
bot = "WorldCup2022: "
ok_list = ["si", "yes", "ok", "va bene"]
no_list = ["no", "ko", "non"]
date_format = "%m/%d/%Y %H:%M"
ita_date = "%d/%m/%Y %H:%M"

def login(email, password):
    payload_login = {"email": email,
                    "password": password}

    resp = requests.request("POST", url_login, headers=headers, data=json.dumps(payload_login))
    if resp.status_code == 200:
        status = resp.json()["status"]
        if status == "success":
            token = resp.json()["data"]["token"]
            return ("ok", token)
        else:
            return ("ko", resp.text)
    else:
        return ("ko", resp.text)


config = configparser.ConfigParser()
file = pathlib.Path("worldcup2022.ini")
if file.exists():
    config.read(file)
    io = config["DEFAULT"]["Name"]
    token = config["DEFAULT"]["APIToken"]
    email = config["DEFAULT"]["Email"]
    password = config["DEFAULT"]["Password"]
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
    resp = requests.request("POST", url_reg, headers=headers, data=json.dumps(payload_reg))
    if resp.status_code == 504:
        while try_req < 4:
            resp = requests.request("POST", url_reg, headers=headers, data=json.dumps(payload_reg))
            if resp.status_code == 504:
                sleep(3)
                try_req = try_req + 1
                continue
            elif resp.status_code == 200:
                break
    if resp.status_code != 200:
        if "shorter than the minimum" in resp.text:
            print(f"{bot}Scegli una password di almeno 8 caratteri e con qualche numero")
            uscita = input(f"Premi un tasto per uscire")
            exit(2)
        else:
            print(f"{bot}Qualcosa non ha funzionato durante la registrazione; errore:")
            print(f"{resp.text}")
            uscita = input(f"Premi un tasto per uscire")
            exit(2)

    print(f"{bot}{resp.json()['message']}")
    print(f"{bot}Eseguo il login")
    status, token = login(email, password)
    if status == "ok":
        print(f"{bot}Login avvenuto correttamente")
    else:
        print(f"{bot}Qualcosa e' andato storto durante il logine, errore{nl}")
        print(token)
        uscita = input(f"Premi un tasto per uscire")
        exit(2)

    config['DEFAULT'] = {
                        'Name': io,
                        'Email': email,
                        'Password': password,
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

resp = requests.request("GET", url, headers=headers, data=payload)
if resp.status_code == 401:
    print(f"{bot}Sessione scaduta riesegui il login")
    status, token = login(email, password)
    if status == "ok":
        print(f"{bot}Login avvenuto correttamente")
        config['DEFAULT']["apitoken"] = token
        auth = f"Bearer {token}"
        headers = {
            'Authorization': auth,
            'Content-Type': 'application/json'
            }
    else:
        print(f"{bot}Qualcosa e' andato storto durante il login, errore:{nl}")
        print(token)
        uscita = input(f"Premi un tasto per uscire")
        exit(2)

    with open(file, 'w') as configfile:
        config.write(configfile)
    
    resp = requests.request("GET", url, headers=headers, data=payload)

if resp.status_code != 200:
    print(f"{bot}Il server ha restituito un errore:{nl}{resp.text}")
    uscita = input(f"Premi un tasto per uscire")
    exit(2)

matches = resp.json()["data"]

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

count = 0
match_list = []
for match in matches:
    count = count + 1
    match_list.append(f'{count}. {match["home_team_en"]} - {match["away_team_en"]}')

count = count + 1
match_list.append(f'{count}. tutte le partite di oggi')
print(f"{nl.join(match_list)}{nl}")
while True:
    choice = input(f"{io}: ")
    if not choice:
        continue
    for match in match_list:
        if match.startswith(choice):
            break
    else:
        print(f"{nl}{bot}Hai inserito una scelta non valida, indica solo il numero relativo alla partita{nl}")
        sleep(1)
        continue
    if "tutte le partite" in match:
        print(f"{nl}{bot}Ecco i risultati di oggi:{nl}")
        for match in matches:
            eu_date = datetime.strptime(match["local_date"], date_format) - timedelta(hours=2)
            print(" ______________________________")
            print(f"| Partita del {datetime.strftime(eu_date, ita_date)} |")
            #print("################################")
            print(" ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
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
            if match["time_elapsed"] == "finished":
                print(f"-> Partita terminata")
            elif match["time_elapsed"] == "notstarted":
                print(f"-> Partita non ancora iniziata")
            else:
                print(f"-> Partita in corso, tempo trascorso: {match['time_elapsed']}")
            print("")
    else:
        selector = int(choice) - 1
        eu_date = datetime.strptime(matches[selector]["local_date"], date_format) - timedelta(hours=2)
        print(f"{nl}{bot}Il risultato di {match[2:]} e' di: ", end = '')
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
        print(f"-> Partita del {datetime.strftime(eu_date, ita_date)}")
        if matches[selector]["time_elapsed"] == "finished":
            print(f"-> Partita terminata")
        elif matches[selector]["time_elapsed"] == "notstarted":
            print(f"-> Partita non ancora iniziata")
        else:
            print(f"-> Partita in corso, tempo trascorso: {matches[selector]['time_elapsed']}")

    sleep(1)
    continua = input(f"{nl}{bot}Vuoi vedere un altro risultato?{nl}{io}: ")
    while True:
        if not continua:
            continua = input(f"{io}: ")
        elif continua in ok_list or continua in no_list:
            break
        else:
            continua = input(f"{bot} Non ho capito, rispondi si o no alla domanda precedente{nl}{io}: ")
    if continua in ok_list:
        continue
    else:
        break
print(f"{bot}Perfetto! Alla prossima!")
exit = input(f"Premi un tasto per uscire")
