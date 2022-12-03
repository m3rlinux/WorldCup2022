# World Cup 2022

<a href="https://www.buymeacoffee.com/m3rlinux" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 108px !important;" ></a>

Visualizza i risultati delle partite dei mondiali Qatar 2022 in tempo reale.

## Descrizione

L'applicazione si appoggia alle API Free sviluppate da [@raminmr](https://github.com/raminmr/free-api-worldcup2022) e tramite una guida interattiva registra l'utente alle API e lo guida nella consultazione dei risultati delle partite.

## Getting started

### Installazione

L'eseguibile non ha bisogno di installazione e' sufficiente scaricarlo ed eseguirlo

### Configurazione

Alla prima esecuzione la guida interattiva chiede alcune info di base per la registrazione dell'utente, come

- nome utente
- e-mail
- password

### Modificare il sorgente e ricreare l'eseguibile

Per poter modificare e testare i sorgenti occorre installare sul proprio sistema Python3 e Git, opzionale ma caldamente consigliato usare un IDE grafico, nel mio caso "Visual Studio Code".

**windows**

- [Python3](https://www.python.org/downloads/windows/) Consiglio di installare Python spuntando l'opzione "Add Python to PATH"
- [Git](https://gitforwindows.org/)

Dal menù "Start" selezionare "Git Bash" per aprire il prompt bash emulato.

Posizionarsi all'interno della cartella desiderata ed eseguire i seguenti comandi

``` bash
git clone https://github.com/m3rlinux/WorldCup2022.git
cd WorldCup2022
pip install pyinstaller
```

Abbiamo così clonato il progetto è installato il modulo pyinstaller che ci permettera di creare l'eseguibile.

Una volta effettuate le modifiche al sorgente eseguire il comando

``` bash
pyinstaller.exe --noconfirm --onefile --console --distpath "." --icon "src/mondiali.ico"  "src/mondiali.py"
```

### Ringraziamenti

Sentiti ringraziamenti vanno all'utente [@raminmr](https://github.com/raminmr) che ha reso disponibili gratuitamente le API

### To-do

- [ ] Permettere all'utente di selezionare una giornata diversa da quella corrente

### Licenza

Concesso in licenza secondo i termini della Licenza Apache, versione 2.0 [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0).
