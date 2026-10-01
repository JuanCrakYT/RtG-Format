# RtG-CLI Komut Kuralları

## 1. Genel Yapı

RtG-CLI komutu bir ana komuttan ve isteğe bağlı argümanlardan oluşur.
Genel format:

`rtg <komut> [<argümanlar>]`

`rtg` dan sonraki ilk argüman, hangi komut veya eklentinin çalıştırılacağını belirler.

Örnekler:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Kayıtlı Komutlar

Ana komutlar RtG-CLI yapılandırmasında kayıtlı olmalıdır.
Bir komut dahili anahtarı ile tanımlanır.

Örnek:

`image`

`image` anahtarı, kullanıcıya gösterilen isimden bağımsız olarak ilgili eklentiyi tanımlar.
Örnek:

`image` → `RtG Image`

`preview` → `RtG Preview`

Görüntülenen isim komut tanımlayıcısı olarak kullanılmamalıdır.

---

## 3. RtG-CLI Komutları ve Eklenti Komutları

RtG-CLI ve eklentilerin kendi komut ve argümanları olabilir.

Bir eklenti tanımlandığı öncesinde, komut ve argümanlar RtG-CLI'ya aittir.
Bir eklenti tanımlandıktan sonra, önek her argümanın kime ait olduğunu belirler:

- Tire yok (`-`) → eklentiye aittir.
- Çift tire (`--`) → eklentiye aittir.
- Tek tire (`-`) → RtG-CLI'ya aittir.

Örnek:

`rtg image convert`

- `image` → eklenti.
- `convert` → eklenti komutu.

Örnek:

`rtg image --width 128`

- `image` → eklenti.
- `--width` → eklenti argümanı.
- `128` → eklenti argümanının değeri.

Örnek:

`rtg image -lang`

- `image` → eklenti.
- `-lang` → RtG-CLI argümanı.

---

## 4. Sistem Argümanları

Bir eklenti tanımlandığı öncesinde, RtG-CLI kendi sözdizimi kurallarını kullanır.
Uzun sistem seçenekleri çift tire kullanır:

`rtg --version`
`rtg --help`

Sistem kısaltmaları tek tire kullanır:

`rtg -v`
`rtg -h`
`rtg -l`

Bir eklenti tanımlandıktan sonra, tek bir tire (`-`) ile başlayan bir seçenek RtG-CLI'ya aittir.

Örnek:

`rtg image -lang`
`rtg image -en`

---

## 5. Eklenti Öncesi ve Sonrası Argümanlar

RtG-CLI argümanları, eklenti tanımlandığı öncesinde veya sonrasında olup olmadıklarına göre farklı anlamlara gelebilir.

Bir eklenti tanımlandığı öncesinde, argümanlar RtG-CLI'ya aittir.

Örneğin:

`rtg --lang`

RtG-CLI için kullanılabilir dilleri gösterir.

Bir eklenti tanımlandıktan sonra, argümanlar eklentiler için kurulan sahip olma kurallarına göre yorumlanır.

Örneğin:

`rtg image -lang`

`image` eklentisi için kullanılabilir dilleri sorgular.

Bu şekilde, argümanın konumu bağlamını belirler ve küresel RtG-CLI argümanlarının, bir eklenti tanımlandıktan sonra kullanılan argümanlarla karıştırılmasını önler.

---

## 6. Sistem Argümanlarının Pozisyonu

Sistem argümanları, etki ettikleri komut veya eklentinin önünde görünmemelidir, eğer argüman o komuta bağlıysa.

Doğru örnek:

`rtg help image -en`

Yanlış örnek:

`rtg help -en image`

Bu iki örnekte, sistem komutu `help` bu yapıyı kullanır, bu yüzden ikinci örnek yanlıştır:
`help <target> <options>`

Pozisyon, hangi komutun argümanı alacağını net bir şekilde belirlemelidir.

---

## 7. Eklenti Komutları ve Argümanları

Komutlar tek tek terminal argümanları olarak yazılır.
Bir komut tırnak işaretleri içinde olmadığı sürece boşluk içermemelidir.

Aşağıdaki argümanlar eklentinin kendi arayüzüne göre kullanılabilir.

Örneğin:

`rtg image convert image`

şu şekilde yorumlanabilir:

- `image` → eklenti
- `convert` → eklenti komutu
- `image` → komut argümanı

---

## 8. Eklenti Komutlarında Tire Kullanımı

Bir eklenti tanımlandıktan sonra:

- Tiresiz argümanlar eklentiye aittir.
- İki veya daha fazla tireli (`--`) argümanlar eklentiye aittir.
- Tek tireli (`-`) argümanlar RtG-CLI'ya aittir.

Örnekler:

`rtg image convert`
`convert` → eklenti.

`rtg image --width 128`
`--width` → eklenti.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Eklenti Komut Arayüzü

Bir eklentiye özgü komutlar, eklenti programı tarafından tanımlanır.
RtG-CLI, eklenti yapılandırmasını `program commands` özelliği aracılığıyla komut arayüzünü bulmak için kullanır.

Bu özellik, programın komut arayüzünü sağlayan dosyaların yollarını içerir.

Örnek:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI, bu arayüzü eklentinin kullanılabilir komutlarını keşfetmek veya çalıştırmak için kullanabilir, ancak iç komutların anlamını varsaymamalı veya değiştirmemelidir.

Bir eklenti, RtG-CLI komutları olarak doğrudan kayıtlı olmayan ek komutlar tanımlayabilir.

Programın dahili uygulaması eklentiler arasında farklı olabilir, RtG-CLI kurallarıyla uyumlu bir arayüz sağladığı sürece.

---

## 10. Diller

Bir eklenti için kullanılabilir diller yapılandırması üzerinden tanımlanır.

Örnek:

`lang: ["es", "en"]`

Çevrilmiş metinler karşılık gelen dil kodu ile tanımlanır.

Örnek:

`content.tr`
`content.en`

RtG-CLI tarafından kullanılan dil seçici bir sistem argümanı olarak kabul edilmelidir.

Örnek:

`rtg help image -en`

---

## 11. Varsayılan Dil

`-<dil>` belirtilmezse, RtG-CLI `rules` içinde tanımlanan ilk dili kullanır.
`-<dil>` belirtilirse, RtG-CLI bu dili kullanılabilirse kullanır.

`assets.json` dosyasındaki `rules` nesnesinde tanımlanan ilk dil, kurallar için varsayılan dildir.

Kullanıcı dil belirtmeden kuralları istediğinde, RtG-CLI o ilk dili kullanmalıdır.

Örneğin:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

Bu durumda:

`rtg -r`
ve
`rtg --rules`

`es` ilk tanımlanan dil olduğu için kuralları İspanyolca gösterir.
Başka bir dil istemek için karşılık gelen seçici kullanılmalıdır:

`rtg -r -en`

`rules` içindeki dil sıralaması sadece hangi dilin varsayılan olacağını belirler. Kullanılabilir dilleri değiştirmez.

Bu kural şu gibi diğer dil seçicileri için de geçerlidir:

`rtg help image -es`

---

## 12. Dil Komutu Değiştirmez

Dili değiştirmek sadece RtG-CLI tarafından gösterilen metni değiştirir.
Dahili komut adını değiştirmez.

Örnek:

`rtg help image -es`

ve

`rtg help image -en`

hala aynı komuta atıfta bulunur:

`image`

---

## 13. Yardım

Genel yardım şu ile alınır:

`rtg help`

Belirli bir komut için yardım şu ile alınır:

`rtg help <komut>`

Yardım belirli bir dilde istenebilir:

`rtg help <komut> -<dil>`

Örnek:

`rtg help image -en`

---

## 14. Dil Sorgulama

Bir eklenti için kullanılabilir diller şu ile sorgulanabilir:

`rtg help <komut> -lang`

Örnek:

`rtg help image -lang`

Bu seçenek RtG-CLI'ya aittir, eklentiye değil.

---

## 15. Eklentiler Sistem Kurallarını Değiştirmemelidir

Bir eklenti kendi komut ve argümanlarını tanımlayabilir, ancak RtG-CLI tarafından ayrılan argümanların anlamını yeniden tanımlayamaz.

Örneğin, bir eklenti sistem yardımına farklı anlam vermek için `-h` kullanmamalıdır.
RtG-CLI tarafından ayrılan isimler eklenti komutları üzerinde önceliğe sahiptir.
RtG-CLI tarafından ayrılan komut ve seçenekler CLI arayüzü tarafından açıkça tanımlanmalıdır.
Bir eklenti ayrılmış bir seçeneğin davranışını yeniden tanımlayamaz.

---

## 16. Tanımlayıcı ve İsim Arasındaki Ayrım

Bir eklentinin dahili anahtarı onu tanımlamak için kullanılır.
Eklenti ismi sadece açıklayıcı bilgi veya kullanıcıya göstermek için kullanılır.

Örnek:

`image` → dahili tanımlayıcı

`RtG Image` → görüntülenen isim

Görüntülenen ismin komut olarak kullanılabileceği varsayılmamalıdır.

---

## 17. Komutlar Deterministik Olmalıdır

RtG-CLI, bir argümanın sisteme mi yoksa eklentiye mi ait olduğunu, programın açıklayıcı adına bağımlı olmadan belirleyebilmelidir.

Yorumlama komut yapısı ve kuralları temel alınmalıdır.

Örnek:

`rtg help image -en`

her zaman aynı şekilde yorumlanmalıdır:

`rtg` → CLI

`help` → CLI komutu

`image` → eklenti

`-en` → CLI seçeneği

---

## 18. Bilinmeyen Argümanlar

Bir eklenti tanımlandıktan sonra, RtG-CLI her argümanın sahipliğini önekine göre belirlemelidir.

* Tiresiz bir argüman eklentiye aittir.
* İki veya daha fazla tireli (`--`) bir argüman eklentiye aittir.
* Tek tireli (`-`) bir argüman RtG-CLI'ya aittir.

RtG-CLI tanımadığı bir sistem argümanı alırsa, seçeneğin mevcut olmadığını bildirmelidir.

Eklenti argümanları, RtG-CLI anlamlarını yorumlamaya çalışmadan eklentiye iletilmelidir.

---

## 19. Kayıtlı Olmayan Komutları Varsaymamak

RtG-CLI, ilgili bir klasör, dosya veya programın varlığı sebebiyle bir komutu geçerli saymamalıdır.

Komut karşılık gelen yapılandırmada tanımlanmalıdır.

---

## 20. Uyumluluk

Eklentiler RtG-CLI sözdizimi kurallarını uygun entegrasyon için takip etmelidir.
Bir eklentinin tamamen farklı bir dahili uygulaması olabilir, ancak komut arayüzü RtG-CLI tarafından kurulmuş kuralları takip etmelidir.

---

## 21. Öncelik Kuralı

Bir eklenti tanımlandıktan sonra, tek bir tire (`-`) RtG-CLI için ayrılmıştır.
Bir eklenti tek tire ile başlayan argümanları kullanamaz.
İki veya daha fazla tire (`--`) ile başlayan veya tire ile başlamayan argümanlar eklentiye aittir.

---

## 22. Eklenti Argümanları

Bir eklenti tanımlandıktan sonra, RtG-CLI eklentiye özgü argümanların anlamını varsaymamalıdır.

Eklentiye ait argümanlar, eklenti programına işlenmek üzere iletilmelidir.

Örnek:

`rtg image --width 128`

RtG-CLI `image` yi eklenti olarak tanımlar.

`--width 128` RtG Image arayüzüne karşılık gelir ve belirtilen eklenti tarafından işlenmelidir.

---

## 23. Boşluk İçeren Argümanlar

Boşluk içeren argümanlar, terminallerin onları tek bir argüman olarak kabul etmesi için tırnak içine yazılmalıdır.

Örnek:

`rtg image "C:\Users\User\Downloads\benim resmim.png" "C:\Users\User\Downloads\cikti.json"`

Tam yol tek bir argüman olarak alınmalıdır.

---

## 24. Eklenti Argümanları Korunmalıdır

Açık bir sistem kuralı belirtmediği sürece, RtG-CLI eklentiye yönelik argümanları değiştirmemeli, silmemeli veya yeniden yorumlamamalıdır.

Argümanlar kullanıcı tarafından sağlandıkları sırada eklentiye teslim edilmelidir.

---

## 25. Tam Örnekler

Eklenti komutu:

`rtg image`

Yardım:

`rtg help image`

İngilizce yardım:

`rtg help image -en`

Dil sorgulama:

`rtg help image -lang`

CLI sürümü:

`rtg --version`

CLI yardım:

`rtg --help`

Eklentiye özgü bir seçenek:

`rtg image --width 128`

Değeri olan eklentiye özgü bir seçenek:

`rtg image --output dosya.json`

Bir kombinasyon:

`rtg image dosya.png --output cikti.json`

Bu örnekte:

* `image` eklentiyi tanımlar.
* `dosya.png` bir eklenti argümanıdır.
* `--output` bir eklenti seçeneğidir.
* `cikti.json` o seçeneğin değeridir.
* Bu argümanların hiçbiri sistem seçeneği olarak yorumlanmamalıdır.

---

## 26. Başlangıç Metni Dili

`rtg -language <dil>` RtG-CLI tarafından görüntülenen başlangıç (void) metninin dilini seçer.

Dil `void-language` içinde bulunmalıdır.

Örnek:

`rtg -language tr`

şu içinde tanımlanan metni gösterir:

`void-language.tr`

`-language` belirtilmezse, RtG-CLI `void` kullanır.

İstenen dil mevcut değilse, RtG-CLI o dilin mevcut olmadığını bildirmelidir.