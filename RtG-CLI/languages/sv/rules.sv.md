# RtG-CLI-kommandoregler

## 1. Allmän struktur

Ett RtG-CLI-kommando består av ett huvudkommando och, valfritt, argument.
Allmänt format:

`rtg <kommando> [<argument>]`

Det första argumentet efter `rtg` avgör vilket kommando eller tillägg som ska köras.

Exempel:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Registrerade kommandon

Huvudkommandon måste vara registrerade i RtG-CLI-konfigurationen.
Ett kommando identifieras genom sin interna nyckel.

Exempel:

`image`

Nyckeln `image` identifierar det motsvarande tillägget, oavsett namnet som visas för användaren.
Exempel:

`image` → `RtG Image`

`preview` → `RtG Preview`

Det visade namnet får inte användas som kommandonidentifierare.

---

## 3. RtG-CLI-kommandon och tilläggskommandon

RtG-CLI och tillägg kan ha sina egna kommandon och argument.

Innan ett tillägg identifieras tillhör kommandon och argument RtG-CLI.
Efter att ett tillägg identifierats bestämmer prefixet vem varje argument tillhör:

- Utan bindestreck (`-`) → tillhör tillägget.
- Två bindestreck (`--`) → tillhör tillägget.
- Ett bindestreck (`-`) → tillhör RtG-CLI.

Exempel:

`rtg image convert`

- `image` → tillägg.
- `convert` → tilläggskommando.

Exempel:

`rtg image --width 128`

- `image` → tillägg.
- `--width` → tilläggsargument.
- `128` → värdet på tilläggsargumentet.

Exempel:

`rtg image -lang`

- `image` → tillägg.
- `-lang` → RtG-CLI-argument.

---

## 4. Systemargument

Innan ett tillägg identifieras använder RtG-CLI sina egna syntaxregler.
Långa systemalternativ använder två bindestreck:

`rtg --version`
`rtg --help`

Systemförkortningar använder ett bindestreck:

`rtg -v`
`rtg -h`
`rtg -l`

Efter att ett tillägg identifierats tillhör ett alternativ som börjar med ett enda bindestreck (`-`) RtG-CLI.

Exempel:

`rtg image -lang`
`rtg image -en`

---

## 5. Argument före och efter tillägget

RtG-CLI-argument kan ha olika betydelse beroende på om de dyker upp före eller efter identifiering av tillägget.

Innan ett tillägg identifieras tillhör argumenten RtG-CLI.

Till exempel:

`rtg --lang`

Visar tillgängliga språk för RtG-CLI.

Efter att ett tillägg identifierats tolkas argumenten enligt ägarreglerna etablerade för tillägg.

Till exempel:

`rtg image -lang`

Frågar tillgängliga språk för `image`-tillägget.

På detta sätt bestämmer argumentets position dess kontext och förhindrar att globala RtG-CLI-argument förväxlas med argument som används efter att ett tillägg identifierats.

---

## 6. Position av systemargument

Systemargument får inte dyka upp före kommandot eller tillägget de påverkar när argumentet beror på det kommandot.

Korrekt exempel:

`rtg help image -en`

Felaktigt exempel:

`rtg help -en image`

I dessa två exempel använder systemkommandot `help` denna struktur, varför det andra exemplet är felaktigt:
`help <target> <options>`

Positionen måste tydligt avgöra vilket kommando som tar emot argumentet.

---

## 7. Tilläggskommandon och -argument

Kommandon skrivs som enskilda terminalargument.
Ett kommando får inte innehålla blanksteg om det inte är inom citattecken.

Följande argument kan användas av tillägget enligt dess eget gränssnitt.

Till exempel:

`rtg image convert image`

kan tolkas som:

- `image` → tillägg
- `convert` → tilläggskommando
- `image` → kommandons argument

---

## 8. Användning av bindestreck i tilläggskommandon

Efter att ett tillägg identifierats:

- Argument utan bindestreck tillhör tillägget.
- Argument med två eller fler bindestreck (`--`) tillhör tillägget.
- Argument med ett enda bindestreck (`-`) tillhör RtG-CLI.

Exempel:

`rtg image convert`
`convert` → tillägg.

`rtg image --width 128`
`--width` → tillägg.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Tilläggskommandogränssnitt

De specifika kommandona för ett tillägg definieras av tilläggets program.
RtG-CLI använder tilläggskonfigurationen för att hitta dess kommandogränssnitt via egenskapen `program commands`.

Denna egenskap innehåller sökvägar till filer som tillhandahåller programmets kommandogränssnitt.

Exempel:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI kan använda detta gränssnitt för att upptäcka eller köra de för tillägget tillgängliga kommandona, men får inte anta eller ändra betydelsen av dess interna kommandon.

Ett tillägg kan definiera ytterligare kommandon som inte är registrerade direkt som RtG-CLI-kommandon.

Programmets interna implementering kan skilja sig mellan tillägg, så länge det tillhandahåller ett gränssnitt kompatibelt med RtG-CLI-reglerna.

---

## 10. Språk

De tillgängliga språken för ett tillägg definieras via dess konfiguration.

Exempel:

`lang: ["es", "en"]`

Översatta texter identifieras med motsvarande språk kod.

Exempel:

`content.sv`
`content.en`

Det språkväljare som RtG-CLI använder måste betraktas som ett systemargument.

Exempel:

`rtg help image -en`

---

## 11. Standardspråk

Om `-<språk>` inte anges använder RtG-CLI det första språket definierat i `rules`.
Om `-<språk>` anges använder RtG-CLI det språket om det är tillgängligt.

Det första språket definierat i `rules`-objektet i `assets.json` är standardspråket för reglerna.

När användaren begär reglerna utan att ange ett språk måste RtG-CLI använda det första språket.

Till exempel:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

I det här fallet:

`rtg -r`
och
`rtg --rules`

visar reglerna på spanska eftersom `es` är det första definierade språket.
För att begära ett annat språk måste dess motsvarande väljare användas:

`rtg -r -en`

Ordningen på språken inuti `rules` avgör endast vilket språk som är standard. Det ändrar inte de tillgängliga språken.

Denna regel gäller också för andra språkväljare som:

`rtg help image -es`

---

## 12. Språket ändrar inte kommandot

Att ändra språket modifierar endast texten som visas av RtG-CLI.
Det ändrar inte det interna kommandonamnet.

Exempel:

`rtg help image -es`

och

`rtg help image -en`

syftar fortfarande på samma kommando:

`image`

---

## 13. Hjälp

Allmän hjälp erhålls med:

`rtg help`

Hjälp för ett specifikt kommando erhålls med:

`rtg help <kommando>`

Hjälp kan begäras på ett specifikt språk:

`rtg help <kommando> -<språk>`

Exempel:

`rtg help image -en`

---

## 14. Språkkonsultation

De tillgängliga språken för ett tillägg kan konsolteras med:

`rtg help <kommando> -lang`

Exempel:

`rtg help image -lang`

Detta alternativ tillhör RtG-CLI och inte tillägget.

---

## 15. Tillägg får inte ändra systemregler

Ett tillägg kan definiera sina egna kommandon och argument, men kan inte omdefiniera betydelsen av argument reserverade av RtG-CLI.

Till exempel bör ett tillägg inte använda `-h` för att ge systemhjälpen en annan betydelse.
Namn reserverade av RtG-CLI har prioritet över tilläggskommandon.
Kommandon och alternativ reserverade av RtG-CLI måste definieras explicit av CLI-gränssnittet.
Ett tillägg kan inte omdefiniera beteendet för ett reserverat alternativ.

---

## 16. Separation mellan identifierare och namn

Tilläggs intern nyckel används för att identifiera det.
Tilläggs namn används bara som beskrivande information eller för att visas för användaren.

Exempel:

`image` → intern identifierare

`RtG Image` → visat namn

Man får inte anta att det visade namnet kan användas som kommando.

---

## 17. Kommandon måste vara deterministiska

RtG-CLI måste kunna avgöra om ett argument tillhör systemet eller tillägget utan att bero på programmets beskrivande namn.

Tolkningen måste baseras på kommandostrukturen och reglerna.

Exempel:

`rtg help image -en`

måste alltid tolkas på samma sätt:

`rtg` → CLI

`help` → CLI-kommando

`image` → tillägg

`-en` → CLI-alternativ

---

## 18. Okända argument

Efter att ett tillägg identifierats måste RtG-CLI bestämma ägandet av varje argument enligt dess prefix.

* Ett argument utan bindestreck tillhör tillägget.
* Ett argument med två eller fler bindestreck (`--`) tillhör tillägget.
* Ett argument med ett enda bindestreck (`-`) tillhör RtG-CLI.

Om RtG-CLI får ett okänt systemargument måste det rapportera att alternativet inte existerar.

Tilläggsargument måste skickas till tillägget utan att RtG-CLI försöker tolka deras betydelse.

---

## 19. Anta inte oregistrerade kommandon

RtG-CLI får inte betrakta ett kommando som giltigt bara för att en relaterad mapp, fil eller program existerar.

Kommandot måste definieras i motsvarande konfiguration.

---

## 20. Kompatibilitet

Tillägg måste följa RtG-CLI:s syntaxregler för att integreras korrekt.
Ett tillägg kan ha en helt annan intern implementation, men dess kommandogränssnitt måste följa reglerna etablerade av RtG-CLI.

---

## 21. Prioritetsregel

Efter att ett tillägg identifierats är ett enda bindestreck (`-`) reserverat för RtG-CLI.
Ett tillägg kan inte använda argument som börjar med ett enda bindestreck.
Argument som börjar med två eller fler bindestreck (`--`) eller som inte börjar med bindestreck tillhör tillägget.

---

## 22. Tilläggsargument

När tillägget identifierats får RtG-CLI inte anta betydelsen av tilläggsspecifika argument.

Argument som tillhör tillägget måste skickas till tilläggsprogrammet för bearbetning.

Exempel:

`rtg image --width 128`

RtG-CLI identifierar `image` som tillägg.

`--width 128` motsvarar RtG Image-gränssnittet och måste bearbetas av nämnda tillägg.

---

## 23. Argument med mellanslag

Argument som innehåller mellanslag måste skrivas inom citattecken så att terminalen behandlar dem som ett enskilt argument.

Exempel:

`rtg image "C:\Users\User\Downloads\min bild.png" "C:\Users\User\Downloads\utdata.json"`

Den fullständiga sökvägen måste tas emot som ett enskilt argument.

---

## 24. Tilläggsargument måste bevaras

RtG-CLI får inte modifiera, ta bort eller omtolka argument avsedda för tillägget, om inte en explicit systemregel anger annat.

Argument måste levereras till tillägget i den ordning de angavs av användaren.

---

## 25. Fullständiga exempel

Tilläggskommando:

`rtg image`

Hjälp:

`rtg help image`

Hjälp på engelska:

`rtg help image -en`

Konsultera språk:

`rtg help image -lang`

CLI-version:

`rtg --version`

CLI-hjälp:

`rtg --help`

Ett tilläggsspecifikt alternativ:

`rtg image --width 128`

Ett tilläggsspecifikt alternativ med värde:

`rtg image --output fil.json`

En kombination:

`rtg image bild.png --output utdata.json`

I detta exempel:

* `image` identifierar tillägget.
* `bild.png` är ett tilläggsargument.
* `--output` är ett tilläggsalternativ.
* `utdata.json` är värdet på det alternativet.
* Ingen av dessa argument ska tolkas som ett systemalternativ.

---

## 26. Starttextens språk

`rtg -language <språk>` väljer språket för starttexten (void) som visas av RtG-CLI.

Språket måste finnas inuti `void-language`.

Exempel:

`rtg -language sv`

visar texten definierad i:

`void-language.sv`

Om `-language` inte anges använder RtG-CLI `void`.

Om det begärda språket inte är tillgängligt måste RtG-CLI rapportera att språket inte är tillgängligt.