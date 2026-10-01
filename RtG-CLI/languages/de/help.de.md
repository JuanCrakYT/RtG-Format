RtG-CLI — Hilfe
================

RtG-CLI ist die Kommandozeilenschnittstelle für das RtG-Format-Ökosystem.
Sie ermöglicht das Entdecken und Ausführen von Addons, das Abfragen von Sprachen, das Anzeigen von Regeln und der Version.

Verwendung
-----------

  rtg [OPTIONEN] <BEFEHL> [ARGUMENTE]

  Das erste Argument identifiziert den auszuführenden Befehl oder Addon.

  Beispiele:
    rtg image
    rtg preview
    rtg help image


Systembefehle
--------------

  -h, --help        Zeigt diese allgemeine Hilfe
  -v, --version     Zeigt die RtG-CLI-Version
  -l, --lang        Listet die verfügbaren Sprachen in RtG-CLI
  -r, --rules       Zeigt die RtG-CLI-Regeln
  -c, --commands    Listet die internen RtG-CLI-Befehle
  -a, --addons      Listet Addons mit verfügbarer Dokumentation
  -u, --usage       Zeigt die allgemeinen Verwendungsinformationen (neu)
  -u-<sprache>      Zeigt die Verwendung in einer bestimmten Sprache (z.B. -u-es, -u-en) (neu)
  --usage-<sprache> Zeigt die Verwendung in einer bestimmten Sprache (z.B. --usage-es, --usage-en) (neu)
  -language <sprache>  Legt die Sprache des Starttexts (void) fest

Befehl: help
-------------

  rtg help                    # Allgemeine Hilfe (dieser Bildschirm)
  rtg help <befehl>           # Hilfe für einen bestimmten Befehl/Addon
  rtg help <befehl> -<sprache>  # Hilfe in bestimmter Sprache (z.B. -es, -en)
  rtg help <befehl> -lang       # Verfügbare Sprachen für diesen Befehl
  rtg help -u                  # Allgemeine Verwendung (neu)
  rtg help -u-<sprache>         # Verwendung in bestimmter Sprache (z.B. -u-es) (neu)
  rtg help --usage             # Allgemeine Verwendung (neu)
  rtg help --usage-<sprache>    # Verwendung in bestimmter Sprache (z.B. --usage-es) (neu)
  rtg help usage               # Allgemeine Verwendung (alternative Syntax, neu)

  Beispiele:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-es
    rtg help --usage-es


Befehl: version
----------------

  rtg -v
  rtg --version

  Zeigt die Version und den Versionsinhalt in allen verfügbaren Sprachen.


Befehl: rules
--------------

  rtg -r
  rtg --rules
  rtg -r -<sprache>   # Regeln in bestimmter Sprache (z.B. rtg -r -en)

  Standardmäßig wird die erste in 'rules' definierte Sprache verwendet (Spanisch).


Befehl: lang
-------------

  rtg -l
  rtg --lang

  Listet alle verfügbaren Sprachen nach Kategorien organisiert:
  Version, Rules, Help, Void, und pro Addon.


Befehl: commands
-----------------

  rtg -c
  rtg --commands

  Listet ausschließlich die internen RtG-CLI-Befehle.
  Enthält keine Addon-Befehle.


Befehl: addons
---------------

  rtg -a
  rtg --addons

  Listet Addons mit für Benutzer sichtbarer Dokumentation/Hilfe.
  Ein registriertes Addon ohne Dokumentation erscheint hier nicht.


Befehl: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<sprache>       # Verwendung in bestimmter Sprache (z.B. -u-es, -u-en) (neu)
  --usage-<sprache>      Zeigt die Verwendung in einer bestimmten Sprache (z.B. --usage-es, --usage-en) (neu)

  Zeigt die allgemeinen Verwendungsinformationen (void) in der angeforderten Sprache.
  Die Sprache muss in 'void-language' in assets.json existieren.


Befehl: language
-----------------

  rtg -language <sprache>

  Wählt die Sprache des Starttexts (void).
  Die Sprache muss in 'void-language' in assets.json existieren.

  Beispiel:
    rtg -language en


Verfügbare Addons
------------------

  image      | RtG Image        - Bildkonverter
  preview    | RtG Preview      - 3D-Viewer für RtG-Format-Builds
  test-addon | RtG Test Addon   - Test-Addon für CLI-Validierung


Sprachen
---------

Sprachen werden mit einem einzelnen Bindestrich angegeben: -es, -en, -pt, etc.
Die Sprache ändert nicht den internen Befehlsnamen.

  rtg help image -es    # Hilfe auf Spanisch
  rtg help image -en    # Hilfe auf Englisch
  rtg -r -en            # Regeln auf Englisch

  Um Sprachen eines Addons anzuzeigen:
    rtg help image -lang

  Die Bedeutung von -lang hängt von der Position ab:
    rtg --lang          # RtG-CLI-Sprachen (vor dem Addon)
    rtg image -lang     # Addon-Sprachen (nach dem Addon)


Addon-Argumente
----------------

Nach der Identifikation eines Addons werden Argumente nach Präfix klassifiziert:

  kein Bindestrich    -> Addon        (z.B. convert, datei.png)
  --option            -> Addon        (z.B. --width 128)
  -option             -> RtG-CLI      (z.B. -lang, -en)

Beispiele:
  rtg image convert datei.png     # convert, datei.png -> Addon
  rtg image --width 128           # --width 128 -> Addon
  rtg image -lang                 # -lang -> RtG-CLI (Addon-Sprachen)
  rtg image -en                   # -en -> RtG-CLI (Sprachselektor)


Argumente mit Leerzeichen
--------------------------

Argumente mit Leerzeichen müssen in Anführungszeichen gesetzt werden:

  rtg image "mein bild.png" "ausgabe.json"

RtG-CLI bewahrt die Reihenfolge und übergibt die Argumente unverändert an das Addon.


Weitere Informationen
----------------------

  rtg help <befehl>      # Detaillierte Hilfe für ein Addon
  rtg help <befehl> -lang  # Sprachen für dieses Addon
  rtg --addons           # Alle dokumentierten Addons anzeigen
  rtg --commands         # Interne Befehle anzeigen