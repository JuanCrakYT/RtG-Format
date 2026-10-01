RtG-CLI — Aiuto
================

RtG-CLI è l'interfaccia a riga di comando dell'ecosistema RtG-Format.
Permette di scoprire ed eseguire addon, interrogare le lingue, visualizzare regole e versione.

Utilizzo
---------

  rtg [OPZIONI] <COMANDO> [ARGOMENTI]

  Il primo argomento identifica il comando o l'addon da eseguire.

  Esempi:
    rtg image
    rtg preview
    rtg help image


Comandi di sistema
-------------------

  -h, --help        Mostra questa guida generale
  -v, --version     Mostra la versione di RtG-CLI
  -l, --lang        Elenca le lingue disponibili in RtG-CLI
  -r, --rules       Mostra le regole di RtG-CLI
  -c, --commands    Elenca i comandi interni di RtG-CLI
  -a, --addons      Elenca gli addon con documentazione visibile all'utente
  -language <lingua>  Imposta la lingua del testo di avvio (void)

Comando: help
--------------

  rtg help                    # Guida generale (questa schermata)
  rtg help <comando>          # Guida per un comando/addon specifico
  rtg help <comando> -<lingua>  # Guida in lingua specifica (es: -es, -en)
  rtg help <comando> -lang      # Lingue disponibili per quel comando

  Esempi:
    rtg help image
    rtg help image -en
    rtg help image -lang


Comando: version
-----------------

  rtg -v
  rtg --version

  Mostra la versione e il contenuto della versione in tutte le lingue disponibili.


Comando: rules
---------------

  rtg -r
  rtg --rules
  rtg -r -<lingua>   # Regole in lingua specifica (es: rtg -r -en)

  Di default usa la prima lingua definita in 'rules' (spagnolo).


Comando: lang
--------------

  rtg -l
  rtg --lang

  Elenca tutte le lingue disponibili organizzate per categoria:
  Version, Rules, Help, Void, e per ogni addon.


Comando: commands
------------------

  rtg -c
  rtg --commands

  Elenca esclusivamente i comandi interni di RtG-CLI.
  Non include i comandi degli addon.


Comando: addons
----------------

  rtg -a
  rtg --addons

  Elenca gli addon che hanno documentazione/aiuto visibile per l'utente.
  Un addon registrato ma senza documentazione non appare qui.


Comando: language
------------------

  rtg -language <lingua>

  Seleziona la lingua del testo di avvio (void).
  La lingua deve esistere in 'void-language' di assets.json.

  Esempio:
    rtg -language en


Addon disponibili
------------------

  image      | RtG Image        - Convertitore immagini
  preview    | RtG Preview      - Visualizzatore 3D per build RtG-Format
  test-addon | RtG Test Addon   - Addon di test per validazione CLI


Lingue
-------

Le lingue sono indicate con un trattino singolo: -es, -en, -pt, ecc.
La lingua non cambia il nome interno del comando.

  rtg help image -es    # Aiuto in spagnolo
  rtg help image -en    # Aiuto in inglese
  rtg -r -en            # Regole in inglese

  Per vedere le lingue di un addon:
    rtg help image -lang

  Il significato di -lang dipende dalla sua posizione:
    rtg --lang          # Lingue RtG-CLI (prima dell'addon)
    rtg image -lang     # Lingue addon (dopo l'addon)


Argomenti degli addon
----------------------

Dopo aver identificato un addon, gli argomenti sono classificati per prefisso:

  senza trattino      -> addon        (es: convert, file.png)
  --opzione           -> addon        (es: --width 128)
  -opzione            -> RtG-CLI      (es: -lang, -en)

Esempi:
  rtg image convert file.png     # convert, file.png -> addon
  rtg image --width 128          # --width 128 -> addon
  rtg image -lang                # -lang -> RtG-CLI (lingue addon)
  rtg image -en                  # -en -> RtG-CLI (selettore lingua)


Argomenti con spazi
---------------------

Gli argomenti con spazi devono essere tra virgolette:

  rtg image "mia immagine.png" "output.json"

RtG-CLI preserva l'ordine degli argomenti e li passa tali quali all'addon.


Ulteriori informazioni
-----------------------

  rtg help <comando>      # Aiuto dettagliato di un addon
  rtg help <comando> -lang  # Lingue di quell'addon
  rtg --addons            # Vedi tutti gli addon documentati
  rtg --commands          # Vedi comandi interni