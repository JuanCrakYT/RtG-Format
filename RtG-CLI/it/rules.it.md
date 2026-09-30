# Regole dei comandi RtG-CLI

## 1. Struttura generale

Un comando RtG-CLI consiste di un comando principale e, opzionalmente, argomenti.
Formato generale:

`rtg <comando> [<argomenti>]`

Il primo argomento dopo `rtg` determina quale comando o addon verrà eseguito.

Esempi:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Comandi registrati

I comandi principali devono essere registrati nella configurazione di RtG-CLI.
Un comando è identificato dalla sua chiave interna.

Esempio:

`image`

La chiave `image` identifica l'addon corrispondente, indipendentemente dal nome mostrato all'utente.
Esempio:

`image` → `RtG Image`

`preview` → `RtG Preview`

Il nome visualizzato non deve essere usato come identificatore del comando.

---

## 3. Comandi RtG-CLI e comandi degli addon

RtG-CLI e gli addon possono avere i propri comandi e argomenti.

Prima di identificare un addon, comandi e argomenti appartengono a RtG-CLI.
Dopo aver identificato un addon, il prefisso determina a chi appartiene ogni argomento:

- Senza trattino (`-`) → appartiene all'addon.
- Due trattini (`--`) → appartiene all'addon.
- Un trattino (`-`) → appartiene a RtG-CLI.

Esempio:

`rtg image convert`

- `image` → addon.
- `convert` → comando dell'addon.

Esempio:

`rtg image --width 128`

- `image` → addon.
- `--width` → argomento dell'addon.
- `128` → valore dell'argomento dell'addon.

Esempio:

`rtg image -lang`

- `image` → addon.
- `-lang` → argomento di RtG-CLI.

---

## 4. Argomenti di sistema

Prima di identificare un addon, RtG-CLI usa le proprie regole di sintassi.
Le opzioni lunghe di sistema usano due trattini:

`rtg --version`
`rtg --help`

Le abbreviazioni di sistema usano un trattino:

`rtg -v`
`rtg -h`
`rtg -l`

Dopo aver identificato un addon, un'opzione che inizia con un singolo trattino (`-`) appartiene a RtG-CLI.

Esempio:

`rtg image -lang`
`rtg image -en`

---

## 5. Argomenti prima e dopo l'addon

Gli argomenti di RtG-CLI possono avere significati diversi a seconda che appaiano prima o dopo l'identificazione dell'addon.

Prima di identificare un addon, gli argomenti appartengono a RtG-CLI.

Per esempio:

`rtg --lang`

Mostra le lingue disponibili per RtG-CLI.

Dopo aver identificato un addon, gli argomenti sono interpretati secondo le regole di proprietà stabilite per gli addon.

Per esempio:

`rtg image -lang`

Interroga le lingue disponibili per l'addon `image`.

In questo modo, la posizione dell'argomento determina il suo contesto e previene la confusione tra argomenti globali di RtG-CLI e argomenti usati dopo l'identificazione di un addon.

---

## 6. Posizione degli argomenti di sistema

Gli argomenti di sistema non devono apparire prima del comando o addon che influenzano quando l'argomento dipende da quel comando.

Esempio corretto:

`rtg help image -en`

Esempio errato:

`rtg help -en image`

In questi due esempi, il comando di sistema `help` usa questa struttura, per cui il secondo esempio è errato:
`help <target> <options>`

La posizione deve permettere di determinare chiaramente quale comando riceve l'argomento.

---

## 7. Comandi e argomenti degli addon

I comandi sono scritti come argomenti individuali del terminale.
Un comando non deve contenere spazi a meno che non sia tra virgolette.

I seguenti argomenti possono essere usati dall'addon secondo la sua interfaccia.

Per esempio:

`rtg image convert image`

può essere interpretato come:

- `image` → addon
- `convert` → comando dell'addon
- `image` → argomento del comando

---

## 8. Uso dei trattini nei comandi degli addon

Dopo aver identificato un addon:

- Gli argomenti senza trattino appartengono all'addon.
- Gli argomenti con due o più trattini (`--`) appartengono all'addon.
- Gli argomenti con un singolo trattino (`-`) appartengono a RtG-CLI.

Esempi:

`rtg image convert`
`convert` → addon.

`rtg image --width 128`
`--width` → addon.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Interfaccia comandi degli addon

I comandi specifici di un addon sono definiti dal programma dell'addon stesso.
RtG-CLI usa la configurazione dell'addon per localizzare la sua interfaccia comandi tramite la proprietà `program commands`.

Questa proprietà contiene i percorsi dei file che forniscono l'interfaccia comandi del programma.

Esempio:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI può usare questa interfaccia per scoprire o eseguire i comandi disponibili per l'addon, ma non deve assumere o modificare il significato dei suoi comandi interni.

Un addon può definire comandi aggiuntivi non registrati direttamente come comandi propri di RtG-CLI.

L'implementazione interna del programma può differire tra addon, purché fornisca un'interfaccia compatibile con le regole di RtG-CLI.

---

## 10. Lingue

Le lingue disponibili per un addon sono definite tramite la sua configurazione.

Esempio:

`lang: ["es", "en"]`

I testi tradotti sono identificati usando il codice lingua corrispondente.

Esempio:

`content.it`
`content.en`

Il selettore lingua usato da RtG-CLI deve essere considerato un argomento di sistema.

Esempio:

`rtg help image -en`

---

## 11. Lingua predefinita

Se `-<lingua>` non è specificato, RtG-CLI userà la prima lingua definita in `rules`.
Se `-<lingua>` è specificato, RtG-CLI userà quella lingua se disponibile.

La prima lingua definita nell'oggetto `rules` di `assets.json` è la lingua predefinita per le regole.

Quando l'utente richiede le regole senza specificare una lingua, RtG-CLI deve usare quella prima lingua.

Per esempio:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

In questo caso:

`rtg -r`
e
`rtg --rules`

mostreranno le regole in spagnolo perché `es` è la prima lingua definita.
Per richiedere un'altra lingua si deve usare il suo selettore corrispondente:

`rtg -r -en`

L'ordine delle lingue dentro `rules` determina solo quale sarà la lingua predefinita. Non cambia le lingue disponibili.

Questa regola si applica anche per altri selettori di lingua come:

`rtg help image -es`

---

## 12. La lingua non cambia il comando

Cambiare la lingua modifica solo il testo mostrato da RtG-CLI.
Non cambia il nome interno del comando.

Esempio:

`rtg help image -es`

e

`rtg help image -en`

continuano a riferirsi allo stesso comando:

`image`

---

## 13. Aiuto

L'aiuto generale si ottiene con:

`rtg help`

L'aiuto per un comando specifico si ottiene con:

`rtg help <comando>`

L'aiuto può essere richiesto in una lingua specifica:

`rtg help <comando> -<lingua>`

Esempio:

`rtg help image -en`

---

## 14. Query lingue

Le lingue disponibili per un addon possono essere interrogate con:

`rtg help <comando> -lang`

Esempio:

`rtg help image -lang`

Questa opzione appartiene a RtG-CLI e non all'addon.

---

## 15. Gli addon non devono modificare le regole di sistema

Un addon può definire i propri comandi e argomenti, ma non può ridefinire il significato degli argomenti riservati da RtG-CLI.

Per esempio, un addon non deve usare `-h` per dare un significato diverso all'aiuto di sistema.
I nomi riservati da RtG-CLI hanno priorità sui comandi degli addon.
I comandi e opzioni riservati da RtG-CLI devono essere definiti esplicitamente dall'interfaccia CLI.
Un addon non può ridefinire il comportamento di un'opzione riservata.

---

## 16. Separazione tra identificatore e nome

La chiave interna dell'addon è usata per identificarlo.
Il nome dell'addon è usato solo come informazione descrittiva o per mostrarlo all'utente.

Esempio:

`image` → identificatore interno

`RtG Image` → nome visualizzato

Non si deve assumere che il nome visualizzato possa essere usato come comando.

---

## 17. I comandi devono essere deterministici

RtG-CLI deve poter determinare se un argomento appartiene al sistema o all'addon senza dipendere dal nome descrittivo del programma.

L'interpretazione deve basarsi sulla struttura e le regole del comando.

Esempio:

`rtg help image -en`

deve essere sempre interpretato nello stesso modo:

`rtg` → CLI

`help` → comando CLI

`image` → addon

`-en` → opzione CLI

---

## 18. Argomenti sconosciuti

Dopo aver identificato un addon, RtG-CLI deve determinare la proprietà di ogni argomento secondo il suo prefisso.

* Un argomento senza trattino appartiene all'addon.
* Un argomento con due o più trattini (`--`) appartiene all'addon.
* Un argomento con un solo trattino (`-`) appartiene a RtG-CLI.

Se RtG-CLI riceve un argomento di sistema che non riconosce, deve segnalare che l'opzione non esiste.

Gli argomenti dell'addon devono essere passati all'addon senza che RtG-CLI tenti di interpretarne il significato.

---

## 19. Non assumere comandi non registrati

RtG-CLI non deve considerare valido un comando solo perché esiste una cartella, file o programma correlato.

Il comando deve essere definito nella configurazione corrispondente.

---

## 20. Compatibilità

Gli addon devono seguire le regole di sintassi di RtG-CLI per integrarsi correttamente.
Un addon può avere un'implementazione interna completamente diversa, ma la sua interfaccia comandi deve seguire le regole stabilite da RtG-CLI.

---

## 21. Regola di priorità

Dopo aver identificato un addon, un solo trattino (`-`) è riservato per RtG-CLI.
Un addon non può usare argomenti che iniziano con un solo trattino.
Gli argomenti che iniziano con due o più trattini (`--`) o che non iniziano con trattino appartengono all'addon.

---

## 22. Argomenti dell'addon

Una volta identificato l'addon, RtG-CLI non deve assumere il significato degli argomenti specifici dell'addon.

Gli argomenti appartenenti all'addon devono essere passati al programma dell'addon per l'elaborazione.

Esempio:

`rtg image --width 128`

RtG-CLI identifica `image` come addon.

`--width 128` corrisponde all'interfaccia di RtG Image e deve essere elaborato da detto addon.

---

## 23. Argomenti con spazi

Gli argomenti che contengono spazi devono essere scritti tra virgolette affinché il terminale li tratti come un unico argomento.

Esempio:

`rtg image "C:\Users\User\Downloads\mia immagine.png" "C:\Users\User\Downloads\output.json"`

Il percorso completo deve essere ricevuto come un unico argomento.

---

## 24. Gli argomenti dell'addon devono essere conservati

RtG-CLI non deve modificare, rimuovere o reinterpretare argomenti destinati all'addon, salvo quando una regola esplicita di sistema lo indichi.

Gli argomenti devono essere consegnati all'addon nell'ordine in cui sono stati forniti dall'utente.

---

## 25. Esempi completi

Comando addon:

`rtg image`

Aiuto:

`rtg help image`

Aiuto in inglese:

`rtg help image -en`

Consultare lingue:

`rtg help image -lang`

Versione CLI:

`rtg --version`

Aiuto CLI:

`rtg --help`

Opzione propria dell'addon:

`rtg image --width 128`

Opzione propria dell'addon con valore:

`rtg image --output file.json`

Una combinazione:

`rtg image image.png --output output.json`

In questo esempio:

* `image` identifica l'addon.
* `image.png` è un argomento dell'addon.
* `--output` è un'opzione dell'addon.
* `output.json` è il valore di quell'opzione.
* Nessuno di questi argomenti deve essere interpretato come opzione di sistema.

---

## 26. Lingua del testo di avvio

`rtg -language <lingua>` seleziona la lingua del testo di avvio mostrato da RtG-CLI.

La lingua deve esistere dentro `void-language`.

Esempio:

`rtg -language it`

mostra il testo definito in:

`void-language.it`

Se non si specifica `-language`, RtG-CLI usa `void`.

Se la lingua richiesta non è disponibile, RtG-CLI deve segnalare che quella lingua non è disponibile.