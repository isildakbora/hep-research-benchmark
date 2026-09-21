<!-- Created: 2026-09-21 22:13:12 +03 -->
# HEP Research Benchmark: deney tasarımı

## Araştırma soruları

1. HEP bilgi ve hesaplama başarısı, doğru kod ve fiziksel olarak geçerli analiz üretimini ne kadar öngörüyor?
2. Aynı modelde sabit kaynaklara ve yürütme geri bildirimine erişim hangi hata türlerini azaltıyor?
3. Diyagram/histogramın görsel sunumu, aynı içeriğin sembolik veya tablosal sunumuna göre sonucu nasıl değiştiriyor?
4. Modeller yöntem hatasını bulup düzeltebiliyor mu; doğru analizi gereksiz yere bozuyor mu; eksik bilgi karşısında sınırını belirtiyor mu?
5. Farklı maliyet ve model boyutlarında, fizik başarısı ile süre/maliyet arasındaki ilişki nasıl değişiyor?

İlk sürümün kapsamı çarpıştırıcı HEP pratiğidir. Genel görelilik, tüm kozmoloji, nükleer fizik ve HEP'in bütün deneyleri için temsil iddiası yoktur. Teori ve araç modülleri alan genişletmesine açıktır.

## Sekiz modül

| Modül | Ölçülen yetenek | Örnek çıktı | Doğrulama |
|---|---|---|---|
| M1 Bilgi ve kaynak | Kavram, fiziksel iddia, kapsam, kaynak desteği ve eksik bilgi | Kısa yanıt, kaynak→iddia eşlemesi | Uzman anahtarı; kaynakta gerçekten bulunan kanıt |
| M2 Teori ve nicel muhakeme | Kinematik, QED/QCD, sınır durumları, simetriler, ölçekler | Formül, sayı, varsayımlar | Analitik çözüm, sayısal eşdeğerlik, limit kontrolleri |
| M3 Feynman diyagramları | Parçacıklar, topoloji, momentum akışı, mertebe, uygun görevde genlik | Graf temsili ve cebirsel çıktı | Graf/korunum testleri, sembolik/nümerik eşdeğerlik, uzman denetimi |
| M4 Kod ve HEP araçları | Genel kod, ROOT/Python, kart üretimi, debugging, dokümantasyon, uygun altyapıda GPU porting | Çalıştırılabilir dosya veya yapılandırma | Parse + gerçek çalışma + bağımsız fizik testleri; dokümantasyonda uzman ölçütü |
| M5 Veri ve istatistik | Ağırlıklar, likelihood, nuisance parametreleri, korelasyon, interval, coverage | Sayısal sonuç ve istatistiksel model | Referans likelihood, pseudo-deney, covariance kontrolleri |
| M6 Dedektör ve histogram | Eksen/ölçek okuma, normalizasyon, DQM, dedektör yanıtı, anomali ve neden ayrımı | Grafik/tablo yorumu ve nicel teşhis | Görselin alttaki bin verisi, bilinen senaryo, uzman ölçütü |
| M7 Bilimsel denetim | Doğru/hatalı/eksik kanıtlı analizi ayırt etme; hatayı onarma | Verdict, kanıt, patch, onarımın sonucu | Temiz kontroller + enjekte edilmiş yöntem hataları + yeniden yürütme |
| M8 Uçtan uca analiz | Kaynak/veriden analiz koduna, doğrulamaya ve rapora bütün süreç | Kod, sonuç, cutflow/fit, log, kısa rapor | Bağımsız yeniden yürütme, gizli veri ve izlenebilir sonuç |

M4 içindeki syntax başarısı fiziksel doğruluk yerine geçmez. M3'te görüntü/piksel benzerliği puanlanmaz. M6'da anomali saptamak, donanım kök nedenini kanıtlamaktan ayrıdır. M8 diğer becerileri yeniden kullandığından ana değerlendirmede ayrı bir integration skoru olarak verilir.

## Profiller ve karşılaştırılabilirlik

| Profil | Modelin erişimi | Kanonik modüller | Starter görev sayısı |
|---|---|---|---:|
| text | Metin istemi ve gömülü sabit kaynak; araç/internet yok | M1,M2,M4,M5,M6,M7 | 12 |
| tools | Aynı temel paket + sabit yerel terminal/Python ortamı; internet yok | Aynı altı modül + M8 | 14 |
| full | tools + görsel giriş; M6 tabloları yerine eşlenmiş grafikler | M1–M8 | 16 |

Modelin text profilinde kod çalıştıramaması, değerlendiricinin kodu çalıştırmayacağı anlamına gelmez. M4 kod çıktısı her profilde bağımsız testlerle değerlendirilir. Çalıştırılmış gibi sunulan fakat çalıştırılmamış çıktı ayrı hata etiketidir.

Farklı profil skorları aynı leaderboard'a konulmaz. tools–text farkı, erişim+geri bildirim+yeniden deneme sisteminin farkıdır; saf model kapasitesi farkı diye adlandırılmaz. full–tools karşılaştırması sadece ortak ailelerin eşlenmiş M6 koşulları için görsel delta verir. M3'ün sembolik karşılığı starter'da yoktur; gelecekte hazırlanacak eşlenmiş sürüm aynı aile sayılır.

M1 içinde `knowledge` ve `frozen_source` alt etiketleri tutulur; kaynak verilmiş sonuç kapalı-kitap skoruyla karıştırılmaz. Starter T101 kavramsal/eksik eşleme, T102 sentetik kaynak paketidir. Gerçek literatür tarama/RAG yeteneği için tarihli, dondurulmuş bir corpus ve corpus ID gerekir; bu corpus starter'a eklenmedi. Canlı web kullanımı ayrı keşif profili olur ve ana skorla birleştirilmez.

GPU porting gibi donanım isteyen görevler aynı hızlandırıcı ve yazılım ortamıyla ayrı alt testte çalıştırılır. GPU bulunmayan modeli bu görevden sessizce muaf tutup tam skor hesaplamak yasaktır. v0.1 starter yalnız CPU gerektiren kod içerir.

## Aile, varyant ve koşu

- **Aile:** Bağımsız bilimsel problem veya analiz kökü. İstatistiksel örnekleme birimi budur.
- **Varyant:** Aynı aileden doğru/hatalı/eksik sürüm, sayı değişimi, paraphrase veya görsel/tablo sunumu. Bağımsız yeni örnek sayılmaz.
- **Koşul/profil:** Modele verilen araçlar, kaynaklar ve modalite.
- **Koşu:** Bir aile/varyant/koşulun yeni oturumda tek denemesi. Araçlı koşuda bütçe içinde kod düzeltme bu tek koşunun parçasıdır.

Hedef dağılım modül başına 12 aile: 3 açık geliştirme + 9 gizli test. Split birimleri en az aile, ortak makaleden türeyen ailelerde ayrıca kaynak/analiz grubu olmalıdır. Bu kümeleri korumak için tam 3/9 dengesi gerekirse gevşetilir; sızıntısızlık sayısal dengeye tercih edilir. Ortak generator/template bağımlılığı da kayıt altına alınır.

Starter modül başına iki açık aile içerir. Bunlar nihai gizli teste taşınmaz. Modül başına dokuz test ailesi küçük olduğundan nihai örneklem sayısı pilot zorluk, madde ayırt ediciliği ve istenen karşılaştırma hassasiyetine göre yeniden hesaplanır. Tekrar sayısı, bağımsız aile eksikliğini gidermez.

## Görev üretimi ve doğrulama

Her görevde prompt, kaynak/asset sürümü, kabul edilen fiziksel konvansiyonlar, referans çözüm, 2–4 kritik bilimsel koşul, kısmi puan ölçütleri, toleranslar ve provenance kaydı bulunur. Doğal birden fazla geçerli çözüm kabul edilir. İstemde olmayan yazılım konvansiyonları sonradan gizli zorunluluk haline getirilmez.

Görev yazarı referans çözümü kurar. İkinci alan uzmanı istemi çözümden bağımsız çözer; üçüncü kişi anlaşmazlıkları giderir. Kod görevlerinde farklı uygulama veya analitik limit kullanılarak ortak hata riski azaltılır. Aynı LLM'nin hem görev hem cevap üretmesi doğrulama sayılmaz; bu paketteki ajan denetimi insan uzman doğrulaması değildir.

Toleranslar sonuçlar görüldükten sonra modele göre değiştirilmez. Deterministik starter sayıları için |x-ref|<=1e-6+1e-3|ref| kullanılır; sayımlar/etiketler tam eşleşir. Gerçek MC görevlerinde istatistiksel oynama, simülasyon yaklaşımı ve referans belirsizliği ayrıca hesaba katılır. Bir yayını yaklaşık açık simülasyonla yeniden üretirken model başarısızlığı ile fizik modellemesi farkı karıştırılmaz.

M7'nin nihai sürümünde her uygun aile için doğru, yöntem hatalı ve eksik kanıtlı örnek hazırlanır. Örnekler ayrı oturumlarda ve nötr dosya adlarıyla verilir. Hata sayısı/sürümü söylenmez. Hatanın observable, fit parametresi, belirsizlik veya limit üzerindeki etkisi referans zincirde önceden ölçülür. Genel syntax hataları bilimsel yöntem hatalarıyla ayrı etiketlenir. Gerçek hata örnekleriyle desteklenmeyen tamamen sentetik sonuçların dış geçerliliği sınırlı olarak belirtilir.

Gizli testte yalnız sayıları değiştirilmiş açık şablonlar kullanılmaz. Benzerlik ve kaynak örtüşmesi kontrol edilir. Referans, generator seed ve scorer model konteynerine bağlanmaz. Yenileme ve değerlendirme sorgusu sınırı planlanır. Test cevapları daha sonra yayımlanırsa o sürüm artık geliştirme kümesi sayılır.

## Birkaç LLM ile koşma protokolü

İlk çalışma için farklı model ailelerinden 3–5 sistem yeterli bir başlangıç planıdır; hangi modellerin seçileceği kullanıcının erişim/bütçesine bağlıdır. Belirli bir güncel modelin daha iyi olduğu varsayılmaz. API modellerinde sürüm/tarih; açık modellerde checkpoint hash, quantization, runtime, context uzunluğu ve donanım kaydedilir. Farklı quantization'lar farklı sistem kimliğidir.

Her görev/profil üç yeni oturumda çalıştırılır; sonuçların en iyisi seçilmez. Aynı system prompt, task prompt, kaynak, çıktı beklentisi ve bütçe kullanılır. Görev sırası seed ile karıştırılır ve bütün modeller için dengelenir. Bellek, geçmiş yanıtlar ve diğer görev dosyaları erişilemez olmalıdır. Erişilebilir ortak bağlam limiti seçilir; sessiz kaynak kesilmesi yapılmaz.

Başlangıç bütçe önerisi (kalibrasyon sonrası dondurulacak): standard görev 10 dakika, en çok 8.192 yeni üretilen token, araçlıysa 30 çağrı; integration görev 30 dakika, en çok 24.576 token ve 100 çağrı. Bunlar başarı eşikleri veya literatürden çıkarılmış optimum değerler değildir. Sağlayıcı reasoning token'larını aynı biçimde sınırlayamıyorsa görünen/gizli muhasebe farkları ve gerçek kullanım raporlanır; saf eşit-compute iddiası yapılmaz. `run_config.json` seçilen nihai değerleri taşır.

Araç ortamı için içerik sabitlenmiş konteyner/image digest önerilir. Starter'ın betikleri bu konteyneri sağlamaz; bağımlılıksız Python örnekleri farklı makinelerde ön kontrol içindir. Maliyet modeli değişse bile gerçek fatura/kullanım verileriyle hesaplanır; olmayan maliyet verisi sıfır sayılmaz.

Altyapı/sağlayıcı 5xx/transport arızası için en çok iki yeniden deneme önceden tanımlanır; ilk geçerli koşu alınır ve tüm denemeler loglanır. Çözülemezse durum `infra_error`, karşılaştırma eksik kalır. Modelin süre/token/araç bütçesini tüketmesi `timeout`, bilimsel olarak yanlış yanıtı `completed,passed=0`, yanıt üretememesi `model_error` olarak sayılır. Hakem kararını gördükten sonra yeniden deneme yapılmaz.

## Ana sonuçlar ve belirsizlik

Ana rapor: profil bazlı M1–M7 puan vektörü, bu profildeki çekirdek modüllerin makro başarı skoru ve ayrı M8 integration başarı skoru. Tek sayı istenirse sekiz-modül makro yalnız tam full profilde ikincil özet olur; M8 ile beceri tekrarının etkisi açıklanır. Eksik alanlar sıfırla doldurulmaz veya gizlice çıkarılmaz.

Başarı aralığı, eşlenmiş model farkı ve örnek sayısı birlikte raporlanır. Aile/varyant/tekrar hiyerarşisini koruyan, gerektiğinde kaynak grubu üzerinde blok bootstrap kullanılır. Tekrarlar önce aile içinde özetlenir; bağımsız n'ye eklenmez. Modül içi örnekler azsa dar lider sıralaması yapılmaz. Önceden seçilmiş temel karşılaştırmalar ile keşif analizleri ayrılır; çoklu test uygulanıyorsa düzeltme yöntemi belirtilir.

Coverage, fiziksel güven aralığının pseudo-deneyler boyunca gerçek parametreyi kapsama oranıdır; aralık genişliği ve Monte Carlo belirsizliğiyle birlikte verilir. Bu, modelin görev cevabına güveninden ayrı metriktir. Starter coverage deneyi içermez. Starter Brier çıktısı yalnız beyan edilen başarı olasılığını değerlendirir; az örnekle kalibrasyon iddiası kurulmaz.

## Yayın için katkı ve gerekli kanıt

İlk HEP LLM benchmarkı, ilk bilimsel hata denetimi veya ilk otonom HEP analizi iddiaları kullanılmaz. Önerilen katkı; sekiz becerinin aynı protokolde ayrıştırılması, kaynak/araç/modalite koşullarının eşlenmesi ve bilimsel onarımın nihai fizik sonucuna etkisinin yürütülerek ölçülmesidir. Bu katkının mevcut ölçümlerden ne kadar farklı olduğu deneyle gösterilmelidir; yalnız modülleri bir araya getirmek yeterli kanıt değildir.

Makalede beklenen tablolar/şekiller: kapsam ve related-work matrisi; görev doğrulama ve split dökümü; modül skorları+belirsizlik; bilgi başarısı ile analiz başarısı ilişkisi; eşlenmiş araç/görsel deltalara ilişkin analiz; kritik hata/yanlış alarm/onarım matrisi; başarı–maliyet grafiği; anonimleştirilmiş doğrulanabilir vaka incelemeleri.

Makale paketi için gerekenler: bağımsız uzman denetimi, dondurulmuş görev ve evaluator sürümü, gerçek model koşuları, baseline ve hata analizleri, yeniden üretim talimatları, veri/lisans/provenance kaydı. Mevcut v0.1 bunların hazırlık tasarımı ve açık starter kısmıdır. Makale metninde henüz elde edilmemiş sonuç yazılmamalı.
