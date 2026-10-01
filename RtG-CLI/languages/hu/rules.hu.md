# RtG-CLI parancsszabályok

## 1. Általános struktúra

Egy RtG-CLI parancs egy főparancsból és opcionálisan argumenteiból áll.
Általános formátum:

`rtg <parancs> [<argumentumok>]`

Az `rtg` utáni első argumentum határozza meg, hogy melyik parancs vagy kiegészítő lesz végrehajtva.

Példák:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Regisztrált parancsok

A főparancsok regisztrálva kell legyenek az RtG-CLI konfigurációjában.
Egy parancs belső kulccsal azonosítható.

Példa:

`image`

Az `image` kulcs azonosítja a megfelelő kiegészítőt, függetlenül a felhasználónak megjelenített névtől.
Példa:

`image` → `RtG Image`

`preview` → `RtG Preview`

A megjelenített név nem használható parancsazonosítóként.

---

## 3. RtG-CLI parancsok és kiegészítő parancsok

Az RtG-CLI és a kiegészítők saját parancsaik és argumentumaik lehetnek.

Mielőtt egy kiegészítő azonosítva lenne, a parancsok és argumentumok az RtG-CLI-éi.
Miután egy kiegészítő azonosítva lett, az előtag határozza meg, kinek tartozik az egyes argumentumok:

- Nélkül kötőjel (`-`) → a kiegészítőhöz tartozik.
- Két kötőjel (`--`) → a kiegészítőhöz tartozik.
- Egy kötőjel (`-`) → az RtG-CLI-hez tartozik.

Példa:

`rtg image convert`

- `image` → kiegészítő.
- `convert` → kiegészítő parancs.

Példa:

`rtg image --width 128`

- `image` → kiegészítő.
- `--width` → kiegészítő argumentum.
- `128` → kiegészítő argumentum értéke.

Példa:

`rtg image -lang`

- `image` → kiegészítő.
- `-lang` → RtG-CLI argumentum.

---

## 4. Rendszerargumentumok

Mielőtt egy kiegészítő azonosítva lenne, az RtG-CLI a saját szintaxis-szabályait használja.
A hosszú rendszeropciók két kötőjelt használnak:

`rtg --version`
`rtg --help`

A rendszerrovatok egy kötőjelt használnak:

`rtg -v`
`rtg -h`
`rtg -l`

Miután egy kiegészítő azonosítva lett, egyetlen kötőjellel (`-`) kezdődő opció az RtG-CLI-hez tartozik.

Példa:

`rtg image -lang`
`rtg image -en`

---

## 5. Argumentumok a kiegészítő előtt és után

Az RtG-CLI argumentumainak eltérő jelentésük lehet attól függően, hogy a kiegészítő azonosítása előtt vagy után kerülnek.

Mielőtt egy kiegészítő azonosítva lenne, az argumentumok az RtG-CLI-hez tartoznak.

Például:

`rtg --lang`

Megjeleníti az RtG-CLI számára elérhető nyelveket.

Miután egy kiegészítő azonosítva lett, az argumentumok a kiegészítőkhoz rendelt tulajdonosi szabályok szerint kerülnek értelmezésre.

Például:

`rtg image -lang`

Lekérdezi az `image` kiegészítőhöz elérhető nyelveket.

Így az argumentum pozíciója meghatározza a kontextusát, és megakadályozza, hogy a globális RtG-CLI argumentumok összekeveredjenek a kiegészítő azonosítása után használt argumentumokkal.

---

## 6. A rendszerargumentumok pozíciója

A rendszerargumentumok nem szabad, hogy a hozzájuk tartozó parancs vagy kiegészítő előtt szerepeljenek, ha az argumentum attól a parancstól függ.

Helyes példa:

`rtg help image -en`

Helytelen példa:

`rtg help -en image`

Ezekben a két példában a `help` rendszerparancs ezt a struktúrát használja, ezért a második példa helytelen:
`help <target> <options>`

A pozíciónak meg kell engednie, hogy egyértelműen meghatározzuk, melyik parancs kapja az argumentumot.

---

## 7. Kiegészítő parancsok és argumentumok

A parancsok külön terminál-argumentumként írandók.
Egy parancs nem tartalmazhat szóközt, hacsak nem idézőjelek között van.

A további argumentumok a kiegészítő saját felületére szerint használhatók.

Például:

`rtg image convert image`

értelmezhető úgy:

- `image` → kiegészítő
- `convert` → kiegészítő parancs
- `image` → parancs argumentum

---

## 8. Kötőjelek használata kiegészítő parancsokban

Egy kiegészítő azonosítása után:

- Kötőjel nélküli argumentumok a kiegészítőhöz tartoznak.
- Két vagy több kötőjeles (`--`) argumentumok a kiegészítőhöz tartoznak.
- Egyetlen kötőjeles (`-`) argumentumok az RtG-CLI-hez tartoznak.

Példák:

`rtg image convert`
`convert` → kiegészítő.

`rtg image --width 128`
`--width` → kiegészítő.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Kiegészítő parancs felület

Egy kiegészítő specifikus parancsai a kiegészítő programja határozza meg.
Az RtG-CLI a kiegészítő konfigurációját használja a parancsfelület lokalizálására a `program commands` tulajdonson keresztül.

Ez a tulajdonság tartalmazza a program parancsfelületét biztosító fájlok elérési útjait.

Példa:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

Az RtG-CLI használhatja ezt a felületet a kiegészítő elérhető parancsainak feltárására vagy végrehajtására, de nem feltételezheti és nem módosíthatja a belső parancsok jelentését.

Egy kiegészítő meghatározhat további parancsokat, amelyek nem regisztráltak közvetlenül RtG-CLI parancsokként.

A program belső implementációja eltérhet a kiegészítők között, amíg RtG-CLI szabályokkal kompatibilis felületet biztosít.

---

## 10. Nyelvek

Egy kiegészítő elérhető nyelvei a konfigurációján keresztül definiálhatók.

Példa:

`lang: ["es", "en"]`

A lefordított teksts a megfelelő nyelvkód használatával azonosíthatók.

Példa:

`content.hu`
`content.en`

Az RtG-CLI által használt nyelvválasztót rendszereargumentumként kell kezelni.

Példa:

`rtg help image -en`

---

## 11. Alapértelmezett nyelv

Ha `-<nyelv>` nincs megadva, az RtG-CLI az `rules`-ban definiált első nyelvet használja.
Ha `-<nyelv>` meg van adva, az RtG-CLI azt a nyelvet használja, ha elérhető.

Az `assets.json` `rules` objektumában definiált első nyelv az alapértelmezett nyelv a szabályokhoz.

Amikor a felhasználó nyelv megadása nélkül kéri a szabályokat, az RtG-CLI az első nyelvet kell használja.

Például:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

Ebben az esetben:

`rtg -r`
és
`rtg --rules`

spanyolul fogják megjeleníteni a szabályokat, mert `es` az első definiált nyelv.
Egy másik nyelv kéréséhez a hozzá tartozó választót kell használni:

`rtg -r -en`

A nyelvek sorrendje az `rules` objektumban kizárólag azt határozza meg, melyik lesz az alapértelmezett. Nem változtatja a rendelkezésre álló nyelveket.

Ez a szabály más nyelvválasztókra is vonatkozik, mint:

`rtg help image -es`

---

## 12. A nyelv nem változtatja a parancsot

A nyelv megváltoztatása csupán az RtG-CLI által megjelenített szöveget módosítja.
Nem változtatja a belső parancsnevet.

Példa:

`rtg help image -es`

és

`rtg help image -en`

még mindig ugyanarra a parancsra hivatkoznak:

`image`

---

## 13. Súgó

Az általános súgó a következővel kérhető le:

`rtg help`

Egy specifikus parancs súgója a következővel kérhető le:

`rtg help <parancs>`

A súgó kérehető egy specifikus nyelven:

`rtg help <parancs> -<nyelv>`

Példa:

`rtg help image -en`

---

## 14. Nyelvlekérdezés

Egy kiegészítő elérhető nyelvei a következővel kérdezhetők le:

`rtg help <parancs> -lang`

Példa:

`rtg help image -lang`

Ez az opció az RtG-CLI-hez tartozik, nem a kiegészítőhöz.

---

## 15. A kiegészítők nem módosíthatják a rendszer szabályait

Egy kiegészítő definiálhat saját parancsokat és argumentumokat, de nem határozhatja át az RtG-CLI számára fenntartott argumentumok jelentését.

Például egy kiegészítő nem használhatja a `-t` opciót a rendszer súgójának más jelentésének adására.
Az RtG-CLI számára fenntartott nevek elsőbbséggel rendelkeznek a kiegészítő parancsok felett.
Az RtG-CLI számára fenntartott parancsok és opciók explicit módon definiálódnak a CLI felületen.
Egy kiegészítő nem definiálhatja újra egy fenntartott opció viselkedését.

---

## 16. Azonosító és név elválasztása

A kiegészítő belső kulcsa szolgál azonosításra.
A kiegészítő neve csupán leíró információként vagy a felhasználónak való megjelenítésre szolgál.

Példa:

`image` → belső azonosító

`RtG Image` → megjelenített név

Nem feltételezhető, hogy a megjelenített név parancsként használható.

---

## 17. A parancsok determinisztikuskell legyenek

Az RtG-CLI képesnek kell lennie arra, hogy az argumentum a rendszerhez vagy a kiegészítőhöz tartozik-e anélkül, hogy a program leíró nevére támaszkodna.

Az értelmezés a parancs struktúráján és szabályain alapulnia kell.

Példa:

`rtg help image -en`

mindig ugyanúgy kell értelmezni:

`rtg` → CLI

`help` → CLI parancs

`image` → kiegészítő

`-en` → CLI opció

---

## 18. Ismeretlen argumentumok

Egy kiegészítő azonosítása után az RtG-CLI az egyes argumentumok tulajdonát az előtagjuk alapján határozza meg.

* Kötőjel nélküli argumentum a kiegészítőhöz tartozik.
* Két vagy több kötőjeles (`--`) argumentum a kiegészítőhöz tartozik.
* Egyetlen kötőjeles (`-`) argumentum az RtG-CLI-hez tartozik.

Ha az RtG-CLI ismeretlen rendszerargumentumot kap, jeleznie kell, hogy az opció nem létezik.

A kiegészítő argumentumait át kell adni a kiegészítőnek anélkül, hogy az RtG-CLI megpróbálná értelmezni azok jelentését.

---

## 19. Nem regisztrált parancsok ne feltételezve

Az RtG-CLI nem tekintheti érvényesnek egy parancsot csupán azért, mert egy kapcsolódó mappa, fájl vagy program létezik.

A parancs a megfelelő konfigurációban definiálva kell legyen.

---

## 20. Kompatibilitás

A kiegészítők az RtG-CLI szintaxis-szabályait követik kell a helyes integráció érdekében.
Egy kiegészítő teljesen eltérő belső implementációval rendelkezhet, de a parancsfelülete az RtG-CLI által kialakított szabályokat kell követnie.

---

## 21. Prioritási szabály

Egy kiegészítő azonosítása után egyetlen kötőjel (`-`) az RtG-CLI számára van fenntartva.
Egy kiegészítő nem használhat egyetlen kötőjellel kezdődő argumentumokat.
Két vagy több kötőjellel (`--`) kezdődő vagy kötőjellel nem kezdődő argumentumok a kiegészítőhöz tartoznak.

---

## 22. Kiegészítő argumentumok

Miután a kiegészítő azonosítva lett, az RtG-CLI nem feltétezheti a kiegészítő-specifikus argumentumok jelentését.

A kiegészítőhöz tartozó argumentumokat át kell adni a kiegészítő programjának a feldolgozásra.

Példa:

`rtg image --width 128`

Az RtG-CLI az `image`-ot kiegészítőként azonosítja.

`--width 128` az RtG Image felületéhez tartozik, és az adott kiegészítőnek kell feldolgoznia.

---

## 23. Szóközzel rendelkező argumentumok

Szóközt tartalmazó argumentumokat idézőjelek közé kell tenni, hogy a terminál egyetlen argumentumként kezelje őket.

Példa:

`rtg image "C:\Users\User\Downloads\én képem.png" "C:\Users\User\Downloads\kimenet.json"`

A teljes útvonalat egyetlen argumentumként kell fogadni.

---

## 24. A kiegészítő argumentumainak megőrzése

Az RtG-CLI nem módosíthatja, nem távolíthatja el, és nem értelmezheti újra a kiegészítőnek szánt argumentumokat, hacsak egy explicit rendszer szabály nem írja elő mást.

Az argumentumokat a felhasználó által megadott sorrendben kell átadni a kiegészítőnek.

---

## 25. Teljes példák

Kiegészítő parancs:

`rtg image`

Súgó:

`rtg help image`

Angol súgó:

`rtg help image -en`

Nyelvlekérdezés:

`rtg help image -lang`

CLI verzió:

`rtg --version`

CLI súgó:

`rtg --help`

Egy kiegészítő-specifikus opció:

`rtg image --width 128`

Egy kiegészítő-specifikus opció értékkel:

`rtg image --output file.json`

Egy kombináció:

`rtg image image.png --output output.json`

Ebben a példában:

* `image` azonosítja a kiegészítőt.
* `image.png` egy kiegészítő argumentum.
* `--output` egy kiegészítő opció.
* `output.json` az opció értéke.
* Egyik argumentum sem értelmezhető rendszer opcióként.

---

## 26. Kezdőképernyő szövege nyelve

`rtg -language <nyelv>` kiválasztja az RtG-CLI által megjelenített kezdőképernyő (void) nyelvét.

A nyelvnek a `void-language` ban kell lennie.

Példa:

`rtg -language hu`

megjeleníti a szöveget, ami definiálva van a:

`void-language.hu`

Ha `-language` nincs megadva, az RtG-CLI a `void` ot használja.

Ha a kért nyelv nem elérhető, az RtG-CLI jeleznie kell, hogy a nyelv nem elérhető.