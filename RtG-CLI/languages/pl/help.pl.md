RtG-CLI — Pomoc
================

RtG-CLI to interfejs wiersza poleceń ekosystemu RtG-Format.
Pozwala na odkrywanie i wykonywanie dodatków, zapytania o języki, przegląd reguł i wersji.

Użycie
-------

  rtg [OPCJE] <POLECENIE> [ARGUMENTY]

  Pierwszy argument identyfikuje polecenie lub dodatek do wykonania.

  Przykłady:
    rtg image
    rtg preview
    rtg help image


Polecenia systemowe
--------------------

  -h, --help        Wyświetla tę ogólną pomoc
  -v, --version     Wyświetla wersję RtG-CLI
  -l, --lang        Wyświetla dostępne języki w RtG-CLI
  -r, --rules       Wyświetla reguły RtG-CLI
  -c, --commands    Wyświetla wewnętrzne polecenia RtG-CLI
  -a, --addons      Wyświetla dodatki z dokumentacją widoczną dla użytkownika
  -u, --usage       Wyświetla ogólne informacje o użyciu (nowe)
  -u-<język>        Wyświetla użycie w konkretnym języku (np. -u-es, -u-en) (nowe)
  --usage-<język>   Wyświetla użycie w konkretnym języku (np. --usage-es, --usage-en) (nowe)
  -language <język>   Ustawia język tekstu startowego (void)

Polecenie: help
----------------

  rtg help                    # Ogólna pomoc (ten ekran)
  rtg help <polecenie>        # Pomoc dla konkretnego polecenia/dodatku
  rtg help <polecenie> -<język> # Pomoc w konkretnym języku (np. -es, -en)
  rtg help <polecenie> -lang    # Dostępne języki dla tego polecenia
  rtg help -u                  # Ogólne użycie (nowe)
  rtg help -u-<język>           # Użycie w konkretnym języku (np. -u-es) (nowe)
  rtg help --usage             # Ogólne użycie (nowe)
  rtg help --usage-<język>      # Użycie w konkretnym języku (np. --usage-es) (nowe)
  rtg help usage               # Ogólne użycie (składnia alternatywna, nowe)

  Przykłady:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es


Polecenie: version
--------------------

  rtg -v
  rtg --version

  Wyświetla wersję i treść wersji we wszystkich dostępnych językach.


Polecenie: rules
-----------------

  rtg -r
  rtg --rules
  rtg -r -<język>   # Reguły w konkretnym języku (np. rtg -r -en)

  Domyślnie używa pierwszego zdefiniowanego języka w 'rules' (hiszpański).


Polecenie: lang
-----------------

  rtg -l
  rtg --lang

  Wyświetla wszystkie dostępne języki posortowane według kategorii:
  Version, Rules, Help, Void, oraz per dodatek.


Polecenie: commands
---------------------

  rtg -c
  rtg --commands

  Wyświetla wyłącznie wewnętrzne polecenia RtG-CLI.
  Nie zawiera poleceń dodatków.


Polecenie: addons
------------------

  rtg -a
  rtg --addons

  Wyświetla dodatki, które mają dokumentację/pomoc widoczną dla użytkownika.
  Zarejestrowany dodatek bez dokumentacji nie pojawia się tutaj.


Polecenie: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<język>         # Użycie w konkretnym języku (np. -u-es, -u-en) (nowe)
  --usage-<język>        Wyświetla użycie w konkretnym języku (np. --usage-es, --usage-en) (nowe)

  Wyświetla ogólne informacje o użyciu (void) w żądanym języku.
  Język musi istnieć w 'void-language' w assets.json.


Polecenie: language
---------------------

  rtg -language <język>

  Wybiera język tekstu startowego (void).
  Język musi istnieć w 'void-language' w assets.json.

  Przykład:
    rtg -language en


Dostępne dodatki
-----------------

  image      | RtG Image        - Konwerter obrazów
  preview    | RtG Preview      - Przeglądarka 3D budowli RtG-Format
  test-addon | RtG Test Addon   - Dodatek testowy do walidacji CLI


Języki
-------

Języki oznaczane są pojedynczym myślnikiem: -es, -en, -pt itd.
Język nie zmienia wewnętrznej nazwy polecenia.

  rtg help image -es    # Pomoc w hiszpańskim
  rtg help image -en    # Pomoc w angielskim
  rtg -r -en            # Reguły w angielskim

  Aby zobaczyć języki dodatku:
    rtg help image -lang

  Znaczenie -lang zależy od jego pozycji:
    rtg --lang          # Języki RtG-CLI (przed dodatkiem)
    rtg image -lang     # Języki dodatku (po dodatku)


Argumenty dodatków
--------------------

Po zidentyfikowaniu dodatku, argumenty klasyfikowane są według prefiksu:

  bez myślnika      -> dodatek        (np. convert, plik.png)
  --opcja           -> dodatek        (np. --width 128)
  -opcja            -> RtG-CLI        (np. -lang, -en)

Przykłady:
  rtg image convert plik.png     # convert, plik.png -> dodatek
  rtg image --width 128          # --width 128 -> dodatek
  rtg image -lang                # -lang -> RtG-CLI (języki dodatku)
  rtg image -en                  # -en -> RtG-CLI (selektor języka)


Argumenty ze spacjami
-----------------------

Argumenty zawierające spacje muszą być w cudzysłowie:

  rtg image "moj obraz.png" "wyjscie.json"

RtG-CLI zachowuje kolejność argumentów i przekazuje je jak są do dodatku.


Więcej informacji
-------------------

  rtg help <polecenie>      # Szczegółowa pomoc dodatku
  rtg help <polecenie> -lang  # Języki tego dodatku
  rtg --addons              # Zobacz wszystkie udokumentowane dodatki
  rtg --commands            # Zobacz polecenia wewnętrzne