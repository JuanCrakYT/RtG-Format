# RtG-CLI commando-regels

## 1. Algemene structuur

Een RtG-CLI-commando bestaat uit een hoofcommando en, optioneel, argumenten.
Algemeen formaat:

`rtg <commando> [<argumenten>]`

Het eerste argument na `rtg` bepaalt welk commando of addon uitgevoerd wordt.

Voorbeelden:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Geregistreerde commando's

Hoofdcommando's moeten geregistreerd zijn in de RtG-CLI-configuratie.
Een commando wordt geïdentificeerd door zijn interne sleutel.

Voorbeeld:

`image`

De sleutel `image` identificeert de bijbehorende addon, ongeacht de naam die aan de gebruiker getoond wordt.
Voorbeeld:

`image` → `RtG Image`

`preview` → `RtG Preview`

De getoonde naam mag niet als commando-identificatie worden gebruikt.

---

## 3. RtG-CLI-commando's en addon-commando's

RtG-CLI en addons kunnen hun eigen commando's en argumenten hebben.

Voordat een addon geïdentificeerd is, behoren commando's en argumenten tot RtG-CLI.
Na identificatie van een addon bepaalt het voorvoegsel wie elk argument toebehoort:

- Geen koppelteken (`-`) → behoort tot de addon.
- Twee koppeltekens (`--`) → behoort tot de addon.
- Een koppelteken (`-`) → behoort tot RtG-CLI.

Voorbeeld:

`rtg image convert`

- `image` → addon.
- `convert` → addon-commando.

Voorbeeld:

`rtg image --width 128`

- `image` → addon.
- `--width` → addon-argument.
- `128` → waarde van het addon-argument.

Voorbeeld:

`rtg image -lang`

- `image` → addon.
- `-lang` → RtG-CLI-argument.

---

## 4. Systeemargumenten

Voordat een addon geïdentificeerd is, gebruikt RtG-CLI zijn eigen syntaxisregels.
Lange systeemopties gebruiken twee koppeltekens:

`rtg --version`
`rtg --help`

Systeemafkortingen gebruiken één koppelteken:

`rtg -v`
`rtg -h`
`rtg -l`

Na identificatie van een addon behoort een optie die met één koppelteken (`-`) begint tot RtG-CLI.

Voorbeeld:

`rtg image -lang`
`rtg image -en`

---

## 5. Argumenten voor en na de addon

RtG-CLI-argumenten kunnen een andere betekenis hebben, afhankelijk van of ze voor of na identificatie van de addon verschijnen.

Voordat een addon geïdentificeerd is, behoren argumenten tot RtG-CLI.

Bijvoorbeeld:

`rtg --lang`

Toont de beschikbare talen voor RtG-CLI.

Na identificatie van een addon worden argumenten geïnterpreteerd volgens de eigenaarsregels vastgelegd voor addons.

Bijvoorbeeld:

`rtg image -lang`

Vraagt de beschikbare talen op voor de `image`-addon.

Op deze manier bepaalt de positie van het argument zijn context en voorkomt verwarring tussen globale RtG-CLI-argumenten en argumenten die na identificatie van een addon gebruikt worden.

---

## 6. Positie van systeemargumenten

Systeemargumenten mogen niet voor het commando of de addon verschijnen waar ze van invloed zijn op wanneer het argument van dat commando afhangt.

Correct voorbeeld:

`rtg help image -en`

Incorrect voorbeeld:

`rtg help -en image`

In deze twee voorbeelden gebruikt het systeemcommando `help` deze structuur, daarom is het tweede voorbeeld onjuist:
`help <target> <options>`

De positie moet duidelijk bepalen welk commando het argument ontvangt.

---

## 7. Addon-commando's en -argumenten

Commando's worden geschreven als individuele terminal-argumenten.
Een commando mag geen spaties bevatten tenzij het tussen aanhalingstekens staat.

De volgende argumenten mogen door de addon worden gebruikt volgens zijn eigen interface.

Bijvoorbeeld:

`rtg image convert image`

kan geïnterpreteerd worden als:

- `image` → addon
- `convert` → addon-commando
- `image` → commando-argument

---

## 8. Gebruik van koppeltekens in addon-commando's

Na identificatie van een addon:

- Argumenten zonder koppelteken behoren tot de addon.
- Argumenten met twee of meer koppeltekens (`--`) behoren tot de addon.
- Argumenten met één koppelteken (`-`) behoren tot RtG-CLI.

Voorbeelden:

`rtg image convert`
`convert` → addon.

`rtg image --width 128`
`--width` → addon.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Addon-commando-interface

De specifieke commando's van een addon worden gedefinieerd door het addon-programma zelf.
RtG-CLI gebruikt de addon-configuratie om de commando-interface te localiseren via de eigenschap `program commands`.

Deze eigenschap bevat de paden naar de bestanden die de commando-interface van het programma leveren.

Voorbeeld:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI kan deze interface gebruiken om de voor de addon beschikbare commando's te ontdekken of uit te voeren, maar mag de betekenis van de interne commando's niet aannemen of wijzigen.

Een addon kan extra commando's definiëren die niet direct geregistreerd zijn als RtG-CLI-commando's.

De interne implementatie van het programma kan verschillen tussen addons, zolang het een interface biedt die compatibel is met de RtG-CLI-regels.

---

## 10. Talen

De beschikbare talen voor een addon worden gedefinieerd via zijn configuratie.

Voorbeeld:

`lang: ["es", "en"]`

Vertaalde teksten worden geïdentificeerd met de bijbehorende taalcode.

Voorbeeld:

`content.nl`
`content.en`

De taalselector die door RtG-CLI gebruikt wordt, moet als een systeemargument beschouwd worden.

Voorbeeld:

`rtg help image -en`

---

## 11. Standaardtaal

Als `-<taal>` niet gespecificeerd is, gebruikt RtG-CLI de eerste taal gedefinieerd in `rules`.
Als `-<taal>` gespecificeerd is, gebruikt RtG-CLI die taal als deze beschikbaar is.

De eerste taal gedefinieerd in het `rules`-object van `assets.json` is de standaardtaal voor de regels.

Wanneer de gebruiker de regels opvraagt zonder een taal te specificeren, moet RtG-CLI die eerste taal gebruiken.

Bijvoorbeeld:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

In dit geval:

`rtg -r`
en
`rtg --rules`

tonen de regels in het Spaans omdat `es` de eerste gedefinieerde taal is.
Om een andere taal op te vragen, moet de bijbehorende selector gebruikt worden:

`rtg -r -en`

De volgorde van de talen binnen `rules` bepaalt alleen welke taal de standaard is. Het verandert niet de beschikbare talen.

Deze regel geldt ook voor andere taalselectoren zoals:

`rtg help image -es`

---

## 12. De taal verandert het commando niet

Het wijzigen van de taal wijzigt alleen de door RtG-CLI getoonde tekst.
Het verandert niet de interne commando-naam.

Voorbeeld:

`rtg help image -es`

en

`rtg help image -en`

verwijzen nog steeds naar hetzelfde commando:

`image`

---

## 13. Help

Algemene help wordt verkregen met:

`rtg help`

Help voor een specifiek commando wordt verkregen met:

`rtg help <commando>`

Help kan in een specifieke taal worden aangevraagd:

`rtg help <commando> -<taal>`

Voorbeeld:

`rtg help image -en`

---

## 14. Taalopvraag

De beschikbare talen voor een addon kunnen worden opgevraagd met:

`rtg help <commando> -lang`

Voorbeeld:

`rtg help image -lang`

Deze optie behoort tot RtG-CLI en niet tot de addon.

---

## 15. Addons mogen systeemregels niet wijzigen

Een addon kan zijn eigen commando's en argumenten definiëren, maar kan de betekenis van door RtG-CLI gereserveerde argumenten niet herdefiniëren.

Bijvoorbeeld mag een addon `-h` niet gebruiken om de systeemhelp een andere betekenis te geven.
Namen gereserveerd door RtG-CLI hebben prioriteit over addon-commando's.
Door RtG-CLI gereserveerde commando's en opties moeten expliciet gedefinieerd zijn door de CLI-interface.
Een addon kan het gedrag van een gereserveerde optie niet herdefiniëren.

---

## 16. Scheiding tussen identificatie en naam

De interne sleutel van een addon wordt gebruikt om het te identificeren.
De addon-naam wordt alleen gebruikt als beschrijvende informatie of om het aan de gebruiker te tonen.

Voorbeeld:

`image` → interne identificatie

`RtG Image` → getoonde naam

Er mag niet aangenomen worden dat de getoonde naam als commando gebruikt kan worden.

---

## 17. Commando's moeten deterministisch zijn

RtG-CLI moet kunnen bepalen of een argument tot het systeem of tot de addon behoort, zonder afhankelijk te zijn van de beschrijvende naam van het programma.

De interpretatie moet gebaseerd zijn op de commando-structuur en regels.

Voorbeeld:

`rtg help image -en`

moet altijd op dezelfde manier geïnterpreteerd worden:

`rtg` → CLI

`help` → CLI-commando

`image` → addon

`-en` → CLI-optie

---

## 18. Onbekende argumenten

Na identificatie van een addon moet RtG-CLI de eigendom van elk argument bepalen volgens zijn voorvoegsel.

* Een argument zonder koppelteken behoort tot de addon.
* Een argument met twee of meer koppeltekens (`--`) behoort tot de addon.
* Een argument met één koppelteken (`-`) behoort tot RtG-CLI.

Als RtG-CLI een onbekend systeemargument ontvangt, moet het melden dat de optie niet bestaat.

Addon-argumenten moeten aan de addon doorgegeven worden zonder dat RtG-CLI probeert hun betekenis te interpreteren.

---

## 19. Geen ongeregestreerde commando's aannemen

RtG-CLI mag een commando niet geldig achten alleen omdat een gerelateerde map, bestand of programma bestaat.

Het commando moet gedefinieerd zijn in de bijbehorende configuratie.

---

## 20. Compatibiliteit

Addons moeten de RtG-CLI-syntaxregels volgen om correct te integreren.
Een addon kan een volledig andere interne implementatie hebben, maar zijn commando-interface moet de regels volgen die door RtG-CLI vastgelegd zijn.

---

## 21. Prioriteitsregel

Na identificatie van een addon is een enkel koppelteken (`-`) gereserveerd voor RtG-CLI.
Een addon kan geen argumenten gebruiken die met één koppelteken beginnen.
Argumenten die met twee of meer koppeltekens (`--`) beginnen of die niet met een koppelteken beginnen, behoren tot de addon.

---

## 22. Addon-argumenten

Eenmaal de addon geïdentificeerd, mag RtG-CLI de betekenis van addon-specifieke argumenten niet aannemen.

Argumenten die tot de addon behoren, moeten aan het addon-programma doorgegeven worden voor verwerking.

Voorbeeld:

`rtg image --width 128`

RtG-CLI identificeert `image` als addon.

`--width 128` komt overeen met de RtG Image-interface en moet door genoemde addon verwerkt worden.

---

## 23. Argumenten met spaties

Argumenten die spaties bevatten moeten tussen aanhalingstekens geschreven worden zodat de terminal ze als één argument behandelt.

Voorbeeld:

`rtg image "C:\Users\User\Downloads\mijn afbeelding.png" "C:\Users\User\Downloads\uitvoer.json"`

Het complete pad moet als één argument ontvangen worden.

---

## 24. Addon-argumenten moeten bewaard blijven

RtG-CLI mag argumenten bestemd voor de addon niet wijzigen, verwijderen of herinterpreteren, tenzij een expliciete systeemregel anders aangeeft.

Argumenten moeten in de volgorde waarin ze door de gebruiker geleverd werden, aan de addon geleverd worden.

---

## 25. Complete voorbeelden

Addon-commando:

`rtg image`

Help:

`rtg help image`

Help in het Engels:

`rtg help image -en`

Talen opvragen:

`rtg help image -lang`

CLI-versie:

`rtg --version`

CLI-help:

`rtg --help`

Een addon-specifieke optie:

`rtg image --width 128`

Een addon-specifieke optie met waarde:

`rtg image --output bestand.json`

Een combinatie:

`rtg image bestand.png --output uitvoer.json`

In dit voorbeeld:

* `image` identificeert de addon.
* `bestand.png` is een addon-argument.
* `--output` is een addon-optie.
* `uitvoer.json` is de waarde van die optie.
* Geen van deze argumenten mag geïnterpreteerd worden als een systeemoptie.

---

## 26. Opstarttekst-taal

`rtg -language <taal>` selecteert de taal van de opstarttekst (void) die door RtG-CLI getoond wordt.

De taal moet in `void-language` bestaan.

Voorbeeld:

`rtg -language nl`

toont de tekst gedefinieerd in:

`void-language.nl`

Als `-language` niet gespecificeerd is, gebruikt RtG-CLI `void`.

Als de aangevraagde taal niet beschikbaar is, moet RtG-CLI melden dat die taal niet beschikbaar is.