RtG-CLI — Yardım
=================

RtG-CLI, RtG-Format ekosistemi için komut satırı arayüzüdür.
Eklentilerin keşfi ve çalıştırılması, dillerin sorgulanması, kuralların ve sürümün görüntülenmesini sağlar.

Kullanım
---------

  rtg [SEÇENEKLER] <KOMUT> [ARGÜMANLAR]

  İlk argüman, çalıştırılacak komutu veya eklentiyi tanımlar.

  Örnekler:
    rtg image
    rtg preview
    rtg help image


Sistem Komutları
-----------------

  -h, --help        Bu genel yardımı gösterir
  -v, --version     RtG-CLI sürümünü gösterir
  -l, --lang        RtG-CLI'daki kullanılabilir dilleri listeler
  -r, --rules       RtG-CLI kurallarını gösterir
  -c, --commands    RtG-CLI dahili komutlarını listeler
  -a, --addons      Kullanıcıdan görünür belgeye sahip eklentileri listeler
  -u, --usage       Genel kullanım bilgisini gösterir (yeni)
  -u-<dil>          Belirli dilde kullanım gösterir (örn: -u-es, -u-en) (yeni)
  --usage-<dil>     Belirli dilde kullanım gösterir (örn: --usage-es, --usage-en) (yeni)
  -language <dil>     Başlangıç metni (void) dilini ayarlar

Komut: help
--------------

  rtg help                    # Genel yardım (bu ekran)
  rtg help <komut>            # Belirli bir komut/eklenti için yardım
  rtg help <komut> -<dil>       # Belirli dilde yardım (örn: -es, -en)
  rtg help <komut> -lang        # O komut için kullanılabilir diller
  rtg help -u                  # Genel kullanım (yeni)
  rtg help -u-<dil>            # Belirli dilde kullanım (örn: -u-es) (yeni)
  rtg help --usage             # Genel kullanım (yeni)
  rtg help --usage-<dil>       # Belirli dilde kullanım (örn: --usage-es) (yeni)
  rtg help usage               # Genel kullanım (alternatif sözdizimi, yeni)

  Örnekler:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-es
    rtg help --usage-es


Komut: version
-----------------

  rtg -v
  rtg --version

  Sürümü ve tüm kullanılabilir dillerdeki sürüm içeriğini gösterir.


Komut: rules
---------------

  rtg -r
  rtg --rules
  rtg -r -<dil>   # Belirli dildeki kurallar (örn: rtg -r -en)

  Varsayılan olarak 'rules' içinde tanımlanan ilk dil (İspanyolca) kullanılır.


Komut: lang
--------------

  rtg -l
  rtg --lang

  Tüm kullanılabilir dilleri kategori別に listeler:
  Version, Rules, Help, Void, ve her eklenti için.


Komut: commands
------------------

  rtg -c
  rtg --commands

  Yalnızca RtG-CLI dahili komutlarını listeler.
  Eklenti komutlarını içermez.


Komut: addons
----------------

  rtg -a
  rtg --addons

  Kullanıcıdan görünür belge/yardımı olan eklentileri listeler.
  Belgesi olmayan kayıtlı eklenti burada görünmez.


Komut: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<dil>         # Belirli dilde kullanım (örn: -u-es, -u-en) (yeni)
  --usage-<dil>         Belirli dilde kullanım gösterir (örn: --usage-es, --usage-en) (yeni)

  İstenen dildeki genel kullanım bilgilerini (void) gösterir.
  Dil, assets.json'daki 'void-language' içinde olmalıdır.


Komut: language
------------------

  rtg -language <dil>

  Başlangıç metni (void) dilini seçer.
  Dil, assets.json'daki 'void-language' içinde olmalıdır.

  Örnek:
    rtg -language en


Kullanılabilir Eklentiler
--------------------------

  image      | RtG Image        - Görüntü dönüştürücü
  preview    | RtG Preview      - RtG-Format yapıları için 3D görüntüleyici
  test-addon | RtG Test Addon   - CLI doğrulama için test eklentisi


Diller
-------

Diller tek bir tire ile belirtilir: -es, -en, -pt vb.
Dil, dahili komut adını değiştirmez.

  rtg help image -es    # İspanyolca yardım
  rtg help image -en    # İngilizce yardım
  rtg -r -en            # İngilizce kurallar

  Bir eklentinin dillerini görmek:
    rtg help image -lang

  -lang anlamı konumuna göre değişir:
    rtg --lang          # RtG-CLI dilleri (eklenti öncesi)
    rtg image -lang     # Eklenti dilleri (eklenti sonrası)


Eklenti Argümanları
--------------------

Bir eklenti tanımlandıktan sonra, argümanlar öneğe göre sınıflandırılır:

  tiresiz          -> eklenti        (örn: convert, file.png)
  --seçenek         -> eklenti        (örn: --width 128)
  -seçenek          -> RtG-CLI       (örn: -lang, -en)

Örnekler:
  rtg image convert file.png     # convert, file.png -> eklenti
  rtg image --width 128          # --width 128 -> eklenti
  rtg image -lang                # -lang -> RtG-CLI (eklenti dilleri)
  rtg image -en                  # -en -> RtG-CLI (dil seçici)


Boşluk İçeren Argümanlar
-------------------------

Boşluk içeren argümanlar tırnak içine alınmalıdır:

  rtg image "benim resmim.png" "cikti.json"

RtG-CLI argüman sırasını korur ve aynen eklentiye iletir.


Daha Fazla Bilgi
-------------------

  rtg help <komut>      # Bir eklenti için ayrıntılı yardım
  rtg help <komut> -lang  # O eklentinin dilleri
  rtg --addons          # Tüm belgeli eklentileri gör
  rtg --commands        # Dahili komutları gör