# OBJECT-OR-ENTED-PROGRAMM-NG

### Araç Kiralama Sistemi

### Temel bileşenleri:
### Veri modeli;
### Arac sınıfı: Araç bilgilerini (ID, model, günlük ücret, kiralama durumu) tutar.

### Musteri sınıfı: Müşteri bilgilerini (ID, ad) tutar.

### Kiralama sınıfı: Kiralama işlemlerini yönetir; kiralama yapma ve iptal etme fonksiyonları var.

### Veri yönetimi:
### Veriler JSON dosyasına (veri.json) kaydedilip oradan yükleniyor.

### Araçlar, müşteriler ve kiralamalar ayrı ayrı veri yapılarında tutuluyor.

### Arayüz (Tkinter):
### Üç ana sekme var;

### Araçlar: Araç ekleyebilir ve mevcut araçları görebilirsin.

### Müşteriler: Müşteri ekleme ve listeleme.

### Kiralama: Müşteri ve araç ID’si ile kiralama yapabilir veya kiralamayı iptal edebilirsin. Kiralanan araçların listesi gösteriliyor.

### İşlevsellik:
### Kiralama yaparken tarihler kontrol ediliyor, araç kiradaysa hata veriliyor.

### Kiralama iptal edilince araç durumu güncelleniyor.

### Kiralama ücreti, kiralama gün sayısı * araç günlük ücreti olarak hesaplanıp gösteriliyor.

### Tüm değişiklikler JSON dosyasına kaydediliyor.

### Görsellik:
### Modern ve temiz bir tema kullanılmış.

### Ağaç görünümleri (Treeview) ile araç, müşteri ve kiralama listeleri gösteriliyor.

### Özetle, bu uygulama araç kiralama işlemlerini takip etmek, araç ve müşteri eklemek, kiralama işlemi yapmak ve iptal etmek için bir arayüz sunuyor ve verileri kalıcı şekilde JSON dosyasında saklıyor.
###                        
###                                
###                              
###                                 



### Kütüphane Yönetim Sistemi
### Veri Yapısı ve Dosyalar:

### Kitaplar, üyeler, kullanıcılar ve ödünç kayıtları JSON dosyalarında saklanıyor.

### Her biri için ayrı sınıflar (Kitap, Uye, Kullanici, Odunc) var. Bu sınıflar veriyi nesne olarak tutup, JSON’a kolayca dönüştürülüp tekrar ### yüklenmesini sağlıyor.

### Veri Yükleme ve Kaydetme:

### JSON dosyalarından veriler uygulama açılırken yükleniyor.

### Veriler değiştiğinde yine JSON dosyalarına kaydediliyor.

### Kullanıcı Yönetimi:

### Sistemde admin ve normal kullanıcılar var.

### Eğer hiç kullanıcı yoksa otomatik olarak admin kullanıcısı oluşturuluyor.

### Tkinter Arayüzü:

### Giriş ekranı var, kullanıcı adı ve şifre ile sisteme giriş yapılabiliyor.

### Başarılı giriş sonrası 3 ana sekme açılıyor:

### Kitap Yönetimi: Kitap ekleme, listeleme ve kitapların rafta mı ödünçte mi olduğunu gösterme.

### Üye Yönetimi: Üye ekleme ve listeleme.

### Ödünç İşlemleri: Üyenin kitap ödünç alması ve iade etmesi.

### Ödünç Alma / İade Süreci:

### Kitap ödünç verildiğinde kitap durumu “Ödünçte” olarak işaretleniyor ve 14 gün sonra iade tarihi belirleniyor.

### Kitap iade edilince kitap tekrar “Rafta” olarak işaretleniyor ve ödünç kaydı siliniyor.

### Arayüz Özellikleri:

### Kitaplar, üyeler ve ödünç kayıtları için tablo görünümü (Treeview) ile listeleme yapılabiliyor.

### Kullanıcıya hatalar veya başarı durumları mesaj kutuları ile bildiriliyor.

### Kısaca, kullanıcı yönetimi, kitap ve üye ekleme, ödünç alma/iade işlemleri yapabilen ve tüm verileri JSON dosyalarına kaydeden bir masaüstü kütüphane sistemi.
###                      
###                      
###                   
###                        


### Restoran Sipariş ve Yönetim Sistemi
### Genel Yapı:
### Arayüz Tkinter ve ttk bileşenleri ile tasarlanmış.

### Görsel stil için özel renkler ve yazı tipleri ayarlanmış.

### Veriler .json dosyasına kaydedilip geri yüklenebiliyor (kalıcılık sağlanmış).

### Veri Yapıları:
### Ürünler, Müşteriler ve Siparişler için ayrı sınıflar tanımlanmış (Urun, Musteri, Siparis).

### Veriler bu sınıflarla oluşturuluyor ve bellekte sözlük/listelerde tutuluyor.

### Arayüz Sekmeleri:
### Uygulama iki ana sekmeden oluşuyor:

### Ürün Yönetimi: Ürün ekleme, listeleme işlemleri yapılır.

### Sipariş Al: Müşteri bilgisi girilir, ürün seçilir, sepete eklenir ve sipariş verilir.

### Sipariş İşlemleri:
### Siparişler ürün ve adet bilgisi ile sepete eklenir.

### Toplam fiyat hesaplanır.

### Siparişler siparisler listesine eklenir ve JSON’a kaydedilir.

### Veri Kaydetme/Yükleme:
### Uygulama kapandığında veriler .json dosyasına kaydedilir.

### Açıldığında bu dosyadan otomatik olarak yüklenir.

### Bu Tkinter uygulaması, bir restoranın ürün ve sipariş yönetimini sağlar. Kullanıcı ürün ekleyebilir, sipariş oluşturabilir, siparişleri silebilir ve tüm veriler JSON dosyasında saklanır. Arayüz üzerinden işlemler kolayca yapılır ve veriler kalıcıdır.
###                     
###                    
###                 
###                  



### Yemek Tarif Uygulaması
### Tkinter arayüzü kuruluyor:

### Pencere başlığı, boyutu ve arka plan rengi ayarlanıyor.

### Stil (font, buton, tab vb.) ayarları yapılıyor.

### Veri yapıları tanımlanıyor:

### Malzeme sınıfı: Tariflerdeki malzemeleri tutuyor (adı ve miktarı).

### Tarif sınıfı: Tarifin adı, malzemeleri, içeriği ve puanları tutuluyor. Ortalama puan hesaplanabiliyor.

### Veri dosyası (tarifler.json) ile veri kalıcılığı sağlanıyor:

### Tarifler ve favoriler JSON formatında kaydedilip yükleniyor.

### Arayüzde birden fazla sekme (tab) oluşturuluyor:

### Tarif ekleme, tüm tarifler, favoriler, malzemeye göre filtreleme, en yüksek puanlılar ve tarif değerlendirme sekmeleri var.

### Tarif ekleme sekmesi:

### Kullanıcıdan tarif adı, malzemeler (satır satır malzeme, miktar formatında) ve tarif içeriği alınıyor.

### Girilen bilgiler kontrol edilip, aynı isimde tarif varsa uyarı veriliyor.

### Yeni tarif listeye ekleniyor ve veri kaydediliyor.

### Tüm tariflerin listelendiği sekme:

### Tarifler listeleniyor. Seçilen tarifin detayları (malzemeler, içerik, ortalama puan) gösteriliyor.

### Tarif silme ve favorilere ekleme butonları var.

### Favoriler sekmesi:

### Favorilere eklenen tarifler listeleniyor.

### Malzemeye göre filtreleme sekmesi:

### Girilen malzeme adına göre tarifler filtreleniyor ve gösteriliyor.

### En yüksek puanlı tariflerin listelendiği sekme:

### Tarifler ortalama puanlarına göre sıralanıp listeleniyor.

### Tarif değerlendirme sekmesi:

### Listeden tarif seçip 1-5 arası puan verilebiliyor.

### Verilen puan tarifin puan listesine ekleniyor, ortalama puan güncelleniyor.

### Fonksiyonlar:

### Tarif ekleme, silme, favorilere ekleme, filtreleme, puan verme gibi işlemler için fonksiyonlar tanımlanmış.

### Arayüz öğeleri bu fonksiyonlarla bağlanmış.

### Uygulama açıldığında:

### JSON dosyasından veri yükleniyor.

### Tarif, favori, puanlı ve değerlendirme listeleri güncelleniyor.

### Özet: Kullanıcı dostu arayüzüyle, tarif ekleme, listeleme, filtreleme, favorilere ekleme ve puanlama işlemlerini kolayca yapmanı sağlayan bir tarif uygulaması.