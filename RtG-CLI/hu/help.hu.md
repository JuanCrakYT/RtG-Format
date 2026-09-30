RtG-CLI — Súgó
================

RtG-CLI az RtG-Format ökoszisztéma parancssori felülete.
Lehetővé teszi a kiegészítők felfedezését és futtatását, nyelvek lekérdezését, szabályok és verziók megtekintését.

Használat
---------

  rtg [OPCIÓK] <PARANCS> [ARGUMENTUMOK]

  Az első argumentum azonosítja a futtatandó parancsot vagy kiegészítőt.

  Példák:
    rtg image
    rtg preview
    rtg help image


Rendszerparancsok
------------------

  -h, --help        Megjeleníti ezt az általános súgót
  -v, --version     Megjeleníti az RtG-CLI verzióját
  -l, --lang        Megjeleníti az RtG-CLI elérhető nyelveit
  -r, --rules       Megjeleníti az RtG-CLI szabályait
  -c, --commands    Megjeleníti az RtG-CLI belső parancsait
  -a, --addons      Megjeleníti a felhasználó számára látható dokumentációval rendelkező kiegészítőket
  -language <nyelv>   Beállítja a kezdőképernyő (void) nyelvét

Parancs: help
--------------

  rtg help                    # Általános súgó (ez a képernyő)
  rtg help <parancs>          # Egy adott parancs/kiegészítő súgója
  rtg help <parancs> -<nyelv>   # Súgó konkrét nyelven (pl. -es, -en)
  rtg help <parancs> -lang      # Az adott parancs elérhető nyelvei

  Példák:
    rtg help image
    rtg help image -en
    rtg help image -lang


Parancs: version
-----------------

  rtg -v
  rtg --version

  Megjeleníti a verziót és a verzió tartalmát minden elérhető nyelven.


Parancs: rules
---------------

  rtg -r
  rtg --rules
  rtg -r -<nyelv>   # Szabályok konkrét nyelven (pl. rtg -r -en)

  Alapértelmezetten az 'rules'-ban definiált első nyelvet használja (spanyol).


Parancs: lang
--------------

  rtg -l
  rtg --lang

  Megjeleníti az összes elérhető nyelvet kategóriák szerint rendezve:
  Version, Rules, Help, Void, és kiegészítónként.


Parancs: commands
------------------

  rtg -c
  rtg --commands

  Kizárólag az RtG-CLI belső parancsait sorolja fel.
  Nem tartalmazza a kiegészítők parancsait.


Parancs: addons
----------------

  rtg -a
  rtg --addons

  Felsorolja a felhasználó számára látható dokumentációval/súgóval rendelkező kiegészítőket.
  Dokumentáció nélküli regisztrált kiegészítő nem jelenik meg itt.


Parancs: language
------------------

  rtg -language <nyelv>

  Kiválasztja a kezdőképernyő (void) nyelvét.
  A nyelvnek léteznie kell a 'void-language'-ben az assets.json-ban.

  Példa:
    rtg -language en


Elérhető kiegészítők
---------------------

  image      | RtG Image        - Képkonverter
  preview    | RtG Preview      - 3D nézegető RtG-Format build-ekhez
  test-addon | RtG Test Addon   - Teszt kiegészítő a CLI validálásához


Nyelvek
--------

A nyelveket egy kötőjellel jelöljük: -es, -en, -pt, stb.
A nyelv nem változtatja a belső parancsnevet.

  rtg help image -es    # Spanyol súgó
  rtg help image -en    # Angol súgó
  rtg -r -en            # Angol szabályok

  Egy kiegészítő nyelveinek megtekintéséhez:
    rtg help image -lang

  A -lang jelentése a pozíciójától függ:
    rtg --lang          # RtG-CLI nyelvek (kiegészítő előtt)
    rtg image -lang     # Kiegészítő nyelvek (kiegészítő után)


Kiegészítő argumentumok
------------------------

Egy kiegészítő azonosítása után az argumentumok az előtagjuk szerint vannak osztályozva:

  kötőjel nélküli     -> kiegészítő        (pl. convert, fájl.png)
  --opció             -> kiegészítő        (pl. --width 128)
  -opció              -> RtG-CLI           (pl. -lang, -en)

Példák:
  rtg image convert fájl.png     # convert, fájl.png -> kiegészítő
  rtg image --width 128          # --width 128 -> kiegészítő
  rtg image -lang                # -lang -> RtG-CLI (kiegészítő nyelvei)
  rtg image -en                  # -en -> RtG-CLI (nyelvválasztó)


Szóközzel rendelkező argumentumok
---------------------------------

Szóközt tartalmazó argumentumokat idézőjelek közé kell tenni:

  rtg image "én képem.png" "kimenet.json"

Az RtG-CLI megőrzi az argumentumok sorrendjét, és a kiegészítőnek átadja őket.

További információk
--------------------

  rtg help <parancs>      # Egy kiegészítő részletes súgója
  rtg help <parancs> -lang  # Az adott kiegészítő nyelvei
  rtg --addons            # Az összes dokumentált kiegészítő megtekintése
  rtg --commands          # A belső parancsok megtekintése