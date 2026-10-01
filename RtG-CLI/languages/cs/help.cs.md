RtG-CLI — Nápověda
===================

RtG-CLI je rozhraní příkazového řádku ekosystému RtG-Format.
Umožňuje objevovat a spouštět doplňky, dotazovat se na jazyky, zobrazovat pravidla a verze.

Použití
--------

  rtg [VOLEBY] <PŘÍKAZ> [ARGUMENTY]

  První argument identifikuje příkaz nebo doplněk, který se má spustit.

  Příklady:
    rtg image
    rtg preview
    rtg help image


Systémové příkazy
------------------

  -h, --help        Zobrazí tuto obecnou nápovědu
  -v, --version     Zobrazí verzi RtG-CLI
  -l, --lang        Zobrazí dostupné jazyky v RtG-CLI
  -r, --rules       Zobrazí pravidla RtG-CLI
  -c, --commands    Zobrazí interní příkazy RtG-CLI
  -a, --addons      Zobrazí doplňky s pro uživatele viditelnou dokumentací
  -u, --usage       Zobrazí obecné informace o použití (nové)
  -u-<jazyk>        Zobrazí použití v konkrétním jazyce (např. -u-es, -u-en) (nové)
  --usage-<jazyk>   Zobrazí použití v konkrétním jazyce (např. --usage-es, --usage-en) (nové)
  -language <jazyk>   Nastaví jazyk úvodního textu (void)

Příkaz: help
-------------

  rtg help                    # Obecná nápověda (tato obrazovka)
  rtg help <příkaz>           # Nápověda pro konkrétní příkaz/doplněk
  rtg help <příkaz> -<jazyk>  # Nápověda v konkrétním jazyce (např. -es, -en)
  rtg help <příkaz> -lang     # Dostupné jazyky pro ten příkaz
  rtg help -u                  # Obecná nápověda (nové)
  rtg help -u-<jazyk>          # Nápověda v konkrétním jazyce (např. -u-es) (nové)
  rtg help --usage             # Obecná nápověda (nové)
  rtg help --usage-<jazyk>     # Nápověda v konkrétním jazyce (např. --usage-es) (nové)
  rtg help usage               # Obecná nápověda (alternativní syntaxe, nové)

  Příklady:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es


Příkaz: version
----------------

  rtg -v
  rtg --version

  Zobrazí verzi a obsah verze ve všech dostupných jazycích.


Příkaz: rules
--------------

  rtg -r
  rtg --rules
  rtg -r -<jazyk>   # Pravidla v konkrétním jazyce (např. rtg -r -en)

  Ve výchozím nastavení používá první jazyk definovaný v 'rules' (španělština).


Příkaz: lang
-------------

  rtg -l
  rtg --lang

  Zobrazí všechny dostupné jazyky uspořádané podle kategorií:
  Version, Rules, Help, Void, a podle doplňku.


Příkaz: commands
-----------------

  rtg -c
  rtg --commands

  Zobrazí výhradně interní příkazy RtG-CLI.
  Neobsahuje příkazy doplňků.


Příkaz: addons
---------------

  rtg -a
  rtg --addons

  Zobrazí doplňky, které mají dokumentaci/nápovědu viditelnou pro uživatele.
  Zaregistrovaný doplněk bez dokumentace se zde nezobrazí.


Příkaz: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<jazyk>        # Použití v konkrétním jazyce (např. -u-es, -u-en) (nové)
  --usage-<jazyk>       Zobrazí použití v konkrétním jazyce (např. --usage-es, --usage-en) (nové)

  Zobrazí obecné informace o použití (void) v požadovaném jazyce.
  Jazyk musí existovat v 'void-language' v assets.json.


Příkaz: language
-----------------

  rtg -language <jazyk>

  Vybere jazyk úvodního textu (void).
  Jazyk musí existovat v 'void-language' v assets.json.

  Příklad:
    rtg -language en


Dostupné doplňky
-----------------

  image      | RtG Image        - Obrázkový konvertor
  preview    | RtG Preview      - 3D prohlížeč sestav RtG-Format
  test-addon | RtG Test Addon   - Testovací doplněk pro validaci CLI


Jazyky
-------

Jazyky se označují jedním spojovníkem: -es, -en, -pt, atd.
Jazyk nemění interní název příkazu.

  rtg help image -es    # Nápověda ve španělštině
  rtg help image -en    # Nápověda v angličtině
  rtg -r -en            # Pravidla v angličtině

  Pro zobrazení jazyků doplňku:
    rtg help image -lang

  Význam -lang závisí na jeho pozici:
    rtg --lang          # Jazyky RtG-CLI (před doplňkem)
    rtg image -lang     # Jazyky doplňku (po doplňku)


Argumenty doplňků
-------------------

Po identifikaci doplňku jsou argumenty klasifikovány podle předpony:

  bez spojovníku      -> doplněk        (např. convert, soubor.png)
  --volba             -> doplněk        (např. --width 128)
  -volba              -> RtG-CLI        (např. -lang, -en)

Příklady:
  rtg image convert soubor.png     # convert, soubor.png -> doplněk
  rtg image --width 128            # --width 128 -> doplněk
  rtg image -lang                  # -lang -> RtG-CLI (jazyky doplňku)
  rtg image -en                    # -en -> RtG-CLI (výběr jazyku)


Argumenty s mezerami
---------------------

Argumenty obsahující mezery musí být v uvozovkách:

  rtg image "muj obrazek.png" "vystup.json"

RtG-CLI zachovává pořadí argumentů a předává je tak, jak jsou, doplňku.


Další informace
------------------

  rtg help <příkaz>      # Podrobná nápověda doplňku
  rtg help <příkaz> -lang  # Jazyky toho doplňku
  rtg --addons           # Zobrazit všechny zdokumentované doplňky
  rtg --commands         # Zobrazit interní příkazy