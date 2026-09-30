# Pravidla příkazů RtG-CLI

## 1. Obecná struktura

Příkaz RtG-CLI se skládá z hlavního příkazu a volitelně argumentů.
Obecný formát:

`rtg <příkaz> [<argumenty>]`

První argument za `rtg` určuje, který příkaz nebo doplněk se provede.

Příklady:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Zaregistrované příkazy

Hlavní příkazy musí být zaregistrované v konfiguraci RtG-CLI.
Příkaz je identifikován svým interním klíčem.

Příklad:

`image`

Klíč `image` identifikuje odpovídající doplněk, nezávisle na názvu zobrazeném uživateli.
Příklad:

`image` → `RtG Image`

`preview` → `RtG Preview`

Zobrazený název nesmí být použit jako identifikátor příkazu.

---

## 3. Příkazy RtG-CLI a příkazy doplňků

RtG-CLI a doplňky mohou mít své vlastní příkazy a argumenty.

Před identifikací doplňku patří příkazy a argumenty RtG-CLI.
Po identifikaci doplňku předpona určuje, komu každý argument patří:

- Bez spojovníku (`-`) → patří doplňku.
- Dva spojovníky (`--`) → patří doplňku.
- Jeden spojovník (`-`) → patří RtG-CLI.

Příklad:

`rtg image convert`

- `image` → doplněk.
- `convert` → příkaz doplňku.

Příklad:

`rtg image --width 128`

- `image` → doplněk.
- `--width` → argument doplňku.
- `128` → hodnota argumentu doplňku.

Příklad:

`rtg image -lang`

- `image` → doplněk.
- `-lang` → argument RtG-CLI.

---

## 4. Systémové argumenty

Před identifikací doplňku RtG-CLI používá vlastní syntaktická pravidla.
Dlouhé systémové volby používají dva spojovníky:

`rtg --version`
`rtg --help`

Systémové zkratky používají jeden spojovník:

`rtg -v`
`rtg -h`
`rtg -l`

Po identifikaci doplňku należy volba začínající jedním spojovníkem (`-`) k RtG-CLI.

Příklad:

`rtg image -lang`
`rtg image -en`

---

## 5. Argumenty před a po doplňku

Argumenty RtG-CLI mohou mít jiný význam v závislosti na tom, zda se objevují před nebo po identifikaci doplňku.

Před identifikací doplňku patří argumenty RtG-CLI.

Například:

`rtg --lang`

Zobrazuje dostupné jazyky pro RtG-CLI.

Po identifikaci doplňku jsou argumenty interpretovány podle pravidel vlastnictví stanovených pro doplňky.

Například:

`rtg image -lang`

Dotazuje se na dostupné jazyky pro doplněk `image`.

Tímto způsobem poloha argumentu určuje jeho kontext a zabraňuje záměně globálních argumentů RtG-CLI s argumenty používanými po identifikaci doplňku.

---

## 6. Pozice systémových argumentů

Systémové argumenty by neměly objevovat před příkazem nebo doplňkem, na který ovlivňují, když argument závisí na tom příkazu.

Správný příklad:

`rtg help image -en`

Špatný příklad:

`rtg help -en image`

V těchto dvou příkladech systémový příkaz `help` používá tuto strukturu, proto je druhý příklad nesprávný:
`help <target> <options>`

Pozice musí jasně určovat, který příkaz dostane argument.

---

## 7. Příkazy a argumenty doplňků

Příkazy se zapisují jako jednotlivé terminálové argumenty.
Příkaz by neměl obsahovat mezery, pokud není v uvozovkách.

Následující argumenty mohou být použity doplňkem podle jeho vlastního rozhraní.

Například:

`rtg image convert image`

může být interpretováno jako:

- `image` → doplněk
- `convert` → příkaz doplňku
- `image` → argument příkazu

---

## 8. Použití spojovníků v příkazech doplňků

Po identifikaci doplňku:

- Argumenty bez spojovníku patří doplňku.
- Argumenty se dvěma nebo více spojovníky (`--`) patří doplňku.
- Argumenty s jedním spojovníkem (`-`) patří RtG-CLI.

Příklady:

`rtg image convert`
`convert` → doplněk.

`rtg image --width 128`
`--width` → doplněk.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Rozhraní příkazů doplňků

Konkrétní příkazy doplňku jsou definovány samotným programem doplňku.
RtG-CLI používá konfiguraci doplňku k nalezení jeho rozhraní příkazů přes vlastnost `program commands`.

Tato vlastnost obsahuje cesty k souborům, které poskytují rozhraní příkazů programu.

Příklad:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI může toto rozhraní použít k zjištění nebo spuštění příkazů dostupných pro doplněk, ale neměl by předpokládat ani měnit význam jeho vnitřních příkazů.

Doplněk může definovat další příkazy, které nejsou registrovány přímo jako příkazy RtG-CLI.

Vnitřní implementace programu se může lišit mezi doplňky, pokud poskytuje rozhraní kompatibilní s pravidly RtG-CLI.

---

## 10. Jazyky

Dostupné jazyky pro doplněk jsou definovány přes jeho konfiguraci.

Příklad:

`lang: ["es", "en"]`

Přeložené texty jsou identifikovány příslušným kódem jazyka.

Příklad:

`content.cs`
`content.en`

Selektor jazyka používaný RtG-CLI musí být považován za systémový argument.

Příklad:

`rtg help image -en`

---

## 11. Výchozí jazyk

Pokud `-<jazyk>` není specifikován, RtG-CLI použije první jazyk definovaný v `rules`.
Pokud `-<jazyk>` je specifikován, RtG-CLI použije ten jazyk, pokud je dostupný.

První jazyk definovaný v objektu `rules` souboru `assets.json` je výchozím jazykem pro pravidla.

Když uživatel požádá o pravidla bez specifikace jazyka, RtG-CLI musí použít ten první jazyk.

Například:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

V tomto případě:

`rtg -r`
a
`rtg --rules`

zobrazí pravidla v španělštině, protože `es` je první definovaný jazyk.
Pro požadavek jiného jazyka musí být použit jeho odpovídající selektor:

`rtg -r -en`

Pořadí jazyků uvnitř `rules` určuje pouze výchozí jazyk. Nemění dostupné jazyky.

Toto pravidlo platí také pro další selektory jazyka, jako:

`rtg help image -es`

---

## 12. Jazyk nemění příkaz

Změna jazyka mění pouze text zobrazený RtG-CLI.
Nemění interní název příkazu.

Příklad:

`rtg help image -es`

a

`rtg help image -en`

stále odkazují na stejný příkaz:

`image`

---

## 13. Nápověda

Obecná nápověda se získá:

`rtg help`

Nápověda pro konkrétní příkaz se získá:

`rtg help <příkaz>`

Nápověda může být požadována v konkrétním jazyce:

`rtg help <příkaz> -<jazyk>`

Příklad:

`rtg help image -en`

---

## 14. Dotaz na jazyky

Dostupné jazyky pro doplněk lze dotázat:

`rtg help <příkaz> -lang`

Příklad:

`rtg help image -lang`

Tato volba patří RtG-CLI, ne doplňku.

---

## 15. Doplňky nemějí měnit systémová pravidla

Doplněk může definovat vlastní příkazy a argumenty, ale nemůže předefinovat význam argumentů rezervovaných RtG-CLI.

Například doplněk by neměl používat `-h` pro jiný význam systémové nápovědy.
Názvy rezervované RtG-CLI mají prioritu nad příkazy doplňků.
Příkazy a volby rezervované RtG-CLI musí být explicitně definovány rozhraním CLI.
Doplněk nemůže předefinovat chování rezervované volby.

---

## 16. Rozlišení mezi identifikátorem a názvem

Interní klíč doplňku se používá k jeho identifikaci.
Název doplňku se používá pouze jako popisná informace nebo pro zobrazení uživateli.

Příklad:

`image` → interní identifikátor

`RtG Image` → zobrazený název

Nelze předpokládat, že zobrazený název může být použit jako příkaz.

---

## 17. Příkazy musí být deterministické

RtG-CLI musí být schopen určit, zda argument patří systému nebo doplňku, bez závislosti na popisném názvu programu.

Interpretace musí být založena na struktuře a pravidlech příkazu.

Příklad:

`rtg help image -en`

musí být vždy interpretován stejným způsobem:

`rtg` → CLI

`help` → příkaz CLI

`image` → doplněk

`-en` → volba CLI

---

## 18. Neznámé argumenty

Po identifikaci doplňku musí RtG-CLI určit vlastnictví každého argumentu podle jeho předpony.

* Argument bez spojovníku patří doplňku.
* Argument se dvěma nebo více spojovníky (`--`) patří doplňku.
* Argument s jedním spojovníkem (`-`) patří RtG-CLI.

Pokud RtG-CLI obdrží neznámý systémový argument, musí oznámit, že volba neexistuje.

Argumenty doplňku musí být předány doplňku bez pokusu RtG-CLI o interpretaci jejich významu.

---

## 19. Nepředpokládat nezaregistrované příkazy

RtG-CLI by neměl považovat příkaz za platný jen proto, že existuje související složka, soubor nebo program.

Příkaz musí být definován v odpovídající konfiguraci.

---

## 20. Kompatibilita

Doplňky musí dodržovat syntaktická pravidla RtG-CLI pro správnou integraci.
Doplněk může mít zcela odlišnou interní implementaci, ale jeho rozhraní příkazů musí dodržovat pravidla stanovená RtG-CLI.

---

## 21. Pravidlo priority

Po identifikaci doplňku je jeden spojovník (`-`) rezervován pro RtG-CLI.
Doplněk nemůže používat argumenty začínající jedním spojovníkem.
Argumenty začínající dvěma nebo více spojovníky (`--`) nebo nezačínající spojovníkem patří doplňku.

---

## 22. Argumenty doplňku

Po identifikaci doplňku by RtG-CLI neměl předpokládat význam argumentů specifických pro doplněk.

Argumenty patřící doplňku musí být předány programu doplňku pro zpracování.

Příklad:

`rtg image --width 128`

RtG-CLI identifikuje `image` jako doplněk.

`--width 128` odpovídá rozhraní RtG Image a musí být zpracováno tímto doplňkem.

---

## 23. Argumenty s mezerami

Argumenty obsahující mezery musí být zapsány v uvozovkách, aby terminál bral jako jeden argument.

Příklad:

`rtg image "C:\Users\User\Downloads\můj obrázek.png" "C:\Users\User\Downloads\výstup.json"`

Celá cesta musí být přijata jako jeden argument.

---

## 24. Argumenty doplňku musí být zachovány

RtG-CLI by neměl modifikovat, odebírat ani přepovídat argumenty určené pro doplněk, pokud to explicitní systémové pravidlo neuvádí jinak.

Argumenty musí být doručeny doplňku v pořadí, v jakém byly uživatelem zadány.

---

## 25. Kompletní příklady

Příkaz doplňku:

`rtg image`

Nápověda:

`rtg help image`

Nápověda v angličtině:

`rtg help image -en`

Dotaz na jazyky:

`rtg help image -lang`

Verze CLI:

`rtg --version`

Nápověda CLI:

`rtg --help`

Volba specifická pro doplněk:

`rtg image --width 128`

Volba specifická pro doplněk s hodnotou:

`rtg image --output soubor.json`

Kombinace:

`rtg image soubor.png --output výstup.json`

V tomto příkladu:

* `image` identifikuje doplněk.
* `soubor.png` je argument doplňku.
* `--output` je volba doplňku.
* `výstup.json` je hodnota té volby.
* Žádný z těchto argumentů by neměl být interpretován jako systémová volba.

---

## 26. Jazyk úvodního textu

`rtg -language <jazyk>` vybírá jazyk úvodního textu (void) zobrazeného RtG-CLI.

Jazyk musí existovat uvnitř `void-language`.

Příklad:

`rtg -language cs`

zobrazí text definovaný v:

`void-language.cs`

Pokud `-language` není specifikován, RtG-CLI používá `void`.

Pokud požadovaný jazyk není dostupný, RtG-CLI musí oznámit, že jazyk není dostupný.