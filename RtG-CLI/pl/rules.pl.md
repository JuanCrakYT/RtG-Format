# Zasady poleceń RtG-CLI

## 1. Ogólna struktura

Polecenie RtG-CLI składa się z polecenia głównego oraz opcjonalnych argumentów.
Format ogólny:

`rtg <polecenie> [<argumenty>]`

Pierwszy argument po `rtg` decyduje, które polecenie lub dodatek zostanie wykonany.

Przykłady:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Zarejestrowane polecenia

Główne polecenia muszą być zarejestrowane w konfiguracji RtG-CLI.
Polecenie identyfikowane jest przez swój klucz wewnętrzny.

Przykład:

`image`

Klucz `image` identyfikuje odpowiadający dodatek, niezależnie od nazwy wyświetlanej użytkownikowi.
Przykład:

`image` → `RtG Image`

`preview` → `RtG Preview`

Wyświetlana nazwa nie może być używana jako identyfikator polecenia.

---

## 3. Polecenia RtG-CLI i polecenia dodatków

RtG-CLI oraz dodatki mogą posiadać własne polecenia i argumenty.

Przed zidentyfikowaniem dodatku, polecenia i argumenty należą do RtG-CLI.
Po zidentyfikowaniu dodatku, prefiks określa, do kogo należy każdy argument:

- Bez myślnika (`-`) → należy do dodatku.
- Dwa myślniki (`--`) → należy do dodatku.
- Jeden myślnik (`-`) → należy do RtG-CLI.

Przykład:

`rtg image convert`

- `image` → dodatek.
- `convert` → polecenie dodatku.

Przykład:

`rtg image --width 128`

- `image` → dodatek.
- `--width` → argument dodatku.
- `128` → wartość argumentu dodatku.

Przykład:

`rtg image -lang`

- `image` → dodatek.
- `-lang` → argument RtG-CLI.

---

## 4. Argumenty systemowe

Przed zidentyfikowaniem dodatku, RtG-CLI korzysta ze własnych reguł składni.
Długie opcje systemowe używają dwóch myślników:

`rtg --version`
`rtg --help`

Skróty systemowe używają jednego myślnika:

`rtg -v`
`rtg -h`
`rtg -l`

Po zidentyfikowaniu dodatku, opcja zaczynająca się od pojedynczego myślnika (`-`) należy do RtG-CLI.

Przykład:

`rtg image -lang`
`rtg image -en`

---

## 5. Argumenty przed i po dodatku

Argumenty RtG-CLI mogą mieć inne znaczenie w zależności od tego, czy pojawiają się przed, czy po zidentyfikowaniu dodatku.

Przed zidentyfikowaniem dodatku, argumenty należą do RtG-CLI.

Na przykład:

`rtg --lang`

Wyświetla dostępne dla RtG-CLI języki.

Po zidentyfikowaniu dodatku, argumenty interpretowane są zgodnie z zasadami własności ustalonymi dla dodatków.

Na przykład:

`rtg image -lang`

Zapytuje o dostępne dla dodatku `image` języki.

Dzięki temu pozycja argumentu określa jego kontekst i uniemożliwia pomyłkowanie globalnych argumentów RtG-CLI z argumentami używanymi po zidentyfikowaniu dodatku.

---

## 6. Pozycja argumentów systemowych

Argumenty systemowe nie powinny pojawiać się przed poleceniem lub dodatkiem, na które wpływają, gdy argument zależy od tego polecenia.

Poprawny przykład:

`rtg help image -en`

Błędny przykład:

`rtg help -en image`

W tych dwóch przykładach polecenie systemowe `help` używa tej struktury, dlatego drugi przykład jest niepoprawny:
`help <target> <options>`

Pozycja musi jasno określać, które polecenie otrzymuje argument.

---

## 7. Polecenia i argumenty dodatków

Polecenia zapisywane są jako osobne argumenty terminala.
Polecenie nie powinno zawierać spacji, chyba że jest ujęte w cudzysłów.

Następujące argumenty mogą być używane przez dodatek zgodnie z jego własnym interfejsem.

Na przykład:

`rtg image convert image`

może zostać zinterpretowane jako:

- `image` → dodatek
- `convert` → polecenie dodatku
- `image` → argument polecenia

---

## 8. Użycie myślników w poleceniach dodatków

Po zidentyfikowaniu dodatku:

- Argumenty bez myślnika należą do dodatku.
- Argumenty z dwoma lub więcej myślnikami (`--`) należą do dodatku.
- Argumenty z pojedynczym myślnikiem (`-`) należą do RtG-CLI.

Przykłady:

`rtg image convert`
`convert` → dodatek.

`rtg image --width 128`
`--width` → dodatek.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Interfejs poleceń dodatków

Polecenia specyficzne dla dodatku są definiowane przez sam program dodatku.
RtG-CLI wykorzystuje konfigurację dodatku do zlokalizowania jego interfejsu poleceń przez właściwość `program commands`.

Właściwość ta zawiera ścieżki do plików dostarczających interfejs poleceń programu.

Przykład:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI może używać tego interfejsu do odnajdywania lub wykonywania poleceń dostępnych dla dodatku, ale nie powinien zakładać ani modyfikować znaczenia jego wewnętrznych poleceń.

Dodatek może definiować dodatkowe polecenia, które nie są rejestrowane bezpośrednio jako polecenia RtG-CLI.

Wewnętrzna implementacja programu może się różnić między dodatkami, o ile dostarcza interfejs zgodny z zasadami RtG-CLI.

---

## 10. Języki

Dostępne dla dodatku języki definiowane są przez jego konfigurację.

Przykład:

`lang: ["es", "en"]`

Przetłumaczone teksty identyfikowane są przy użyciu odpowiedniego kodu języka.

Przykład:

`content.pl`
`content.en`

Selektor języka używany przez RtG-CLI musi być traktowany jako argument systemowy.

Przykład:

`rtg help image -en`

---

## 11. Język domyślny

Jeśli `-<język>` nie jest określony, RtG-CLI użyje pierwszego języka zdefiniowanego w `rules`.
Jeśli `-<język>` jest określony, RtG-CLI użyje tego języka, jeśli jest dostępny.

Pierwszy zdefiniowany język w obiekcie `rules` pliku `assets.json` jest językiem domyślnym dla reguł.

Gdy użytkownik żąda reguł bez określania języka, RtG-CLI musi użyć tego pierwszego języka.

Na przykład:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

W tym przypadku:

`rtg -r`
oraz
`rtg --rules`

wyświetlą reguły w hiszpańskim, ponieważ `es` jest pierwszym zdefiniowanym językiem.
Aby zażądać innego języka, należy użyć odpowiedniego selektora:

`rtg -r -en`

Kolejność języków wewnątrz `rules` określa tylko, który język jest domyślny. Nie zmienia dostępnych języków.

Ta reguła dotyczy również innych selektorów języka, takich jak:

`rtg help image -es`

---

## 12. Język nie zmienia polecenia

Zmiana języka modyfikuje tylko tekst wyświetlany przez RtG-CLI.
Nie zmienia wewnętrznej nazwy polecenia.

Przykład:

`rtg help image -es`

oraz

`rtg help image -en`

wciąż odnoszą się do tego samego polecenia:

`image`

---

## 13. Pomoc

Ogólna pomoc uzyskuje się za pomocą:

`rtg help`

Pomoc dla konkretnego polecenia uzyskuje się za pomocą:

`rtg help <polecenie>`

Pomoc może zostać żądana w określonym języku:

`rtg help <polecenie> -<język>`

Przykład:

`rtg help image -en`

---

## 14. Zapytanie o języki

Dostępne dla dodatku języki można sprawdzić za pomocą:

`rtg help <polecenie> -lang`

Przykład:

`rtg help image -lang`

Ta opcja należy do RtG-CLI, a nie do dodatku.

---

## 15. Dodatki nie mogą modyfikować reguł systemowych

Dodatek może definiować własne polecenia i argumenty, ale nie może przedefiniować znaczenia argumentów zarezerwowanych przez RtG-CLI.

Na przykład, dodatek nie powinien używać `-h` do nadania innego znaczenia pomocy systemowej.
Nazwy zarezerwowane przez RtG-CLI mają priorytet nad poleceniami dodatków.
Polecenia i opcje zarezerwowane przez RtG-CLI muszą być jawnie zdefiniowane przez interfejs CLI.
Dodatek nie może przedefiniować zachowania zarezerwowanej opcji.

---

## 16. Rozróżnienie między identyfikatorem a nazwą

Wewnętrzny klucz dodatku służy do jego identyfikacji.
Nazwa dodatku służy tylko jako informacja opisowa lub do wyświetlenia użytkownikowi.

Przykład:

`image` → identyfikator wewnętrzny

`RtG Image` → wyświetlana nazwa

Nie należy zakładać, że wyświetlana nazwa może być używana jako polecenie.

---

## 17. Polecenia muszą być deterministyczne

RtG-CLI musi potrafić ustalić, czy argument należy do systemu, czy do dodatku, bez zależności od opisowej nazwy programu.

Interpretacja musi opierać się na strukturze i zasadach polecenia.

Przykład:

`rtg help image -en`

musi zawsze być interpretowany w ten sam sposób:

`rtg` → CLI

`help` → polecenie CLI

`image` → dodatek

`-en` → opcja CLI

---

## 18. Nieznane argumenty

Po zidentyfikowaniu dodatku, RtG-CLI musi określić własność każdego argumentu zgodnie z jego prefiksem.

* Argument bez myślnika należy do dodatku.
* Argument z dwoma lub więcej myślnikami (`--`) należy do dodatku.
* Argument z pojedynczym myślnikiem (`-`) należy do RtG-CLI.

Jeśli RtG-CLI otrzyma nieznany argument systemowy, musi zgłosić, że opcja nie istnieje.

Argumenty dodatku muszą zostać przekazane dodatkowi bez próby interpretacji ich znaczenia przez RtG-CLI.

---

## 19. Nie zakładać niezarejestrowanych poleceń

RtG-CLI nie powinien uważać polecenie za prawidłowe tylko dlatego, że istnieje powiązany folder, plik lub program.

Polecenie musi być zdefiniowane w odpowiedniej konfiguracji.

---

## 20. Kompatybilność

Dodatki muszą przestrzegać reguł składni RtG-CLI w celu poprawnej integracji.
Dodatek może mieć zupełnie inną implementację wewnętrzną, ale jego interfejs poleceń musi przestrzegać zasad ustalonych przez RtG-CLI.

---

## 21. Zasada priorytetu

Po zidentyfikowaniu dodatku, pojedynczy myślnik (`-`) jest zarezerwowany dla RtG-CLI.
Dodatek nie może używać argumentów zaczynających się od pojedynczego myślnika.
Argumenty zaczynające się od dwóch lub więcej myślników (`--`) lub nie zaczynające się od myślnika należą do dodatku.

---

## 22. Argumenty dodatku

Po zidentyfikowaniu dodatku, RtG-CLI nie powinien zakładać znaczenia argumentów specyficznych dla dodatku.

Argumenty należące do dodatku muszą zostać przekazane programowi dodatku do przetworzenia.

Przykład:

`rtg image --width 128`

RtG-CLI identyfikuje `image` jako dodatek.

`--width 128` odpowiada interfejsowi RtG Image i musi zostać przetworzone przez ten dodatek.

---

## 23. Argumenty ze spacjami

Argumenty zawierające spacje muszą być zapisane w cudzysłowie, aby terminal traktował je jako pojedynczy argument.

Przykład:

`rtg image "C:\Users\User\Downloads\moj obraz.png" "C:\Users\User\Downloads\wyjscie.json"`

Pełna ścieżka musi zostać odebrana jako pojedynczy argument.

---

## 24. Argumenty dodatku muszą zostać zachowane

RtG-CLI nie powinien modyfikować, usuwać ani ponownie interpretować argumentów przeznaczonych dla dodatku, chyba że jawna reguła systemowa stanowi inaczej.

Argumenty muszą zostać dostarczone do dodatku w kolejności, w jakiej zostały podane przez użytkownika.

---

## 25. Pełne przykłady

Polecenie dodatku:

`rtg image`

Pomoc:

`rtg help image`

Pomoc w angielskim:

`rtg help image -en`

Zapytanie o języki:

`rtg help image -lang`

Wersja CLI:

`rtg --version`

Pomoc CLI:

`rtg --help`

Opcja własna dodatku:

`rtg image --width 128`

Opcja własna dodatku z wartością:

`rtg image --output plik.json`

Kombinacja:

`rtg image plik.png --output wyjscie.json`

W tym przykładzie:

* `image` identyfikuje dodatek.
* `plik.png` to argument dodatku.
* `--output` to opcja dodatku.
* `wyjscie.json` to wartość tej opcji.
* Żaden z tych argumentów nie powinien być interpretowany jako opcja systemowa.

---

## 26. Język tekstu startowego

`rtg -language <język>` wybiera język tekstu startowego (void) wyświetlanego przez RtG-CLI.

Język musi istnieć wewnątrz `void-language`.

Przykład:

`rtg -language pl`

wyświetla zdefiniowany w tekście:

`void-language.pl`

Jeśli nie określono `-language`, RtG-CLI używa `void`.

Jeśli żądany język jest niedostępny, RtG-CLI musi zgłosić, że ten język jest niedostępny.