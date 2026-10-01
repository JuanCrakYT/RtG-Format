RtG-CLI — Hulp
===============

RtG-CLI is de commandoregelinterface van het RtG-Format-ecosysteem.
Het maakt het ontdekken en uitvoeren van addons, het opvragen van talen, en het bekijken van regels en versies mogelijk.

Gebruik
--------

  rtg [OPTIES] <COMMANDO> [ARGUMENTEN]

  Het eerste argument identificeert het uit te voeren commando of de addon.

  Voorbeelden:
    rtg image
    rtg preview
    rtg help image


Systeemcommando's
------------------

  -h, --help        Toont deze algemene hulp
  -v, --version     Toont de RtG-CLI-versie
  -l, --lang        Toont de beschikbare talen in RtG-CLI
  -r, --rules       Toont de RtG-CLI-regels
  -c, --commands    Toont de interne RtG-CLI-commando's
  -a, --addons      Toont addons met voor de gebruiker zichtbare documentatie
  -u, --usage       Toont algemene gebruiksinformatie (nieuw)
  -u-<taal>         Toont gebruik in specifieke taal (bijv. -u-es, -u-en) (nieuw)
  --usage-<taal>    Toont gebruik in specifieke taal (bijv. --usage-es, --usage-en) (nieuw)
  -language <taal>   Stelt de taal van de opstarttekst (void) in

Commando: help
---------------

  rtg help                    # Algemene hulp (dit scherm)
  rtg help <commando>         # Hulp voor een specifiek commando/addon
  rtg help <commando> -<taal>  # Hulp in specifieke taal (bijv. -es, -en)
  rtg help <commando> -lang     # Beschikbare talen voor dat commando
  rtg help -u                  # Algemene hulp (nieuw)
  rtg help -u-<taal>           # Hulp in specifieke taal (bijv. -u-es) (nieuw)
  rtg help --usage             # Algemene hulp (nieuw)
  rtg help --usage-<taal>       # Hulp in specifieke taal (bijv. --usage-es) (nieuw)
  rtg help usage               # Algemene hulp (alternatieve syntaxis, nieuw)

  Voorbeelden:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es


Commando: version
------------------

  rtg -v
  rtg --version

  Toont de versie en versie-inhoud in alle beschikbare talen.


Commando: rules
----------------

  rtg -r
  rtg --rules
  rtg -r -<taal>   # Regels in specifieke taal (bijv. rtg -r -en)

  Standaard gebruikt de eerste taal gedefinieerd in 'rules' (Spaans).


Commando: lang
---------------

  rtg -l
  rtg --lang

  Toont alle beschikbare talen, geordend per categorie:
  Version, Rules, Help, Void, en per addon.


Commando: commands
--------------------

  rtg -c
  rtg --commands

  Toont uitsluitend de interne RtG-CLI-commando's.
  Bevat geen addon-commando's.


Commando: addons
-----------------

  rtg -a
  rtg --addons

  Toont addons die gebruikerszichtbare documentatie/hulp hebben.
  Een geregistreerde addon zonder documentatie verschijnt hier niet.


Commando: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<taal>         # Gebruik in specifieke taal (bijv. -u-es, -u-en) (nieuw)
  --usage-<taal>        Toont gebruik in specifieke taal (bijv. --usage-es, --usage-en) (nieuw)

  Toont algemene gebruiksinformatie (void) in de aangevraagde taal.
  De taal moet bestaan in 'void-language' in assets.json.


Commando: language
--------------------

  rtg -language <taal>

  Selecteert de taal van de opstarttekst (void).
  De taal moet bestaan in 'void-language' in assets.json.

  Voorbeeld:
    rtg -language en


Beschikbare addons
-------------------

  image      | RtG Image        - Afbeeldingsconverter
  preview    | RtG Preview      - 3D-viewer voor RtG-Format builds
  test-addon | RtG Test Addon   - Test-addon voor CLI-validatie


Talen
------

Talen worden aangeduid met een enkele koppelteken: -es, -en, -pt, etc.
De taal verandert niet de interne commando-naam.

  rtg help image -es    # Hulp in het Spaans
  rtg help image -en    # Hulp in het Engels
  rtg -r -en            # Regels in het Engels

  Om talen van een addon te zien:
    rtg help image -lang

  De betekenis van -hangt af van de positie:
    rtg --lang          # RtG-CLI-talen (voor de addon)
    rtg image -lang     # Addon-talen (na de addon)


Addon-argumenten
-----------------

Na identificatie van een addon worden argumenten geclassificeerd op voorvoegsel:

  geen koppelteken    -> addon        (bijv. convert, bestand.png)
  --optie             -> addon        (bijv. --width 128)
  -optie              -> RtG-CLI      (bijv. -lang, -en)

Voorbeelden:
  rtg image convert bestand.png     # convert, bestand.png -> addon
  rtg image --width 128             # --width 128 -> addon
  rtg image -lang                   # -lang -> RtG-CLI (addon-talen)
  rtg image -en                     # -en -> RtG-CLI (taalselector)


Argumenten met spaties
------------------------

Argumenten met spaties moeten tussen aanhalingstekens:

  rtg image "mijn afbeelding.png" "uitvoer.json"

RtG-CLI behoudt de argumentvolgorde en geeft ze ongewijzigd door aan de addon.


Meer informatie
----------------

  rtg help <commando>      # Gedetailleerde hulp voor een addon
  rtg help <commando> -lang  # Talen van die addon
  rtg --addons             # Alle gedocumenteerde addons bekijken
  rtg --commands           # Interne commando's bekijken