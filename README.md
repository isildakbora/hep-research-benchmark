<!-- Created: 2026-09-21 22:13:12 +03 -->
# HEP Research Benchmark — v0.1 tasarım ve başlangıç paketi

GitHub'dan indirip ilk model denemesini yapmak için: **[Adım adım çalıştırma kılavuzu](RUN_GUIDE_TR.md)**.

Bu paket, birkaç LLM üzerinde kontrollü bir ilk deneme yapmak ve daha sonra bir benchmark makalesi hazırlamak için oluşturuldu. Çalışma adı geçicidir. Kapsam, HEP bilgisinden çalıştırılan analizlere uzanan sekiz yetenek alanıdır; ilk görevler çarpıştırıcı fiziği ağırlıklıdır. HEP'in bütün alt alanlarını temsil ettiği iddia edilmez.

**Mevcut durum:** 16 özgün açık görev ailesi, referans yanıtlar, ölçütler, dört görsel, iki küçük sentetik veri dosyası, koşu şablonları ve puan toplama aracı. İnsan alan uzmanı doğrulaması, gizli test kümesi ve gerçek LLM ölçümü henüz yoktur. Görevlerin bir bölümü kolaydır; starter doygunluğunu önlemek için zorlaştırılmış nihai sürüm gerekir.

**Hedef sürüm:** Sekiz modülde 12'şer aile, toplam 96 aile; bunun 24'ü açık geliştirme, 72'si gizli test için planlanmıştır. Bu bir başlangıç örneklem planıdır, istatistiksel yeterlilik garantisi değildir. `catalog_96.csv` içinde yalnız ilk 16 ailenin mevcut, diğerlerinin plan olduğunu gösteren durum alanı vardır.

## Dosyalar

- `DESIGN_TR.md`: kapsam, profiller, görev üretimi, deney ve yayın protokolü.
- `SCORING_TR.md`: puanlama, başarısız koşular, maliyet ve belirsizlik kuralları.
- `catalog_96.csv`: nihai kapsam için konu/aile kataloğu; tamamlanma durumu açıkça işaretli.
- `public/tasks.jsonl`: 16 başlangıç görevinin makine tarafından okunabilir kayıtları.
- `public/prompts/{text,tools,full}/`: profil için doğru istemler.
- `public/assets/`: yalnız gerekli koşulda modele gösterilecek görseller/veriler.
- `evaluator/answer_key.jsonl`: referanslar, toleranslar, dört ölçüt ve kritik koşullar. **Modele verme.**
- `templates/results_*.csv`: üç tekrar için boş ölçüm tabloları.
- `templates/run_config.json`: model ve koşu ayarları.
- `templates/system_prompt.txt`: tüm modellere ortak temel istem.
- `scripts/export_task.py`: yalnız seçilen görevin doğru profilini ve eklerini model paketine çıkarır.
- `scripts/score_results.py`: dışarıda doğrulanmış puanları toplar; LLM yanıtlarını otomatik değerlendirmez.
- `VALIDATION.md`: yapılan teknik kontroller ve henüz yapılmayan doğrulamalar.

## İlk deneme

Çalıştırma araçları için Python 3.10+ standart kütüphanesi yeterlidir (3.14.4 ile test edildi); araç API anahtarı kullanmaz, model çağırmaz ve ücretli işlem yapmaz. Görseller hazır PNG olarak verilir; mevcut görevleri kullanmak için görsel üretme bağımlılığı gerekmez.

1. Karşılaştırılacak modeller için aynı profili seç: yalnız metin `text`; terminal/kod çalıştırma `tools`; bunlara görsel giriş de ekleniyorsa `full`.
2. Her model/checkpoint/quantization/harness ayarına farklı `model_id` ver. `run_config.json` kopyasını gerçek değerlerle doldur.
3. Model için yeni, boş bir oturum aç. Ortak sistem istemi ve yalnız bir görev paketini ver:

```bash
python3 scripts/export_task.py --task T301 --profile full --out runs/modelA/full/r1/T301/input
```

4. Yanıtı, üretilen kodu, araç kayıtlarını ve maliyeti sakla. Aynı profil içinde her görevi üç ayrı yeni oturumda çalıştır. Görevler arasında bellek veya dosya paylaşma.
5. Kodları ayrı değerlendirme ortamında çalıştır, referans/rubrik ile puanla ve ilgili CSV'yi doldur. `passed` 0/1, `partial_score` 0–1; bunlar modelin kendi beyanı değildir.
6. İlgili CSV'deki tüm `REPLACE_MODEL_ID` alanlarını değiştir. Birden çok modelin CSV'sini tek başlık altında birleştirebilirsin. Farklı profiller dosyada bulunabilir fakat ayrı raporlanır.

```bash
python3 scripts/score_results.py --tasks public/tasks.jsonl --results runs/results_full.csv --repeats 3 --out runs/scores_full.json
```

Boş şablonlar `pending` olarak kalır; araç bunlara puan vermez. Bir görev eksikse toplam skor bloke edilir. Tamamlanan starter koşularının özetleri yalnız açıklayıcıdır; doğrulanmış model sıralaması sayılmaz.

## Modellerin alacağı dosyalar

Değerlendirilen ajanı bu projenin kökünde başlatma. Ayrı boş çalışma alanına sadece `export_task.py` çıktısını koy. `evaluator/`, diğer görevler, diğer profil istemleri ve sonuç CSV'leri modelin erişiminde olmamalı. Bu paket başlangıç/development paketi olduğu için bütün yanıt anahtarları kullanıcıya açıktır; gizli benchmark değildir.

`export_task.py` interneti kapatmaz, sandbox kurmaz veya araç çağrılarını sınırlamaz. Bu koşulları kullanılan model/ajan ortamında uygulamak gerekir. Henüz otomatik çok sağlayıcılı API koşucusu veya sandbox uygulaması eklenmedi.

## Kaynaklarla ilişki

Görevler bu tasarım için özgün olarak yazılmış sentetik başlangıç örnekleridir; aşağıdaki benchmarkların görevleri veya sonuçları kopyalanmadı. Mevcut çalışmaları yeniden koştuğumuz iddia edilmez.

Ana karşılaştırmalar: [TPBench](https://arxiv.org/abs/2502.15815), [Towards a Large Physics Benchmark](https://arxiv.org/abs/2507.21695), [LLM-powered HEP analysis](https://arxiv.org/abs/2512.07785), [CelloAI](https://arxiv.org/abs/2603.01051), [FeynmanBench](https://arxiv.org/abs/2604.03893), [PRL-Bench](https://arxiv.org/abs/2604.15411), [Collider-Bench](https://arxiv.org/abs/2605.13950), [HEPToolBench](https://arxiv.org/abs/2608.28232).

Bilimsel geçerlilik ve denetim için ilgili çalışmalar: [SciIF](https://arxiv.org/abs/2601.04770), [SDABench](https://arxiv.org/abs/2607.11079), [VERA](https://arxiv.org/abs/2608.26596), [Beyond Execution](https://arxiv.org/abs/2608.26753). Fiziksel belirsizlik değerlendirmesi için [FAIR Universe HiggsML](https://arxiv.org/abs/2410.02867) ilgili bir yöntem kaynağıdır; LLM benchmarkı değildir.

Bu paket için henüz yayın/lisans kararı verilmedi. İleride eklenen kaynak, veri ve şekillerin kullanım koşulları ayrı kaydedilmeli.
