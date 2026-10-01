RtG-CLI — Hjälp
================

RtG-CLI är kommandoradsgränssnittet för RtG-Format-ekosystemet.
Det gör det möjligt att upptäcka och köra tillägg, fråga efter språk, visa regler och versioner.

Användning
-----------

  rtg [ALTERNATIV] <KOMMANDO> [ARGUMENT]

  Det första argumentet identifierar kommandot eller tillägget som ska köras.

  Exempel:
    rtg image
    rtg preview
    rtg help image


Systemkommandon
----------------

  -h, --help        Visar denna allmänna hjälp
  -v, --version     Visar RtG-CLI-versionen
  -l, --lang        Visar tillgängliga språk i RtG-CLI
  -r, --rules       Visar RtG-CLI-regler
  -c, --commands    Visar RtG-CLI-interna kommandon
  -a, --addons      Visar tillägg med användarsynlig dokumentation
  -u, --usage       Visar allmän användningsinformation (nytt)
  -u-<språk>        Visar användning på specifikt språk (t.ex. -u-es, -u-en) (nytt)
  --usage-<språk>   Visar användning på specifikt språk (t.ex. --usage-es, --usage-en) (nytt)
  -language <språk>   Ställer in språket för starttexten (void)

Kommando: help
---------------

  rtg help                    # Allmän hjälp (den här skärmen)
  rtg help <kommando>         # Hjälp för ett specifikt kommando/tillägg
  rtg help <kommando> -<språk>  # Hjälp på specifikt språk (t.ex. -es, -en)
  rtg help <kommando> -lang     # Tillgängliga språk för det kommandot
  rtg help -u                  # Allmän hjälp (nytt)
  rtg help -u-<språk>          # Hjälp på specifikt språk (t.ex. -u-es) (nytt)
  rtg help --usage             # Allmän hjälp (nytt)
  rtg help --usage-<språk>      # Hjälp på specifikt språk (t.ex. --usage-es) (nytt)
  rtg help usage               # Allmän hjälp (alternativ syntax, nytt)

  Exempel:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es


Kommando: version
------------------

  rtg -v
  rtg --version

  Visar version och versionsinnehåll på alla tillgängliga språk.


Kommando: rules
----------------

  rtg -r
  rtg --rules
  rtg -r -<språk>   # Regler på specifikt språk (t.ex. rtg -r -en)

  Som standard använder den det första språket definierat i 'rules' (spanska).


Kommando: lang
---------------

  rtg -l
  rtg --lang

  Visar alla tillgängliga språk organiserade efter kategori:
  Version, Rules, Help, Void, och per tillägg.


Kommando: commands
--------------------

  rtg -c
  rtg --commands

  Visar enbart RtG-CLI-interna kommandon.
  Inkluderar inte tilläggskommandon.


Kommando: addons
-----------------

  rtg -a
  rtg --addons

  Visar tillägg som har användarsynlig dokumentation/hjälp.
  Ett registrerat tillägg utan dokumentation visas inte här.


Kommando: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<språk>        # Användning på specifikt språk (t.ex. -u-es, -u-en) (nytt)
  --usage-<språk>       Visar användning på specifikt språk (t.ex. --usage-es, --usage-en) (nytt)

  Visar allmän användningsinformation (void) på det begärda språket.
  Språket måste finnas i 'void-language' i assets.json.


Kommando: language
--------------------

  rtg -language <språk>

  Väljer språket för starttexten (void).
  Språket måste finnas i 'void-language' i assets.json.

  Exempel:
    rtg -language en


Tillgängliga tillägg
---------------------

  image      | RtG Image        - Bildkonverterare
  preview    | RtG Preview      - 3D-visare för RtG-Format-byggnader
  test-addon | RtG Test Addon   - Test-tillägg för CLI-validering


Språk
------

Språk anges med ett enda bindestreck: -es, -en, -pt, etc.
Språket ändrar inte det interna kommandonamnet.

  rtg help image -es    # Hjälp på spanska
  rtg help image -en    # Hjälp på engelska
  rtg -r -en            # Regler på engelska

  För att se språk för ett tillägg:
    rtg help image -lang

  Betydelsen av -lang beror på dess position:
    rtg --lang          # RtG-CLI-språk (innan tillägget)
    rtg image -lang     # Tilläggsspråk (efter tillägget)


Tilläggsargument
-----------------

Efter att ett tillägg identifierats klassificeras argumenten efter prefix:

  utan bindestreck     -> tillägg        (t.ex. convert, fil.png)
  --alternativ         -> tillägg        (t.ex. --width 128)
  -alternativ          -> RtG-CLI        (t.ex. -lang, -en)

Exempel:
  rtg image convert fil.png     # convert, fil.png -> tillägg
  rtg image --width 128         # --width 128 -> tillägg
  rtg image -lang               # -lang -> RtG-CLI (tilläggsspråk)
  rtg image -en                 # -en -> RtG-CLI (språkväljare)


Argument med mellanslag
------------------------

Argument med mellanslag måste vara inom citattecken:

  rtg image "min bild.png" "utdata.json"

RtG-CLI bevahrar argumentordningen och skickar dem som de är till tillägget.


Mer information
----------------

  rtg help <kommando>      # Detaljerad hjälp för ett tillägg
  rtg help <kommando> -lang  # Språk för det tillägget
  rtg --addons             # Visa alla dokumenterade tillägg
  rtg --commands           # Visa interna kommandon