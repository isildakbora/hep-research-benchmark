<!-- Updated: 2026-09-21T20:03:53+00:00; public repository access -->
<!-- Created: 2026-09-21; private GitHub publication and operational guide -->
# Birkaç LLM ile nasıl çalıştırılır?

Mevcut sürüm görev hazırlama ve **dışarıda doğrulanmış puanları toplama** aracıdır. Modelleri otomatik çağıran bir API koşucusu veya yanıtları otomatik puanlayan hakem henüz yoktur. Sohbet arayüzüyle ya da kendi model API/ajan ortamınızla kullanılabilir. İlk smoke test için text profili en az kurulum gerektirir; nihai karşılaştırma için tüm modellerde aynı profil ve ayarlar korunur.

## 1. Açık depoyu indir ve test et

Depo public olarak paylaşılır. Git ile kimlik doğrulaması olmadan klonlanabilir; GitHub CLI kullananlar için:

```bash
gh repo clone isildakbora/hep-research-benchmark
cd hep-research-benchmark
python3 --version
python3 -m unittest discover -s tests -v
```

Python 3.10 veya üstü gerekir; 3.14.4 ile 20 test geçti. pip kurulumu gerekmez. Bu komutların hiçbiri LLM çağırmaz. GitHub CLI yerine doğrudan git ile de klonlanabilir:

```bash
git clone https://github.com/isildakbora/hep-research-benchmark.git
```

Aşağıdaki bütün komutları depo kökünden çalıştır.

## 2. Profil ve model kimliğini seç

| Profil | Modelin kullanabileceği yetenek | Her model için 3 tekrarda görev koşusu |
|---|---|---:|
| text | Metin; model tarafında terminal/kod/internet yok | 36 |
| tools | Metin + yerel terminal/Python; internet yok | 42 |
| full | tools + görsel giriş | 48 |

Örnekte `modelA` bir yer tutucudur. Bunun yerine sürümü belirli bir model adı kullan. Farklı checkpoint, quantization veya agent harness farklı `model_id` almalıdır. Bir sohbet arayüzü otomatik web/araç/bellek kullanımını kapatamıyorsa, bu sınırlama run config'te belirtilmeli; aynı profilde kontrollü koşuyla eşdeğer olduğu iddia edilmemeli.

```bash
mkdir -p runs/modelA
cp templates/run_config.json runs/modelA/run_config.json
cp templates/results_text.csv runs/modelA/results_text.csv
```

`run_config.json` dosyasında gerçek model/sürüm, profil, tarih, sampling/reasoning ayarları ve bütçeleri doldur. CSV'deki bütün `REPLACE_MODEL_ID` değerlerini `modelA` ile değiştir. Aynı işlem modelB, modelC için ayrı yapılır. API anahtarı bu dosyalara yazılmaz.

## 3. Bir görevi modele hazırla

```bash
python3 scripts/export_task.py \
  --task T101 \
  --profile text \
  --out ../hep-benchmark-model-inputs/modelA/text/r1/T101
```

Bu klasörde `SYSTEM.txt`, `TASK.md`, gerekiyorsa `assets/` ve dosya hashlerini içeren manifest bulunur. `r1`, birinci bağımsız tekrardır; diğer tekrarlar `r2`, `r3` kullanır. Çıktı klasörü boş olmalı; betik mevcut denemeyi üzerine yazmaz.

Sohbet arayüzünde her görev için yeni, geçmişi olmayan oturum aç. Önce SYSTEM.txt içeriğini, sonra TASK.md içeriğini ve o paketin eklerini ver. API'de SYSTEM.txt sistem mesajı, TASK.md görev mesajı olur; görsel/veri eklerini sağlayıcının desteklediği biçimde ekle. Sistem rolü sunmayan arayüzlerde bu farkı kaydet; API ile tamamen eşdeğer sayma.

**Değerlendirilen modele bütün depoyu veya cevap anahtarını verme.** Dosya sistemine erişen ajan için ayrı kısıtlı çalışma alanına yalnız bu paket kopyalanmalı; depo ve `evaluator/` bağlanmamalı. Bir sibling klasöre export etmek tek başına erişim izolasyonu sağlamaz. İzolasyon ve araç/internet kısıtları kullanılan ajan ortamında uygulanır.

Yanıt metnini değerlendirme tarafında örneğin `runs/modelA/text/r1/T101/response.txt` olarak sakla. Modelin kod/artifact çıktıları ve yürütme logları da aynı trial kimliğiyle saklanır. Bu kayıtlar diğer görevlere verilmez.

Görsel örnek için aynı işlem:

```bash
python3 scripts/export_task.py \
  --task T301 \
  --profile full \
  --out ../hep-benchmark-model-inputs/modelA/full/r1/T301
```

full koşusuna geçildiğinde `results_full.csv` şablonu ve ayrı profile uygun run config kullanılmalıdır.

## 4. Yanıtı değerlendir

Değerlendirici `evaluator/answer_key.jsonl` içindeki ilgili görevi kullanır. Dört kriteri 0/0.5/1 puanlar; her ağırlık 0.25'tir. Kanıt ve kriter puanlarını `templates/rubric_record.json` kopyasında saklar. Kritik kriterlerin tamamı 1 ise `passed=1`, aksi halde 0. `partial_score` ağırlıklı toplamdır.

Kod görevlerinde yalnız örnek çıktı yeterli değildir. Üretilen kod ayrı izole değerlendirme ortamında çalıştırılmalı ve belirtilen ilave durumlarda denenmelidir. T801/T802'nin yürütme/provenance koşulları, kodun gerçekten çalıştığı doğrulanmadan geçilemez. Bu aşama henüz otomatik bir sandbox checker ile paketlenmedi.

CSV'de ilgili `task_id` + `repeat` satırını güncelle:

| Alan | Girilecek değer |
|---|---|
| status | Puanlandıysa `completed`; yanlış bilimsel yanıt da completed olabilir |
| passed | Değerlendiricinin verdiği 0 veya 1 |
| partial_score | Değerlendiricinin ölçütlerden hesapladığı 0–1 puan |
| confidence | Modelin bildirdiği 0–1 güven; yoksa boş |
| wall_seconds | Ölçülen süre; yoksa boş |
| input_tokens, output_tokens | Sağlayıcı/runtime verisi; yoksa boş |
| cost_usd | Gerçek kullanım fiyatından hesaplanan maliyet; bilinmiyorsa boş |
| grader_id | Değerlendiricinin kimliği |
| notes | Hata türü, test kanıtı veya kısıt |

Modelin bütçesi biterse `timeout`, modele atfedilen yanıt başarısızlığında `model_error`; bunlar 0 puandır. Altyapı arızası `infra_error`, henüz çalışılmayan görev `pending` olur ve puan alanları boş kalır. Bu iki durum toplam skoru bloke eder. Eksik maliyeti 0 yazma.

## 5. Aynı işlemi bütün görev ve tekrarlar için yap

text görevleri:

```text
T101 T102 T201 T202 T401 T402 T501 T502 T601 T602 T701 T702
```

tools bunlara T801/T802'yi, full ayrıca T301/T302'yi ekler. full profilinde T601/T602 görsellerden okunur; export betiği doğru istemi seçer. Her görev üç yeni oturumda çalışır; aynı oturumun üç kez devam ettirilmesi tekrar sayılmaz. En iyi cevabı seçme.

## 6. Skorları hesapla

```bash
python3 scripts/score_results.py \
  --tasks public/tasks.jsonl \
  --results runs/modelA/results_text.csv \
  --repeats 3 \
  --out runs/modelA/scores_text.json
```

`status=complete` olduğunda modül puanları, `core_pass_percent` ve varsa `integration_pass_percent` üretilir. `incomplete` varsa eksik/pending/infra satırları tamamlanmalıdır. Kısmi görevler üzerinden toplam oluşturulmaz. ModelB ve modelC için aynı komutu kendi dosyalarıyla çalıştır. Aynı profildeki modül puanlarını ve maliyetleri karşılaştır.

Tek bir arayüzde önce işleyişi denemek için bir görevi çalıştırabilirsin; bu, bütün profil skorunu üretmez. Üç tekrarlı starter sonuçları geliştirme/kalibrasyon içindir; yayımlanacak model üstünlüğü iddiası için bağımsız uzman doğrulaması ve gizli test sürümü gerekir.

`runs/`, yerel ortamlar ve credential dosyaları `.gitignore` ile dışarıda tutulur. Veri/sonuç paylaşımı gerektiğinde neyin gönderileceğine ayrıca karar verilir. Depo ve başlangıç görevlerinin cevap anahtarları artık publictir. Gelecekteki gizli test görevleri/anahtarları bu depoya veya Git geçmişine eklenmemelidir. Bir LLM’e doğrudan depo erişimi vererek yapılan deneme için `SELF_TEST_TR.md` içindeki sınırlamalar geçerlidir.
