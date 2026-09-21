<!-- Created: 2026-09-21 22:13:12 +03 -->
# Puanlama sözleşmesi

## Görev puanı

Her starter görevinde dört ölçüt vardır. Ölçüt puanları `0` (yanlış/eksik), `0.5` (kritik olmayan kısmi doğruluk), `1` (tam karşılanmış) olarak uzman tarafından atanır. Her ölçütün ağırlığı 0.25'tir. `partial_score=sum(weight_i*criterion_i)` bir teşhis puanıdır; bilimsel anlamda eşit aralıklı yetenek ölçeği olduğu iddia edilmez.

`passed=1`, görevin önceden açıklanmış bütün **kritik** ölçütleri tam karşılandığında verilir. Diğer durumda 0'dır. Kritik kriterde kısmi doğruluk başarı sayılmaz. Nicel testlerde tolerans dışında sayı tam puan alamaz; yanlış bilimsel sonuç güzel anlatımla telafi edilmez. Sıradan Markdown/üslup farkı bilimsel başarısızlık değildir; native/JSON koşullarında çıktı çıkarma kuralları simetrik olmalıdır.

Kod için düzgün görünen metin yeterli değildir. T401/T402/T701 kodu evaluator tarafından örnekte olmayan girdilerle çalıştırılmalıdır; T801/T802 için çalıştırılmış kod, sonuç ve logun izlenebilirliği zorunludur. Kod değerlendirmesi izole ortamda yapılır. JSON referansında sayının bulunması, evaluator testinin uygulanmış olduğu anlamına gelmez. Paket bu kodları otomatik çalıştıran bir sandbox sağlamaz.

Her değerlendirme için ölçüt puanları ve kısa kanıt ayrıca saklanır (`templates/rubric_record.json`). CSV'de yalnız toplamlar tutulur. `score_results.py` CSV'ye yazılan hükmün bilimsel doğruluğunu denetlemez. Hakem LLM kullanılırsa kararlar özellikle kritik hatalarda insan doğrulamasından geçmeli; değerlendirilen model kendi tek hakemi olmamalıdır.

## Toplama

R tekrar için aile başarısı `P_f=(sum_r pass_fr)/R`. Starter'da her aile/profil için tek görev vardır. Modül skoru `S_m=100*mean_f(P_f)`. Çekirdek skor o profilde sabitlenmiş M1–M7 modüllerinin eşit ağırlıklı ortalamasıdır. M8 ayrıca integration skoru olarak verilir. Çok görevi olan modül, sırf madde sayısı nedeniyle daha yüksek ağırlık kazanmaz.

Araç şu alanları verir:

- `task_scores`: tekrarlar üzerinden görev başarı/kısmi puan ortalaması.
- `module_scores`: modül başarı yüzdesi, kısmi puan yüzdesi ve aile sayısı.
- `core_pass_percent`: M8 dışındaki mevcut kanonik modüllerin makrosu.
- `integration_pass_percent`: M8 varsa onun puanı; yoksa null.
- `macro_pass_percent`: bütün mevcut modüllerin ikincil betimsel özeti; full dışındaki değerler full HEP skoru diye sunulamaz.
- `macro_partial_percent`: kısmi puanların ikincil betimsel özeti.
- `confidence_brier`: mevcut güven beyanlarında mean((confidence-pass)^2); düşük daha iyidir. Sayı ve toplam beklenen koşu sayısı birlikte verilir.
- `totals`: süre/token/maliyet toplamları ve kaç koşunun verisinin bulunduğu. Eksik değer sıfır değildir.

Başlık etiketi her raporda `starter_smoke_test_not_validated_leaderboard` olur. Starter için tablo/işleyiş kontrolü yapılabilir; model üstünlüğü ya da insan düzeyi iddiası kurulamaz. Araç skorları sıralamaz ve güven aralığı hesaplamaz. Yayın sürümünde aile/grup düzeyindeki istatistiksel değerlendirme ayrıca uygulanmalıdır.

## Durumlar ve eksiklik

| status | CSV skorları | Anlamı |
|---|---|---|
| completed | passed 0/1 ve partial_score 0–1 zorunlu | Model yanıtı değerlendirilmiş; yanlış yanıt da completed olabilir |
| timeout | boş veya 0; hesapta 0 | Modelin önceden belirlenmiş bütçesi bitmiş |
| model_error | boş veya 0; hesapta 0 | Modele atfedilen yanıt/çalışma başarısızlığı |
| infra_error | boş | Dış altyapı arızası; toplam skor bloke |
| pending | boş | Çalıştırılmamış/puanlanmamış; toplam skor bloke |

Skor aracı herhangi bir görev/tekrar eksikse `incomplete` yazar; mevcut kolay görevler üzerinden toplam oluşturmaz. Yinelenen satır, profil dışı görev, aralık dışı değer, NaN/Inf ve belirsiz task ID hata olarak reddedilir. Starter uygulaması aynı profilde bir aileye birden çok task tanımlanmasını reddeder; gelecekte varyantlar eklenirse önce aile içi ağırlıklandırma uygulanmalıdır.

## Bilimsel denetim yan metrikleri

M7'nin geniş sürümünde temiz örnek yanlış alarm oranı, yöntem hatası recall/precision, başarılı onarım ve eksik kanıtta doğru çekimserlik ayrı paydalarla verilir. Bir görevde birden fazla hata varsa hata örneği ile görev başarısı ayrılır. Starter'da M7 yalnız bir hatalı ve bir temiz örnek içerdiğinden bu oranlar anlamlı bir güvenilirlik ölçümü sağlamaz; eksik kanıt davranışı M1'de örneklenmiştir.

Bir fiziksel düzeltmenin başarısı; gerektiğinde tahmin yanlılığı, interval coverage, aralık genişliği, histogram farkı veya bağımsız örneklem performansıyla değerlendirilir. Bu ölçüler göreve özeldir ve keyfi tek ağırlıklı toplam içine saklanmaz. Bütçe, hız ve maliyet ana bilimsel skora eklenmez; başarı–maliyet karşılaştırması ayrı gösterilir.
