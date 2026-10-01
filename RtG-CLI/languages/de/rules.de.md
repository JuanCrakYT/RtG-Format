# RtG-CLI Befehlsregeln

## 1. Allgemeine Struktur

Ein RtG-CLI-Befehl besteht aus einem Hauptbefehl und optional Argumenten.
Allgemeines Format:

`rtg <befehl> [<argumente>]`

Das erste Argument nach `rtg` bestimmt, welcher Befehl oder Addon ausgeführt wird.

Beispiele:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Registrierte Befehle

Hauptbefehle müssen in der RtG-CLI-Konfiguration registriert sein.
Ein Befehl wird über seinen internen Schlüssel identifiziert.

Beispiel:

`image`

Der Schlüssel `image` identifiziert das entsprechende Addon, unabhängig vom dem Benutzer angezeigten Namen.
Beispiel:

`image` → `RtG Image`

`preview` → `RtG Preview`

Der angezeigte Name darf nicht als Befehlsidentifikator verwendet werden.

---

## 3. RtG-CLI-Befehle und Addon-Befehle

RtG-CLI und Addons können ihre eigenen Befehle und Argumente haben.

Bevor ein Addon identifiziert wird, gehören Befehle und Argumente zu RtG-CLI.
Nach der Identifikation eines Addons bestimmt das Präfix, wem jedes Argument gehört:

- Kein Bindestrich (`-`) → gehört zum Addon.
- Zwei Bindestriche (`--`) → gehört zum Addon.
- Ein Bindestrich (`-`) → gehört zu RtG-CLI.

Beispiel:

`rtg image convert`

- `image` → Addon.
- `convert` → Addon-Befehl.

Beispiel:

`rtg image --width 128`

- `image` → Addon.
- `--width` → Addon-Argument.
- `128` → Wert des Addon-Arguments.

Beispiel:

`rtg image -lang`

- `image` → Addon.
- `-lang` → RtG-CLI-Argument.

---

## 4. Systemargumente

Bevor ein Addon identifiziert wird, verwendet RtG-CLI seine eigenen Syntaxregeln.
Lange Systemoptionen verwenden zwei Bindestriche:

`rtg --version`
`rtg --help`

Systemabkürzungen verwenden einen Bindestrich:

`rtg -v`
`rtg -h`
`rtg -l`

Nachdem ein Addon identifiziert wurde, gehört eine Option, die mit einem einzelnen Bindestrich (`-`) beginnt, zu RtG-CLI.

Beispiel:

`rtg image -lang`
`rtg image -en`

---

## 5. Argumente vor und nach dem Addon

RtG-CLI-Argumente können eine unterschiedliche Bedeutung haben, je nachdem, ob sie vor oder nach der Identifikation des Addons erscheinen.

Bevor ein Addon identifiziert wird, gehören Argumente zu RtG-CLI.

Zum Beispiel:

`rtg --lang`

Zeigt die für RtG-CLI verfügbaren Sprachen an.

Nachdem ein Addon identifiziert wurde, werden Argumente gemäß den für Addons festgelegten Besitzregeln interpretiert.

Zum Beispiel:

`rtg image -lang`

Fragt die für das `image`-Addon verfügbaren Sprachen ab.

Auf diese Weise bestimmt die Position des Arguments seinen Kontext und verhindert, dass globale RtG-CLI-Argumente mit Argumenten verwechselt werden, die nach der Identifikation eines Addons verwendet werden.

---

## 6. Position der Systemargumente

Systemargumente dürfen nicht vor dem Befehl oder Addon erscheinen, auf das sie sich beziehen, wenn das Argument von diesem Befehl abhängt.

Korrektes Beispiel:

`rtg help image -en`

Falsches Beispiel:

`rtg help -en image`

In diesen beiden Beispielen verwendet der Systembefehl `help` diese Struktur, weshalb das zweite Beispiel falsch ist:
`help <target> <options>`

Die Position muss eindeutig bestimmen, welcher Befehl das Argument erhält.

---

## 7. Addon-Befehle und -Argumente

Befehle werden als einzelne Terminalargumente geschrieben.
Ein Befehl darf keine Leerzeichen enthalten, es sei denn, er ist in Anführungszeichen eingeschlossen.

Die folgenden Argumente können vom Addon gemäß seiner eigenen Schnittstelle verwendet werden.

Zum Beispiel:

`rtg image convert image`

kann interpretiert werden als:

- `image` → Addon
- `convert` → Addon-Befehl
- `image` → Befehlsargument

---

## 8. Verwendung von Bindestrichen in Addon-Befehlen

Nachdem ein Addon identifiziert wurde:

- Argumente ohne Bindestrich gehören zum Addon.
- Argumente mit zwei oder mehr Bindestrichen (`--`) gehören zum Addon.
- Argumente mit einem einzelnen Bindestrich (`-`) gehören zu RtG-CLI.

Beispiele:

`rtg image convert`
`convert` → Addon.

`rtg image --width 128`
`--width` → Addon.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Addon-Befehlsschnittstelle

Die spezifischen Befehle eines Addons werden vom Addon-Programm selbst definiert.
RtG-CLI verwendet die Addon-Konfiguration, um seine Befehlsschnittstelle über die Eigenschaft `program commands` zu lokalisieren.

Diese Eigenschaft enthält die Pfade zu den Dateien, die die Befehlsschnittstelle des Programms bereitstellen.

Beispiel:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI kann diese Schnittstelle verwenden, um die dem Addon verfügbaren Befehle zu ermitteln oder auszuführen, darf aber deren interne Bedeutung nicht annehmen oder ändern.

Ein Addon kann zusätzliche Befehle definieren, die nicht direkt als RtG-CLI-Befehle registriert sind.

Die interne Implementierung des Programms kann zwischen Addons variieren, solange sie eine mit den RtG-CLI-Regeln kompatible Schnittstelle bereitstellt.

---

## 10. Sprachen

Die für ein Addon verfügbaren Sprachen werden über seine Konfiguration definiert.

Beispiel:

`lang: ["es", "en"]`

Übersetzte Texte werden über den entsprechenden Sprachcode identifiziert.

Beispiel:

`content.de`
`content.en`

Der von RtG-CLI verwendete Sprachselektor muss als Systemargument betrachtet werden.

Beispiel:

`rtg help image -en`

---

## 11. Standardsprache

Wenn `-<sprache>` nicht angegeben wird, verwendet RtG-CLI die erste in `rules` definierte Sprache.
Wenn `-<sprache>` angegeben wird, verwendet RtG-CLI diese Sprache, falls verfügbar.

Die erste im `rules`-Objekt von `assets.json` definierte Sprache ist die Standardsprache für die Regeln.

Wenn der Benutzer die Regeln ohne Angabe einer Sprache anfordert, muss RtG-CLI diese erste Sprache verwenden.

Zum Beispiel:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

In diesem Fall:

`rtg -r`
und
`rtg --rules`

zeigen die Regeln auf Spanisch an, da `es` die erste definierte Sprache ist.
Um eine andere Sprache anzufordern, muss der entsprechende Selektor verwendet werden:

`rtg -r -en`

Die Reihenfolge der Sprachen innerhalb von `rules` bestimmt nur, welche Sprache die Standardsprache ist. Sie ändert nicht die verfügbaren Sprachen.

Diese Regel gilt auch für andere Sprachselektoren wie:

`rtg help image -es`

---

## 12. Die Sprache ändert nicht den Befehl

Das Ändern der Sprache ändert nur den von RtG-CLI angezeigten Text.
Es ändert nicht den internen Befehlsnamen.

Beispiel:

`rtg help image -es`

und

`rtg help image -en`

verweisen weiterhin auf denselben Befehl:

`image`

---

## 13. Hilfe

Die allgemeine Hilfe wird mit folgendem Befehl erhalten:

`rtg help`

Die Hilfe für einen bestimmten Befehl wird mit folgendem Befehl erhalten:

`rtg help <befehl>`

Die Hilfe kann in einer bestimmten Sprache angefordert werden:

`rtg help <befehl> -<sprache>`

Beispiel:

`rtg help image -en`

---

## 14. Sprachanfrage

Die für ein Addon verfügbaren Sprachen können mit folgendem Befehl abgefragt werden:

`rtg help <befehl> -lang`

Beispiel:

`rtg help image -lang`

Diese Option gehört zu RtG-CLI und nicht zum Addon.

---

## 15. Addons dürfen Systemregeln nicht ändern

Ein Addon kann seine eigenen Befehle und Argumente definieren, aber die Bedeutung von Argumenten, die für RtG-CLI reserviert sind, nicht neu definieren.

Zum Beispiel darf ein Addon `-h` nicht verwenden, um der Systemhilfe eine andere Bedeutung zu geben.
Namen, die für RtG-CLI reserviert sind, haben Vorrang vor Addon-Befehlen.
Von RtG-CLI reservierte Befehle und Optionen müssen explizit durch die CLI-Schnittstelle definiert werden.
Ein Addon kann das Verhalten einer reservierten Option nicht neu definieren.

---

## 16. Trennung zwischen Identifikator und Name

Der interne Schlüssel eines Addons wird zu dessen Identifikation verwendet.
Der Addon-Name wird nur als beschreibende Information oder zur Anzeige für den Benutzer verwendet.

Beispiel:

`image` → interner Identifikator

`RtG Image` → angezeigter Name

Es darf nicht angenommen werden, dass der angezeigte Name als Befehl verwendet werden kann.

---

## 17. Befehle müssen deterministisch sein

RtG-CLI muss in der Lage sein, zu bestimmen, ob ein Argument zum System oder zum Addon gehört, ohne vom beschreibenden Namen des Programms abzuhängen.

Die Interpretation muss auf der Befehlsstruktur und den Regeln basieren.

Beispiel:

`rtg help image -en`

muss immer auf die gleiche Weise interpretiert werden:

`rtg` → CLI

`help` → CLI-Befehl

`image` → Addon

`-en` → CLI-Option

---

## 18. Unbekannte Argumente

Nach der Identifikation eines Addons muss RtG-CLI den Besitz jedes Arguments gemäß seinem Präfix bestimmen.

* Ein Argument ohne Bindestrich gehört zum Addon.
* Ein Argument mit zwei oder mehr Bindestrichen (`--`) gehört zum Addon.
* Ein Argument mit einem einzelnen Bindestrich (`-`) gehört zu RtG-CLI.

Wenn RtG-CLI ein unbekanntes Systemargument erhält, muss es melden, dass die Option nicht existiert.

Addon-Argumente müssen an das Addon übergeben werden, ohne dass RtG-CLI versucht, ihre Bedeutung zu interpretieren.

---

## 19. Nicht registrierte Befehle nicht annehmen

RtG-CLI darf einen Befehl nicht als gültig betrachten, nur weil ein zugehöriger Ordner, eine Datei oder ein Programm existiert.

Der Befehl muss in der entsprechenden Konfiguration definiert sein.

---

## 20. Kompatibilität

Addons müssen die RtG-CLI-Syntaxregeln befolgen, um sich korrekt zu integrieren.
Ein Addon kann eine völlig andere interne Implementierung haben, aber seine Befehlsschnittstelle muss den von RtG-CLI festgelegten Regeln folgen.

---

## 21. Prioritätsregel

Nachdem ein Addon identifiziert wurde, ist ein einzelner Bindestrich (`-`) für RtG-CLI reserviert.
Ein Addon kann keine Argumente verwenden, die mit einem einzelnen Bindestrich beginnen.
Argumente, die mit zwei oder mehr Bindestrichen (`--`) beginnen oder nicht mit einem Bindestrich beginnen, gehören zum Addon.

---

## 22. Addon-Argumente

Sobald das Addon identifiziert wurde, darf RtG-CLI die Bedeutung addon-spezifischer Argumente nicht annehmen.

Die dem Addon gehörenden Argumente müssen an das Addon-Programm übergeben werden, damit es sie verarbeiten kann.

Beispiel:

`rtg image --width 128`

RtG-CLI identifiziert `image` als Addon.

`--width 128` entspricht der RtG Image-Schnittstelle und muss von besagtem Addon verarbeitet werden.

---

## 23. Argumente mit Leerzeichen

Argumente, die Leerzeichen enthalten, müssen in Anführungszeichen geschrieben werden, damit das Terminal sie als ein einzelnes Argument behandelt.

Beispiel:

`rtg image "C:\Users\User\Downloads\mein bild.png" "C:\Users\User\Downloads\ausgabe.json"`

Der vollständige Pfad muss als einzelnes Argument empfangen werden.

---

## 24. Addon-Argumente müssen beibehalten werden

RtG-CLI darf Argumente, die für das Addon bestimmt sind, nicht modifizieren, entfernen oder neu interpretieren, es sei denn, eine explizite Systemregel besagt etwas anderes.

Argumente müssen in der Reihenfolge an das Addon übergeben werden, in der sie vom Benutzer bereitgestellt wurden.

---

## 25. Vollständige Beispiele

Addon-Befehl:

`rtg image`

Hilfe:

`rtg help image`

Hilfe auf Englisch:

`rtg help image -en`

Sprachen abfragen:

`rtg help image -lang`

CLI-Version:

`rtg --version`

CLI-Hilfe:

`rtg --help`

Eine addon-spezifische Option:

`rtg image --width 128`

Eine addon-spezifische Option mit Wert:

`rtg image --output datei.json`

Eine Kombination:

`rtg image bild.png --output ausgabe.json`

In diesem Beispiel:

* `image` identifiziert das Addon.
* `bild.png` ist ein Addon-Argument.
* `--output` ist eine Addon-Option.
* `ausgabe.json` ist der Wert dieser Option.
* Keines dieser Argumente sollte als Systemoption interpretiert werden.

---

## 26. Starttext-Sprache

`rtg -language <sprache>` wählt die Sprache des von RtG-CLI angezeigten Starttexts.

Die Sprache muss innerhalb von `void-language` existieren.

Beispiel:

`rtg -language de`

zeigt den Text an, der in definiert ist:

`void-language.de`

Wenn `-language` nicht angegeben wird, verwendet RtG-CLI `void`.

Wenn die angeforderte Sprache nicht verfügbar ist, muss RtG-CLI melden, dass die Sprache nicht verfügbar ist.