<!-- Updated: 2026-09-21T21:37:15+00:00; optional second-stage self-grading -->
<!-- Created: 2026-09-21T20:03:53+00:00 -->
# Bir LLM'e depoyu verip kendini sınatmak

Depo: https://github.com/isildakbora/hep-research-benchmark

Depoyu okuyabilen bir LLM veya kod ajanıyla geliştirme denemesi yapılabilir. Link vermek, modelin tüm dosyaları veya görselleri gerçekten okuyabildiğini garanti etmez; erişemediği girdileri açıkça belirtmelidir. Mevcut sürüm otomatik model API koşucusu değildir. `score_results.py` yalnız dışarıdan verilen puanları toplar.

## Kopyalanabilir ilk deneme istemi

```text
Bu depodaki açık başlangıç görevleri üzerinde geliştirme amaçlı bir deneme yap:
https://github.com/isildakbora/hep-research-benchmark

Bu bir kör benchmark veya yayımlanabilir model karşılaştırması değildir.
1. README.md ve RUN_GUIDE_TR.md ile profil kurallarını öğren. Çözerken evaluator/, tests/, referans çözümler ve önceki sonuçları okuma. Bunlardan birini gördüysen bunu kaydet; temiz değerlendirme iddia etme.
2. İlk denemede text profilini seç: public/prompts/text/ altındaki 12 görevi bir kez yanıtla. Yalnız ilgili görev metnini kullan; problem çözerken hesaplama, kod yürütme veya web araması kullanma. Dosya yüklemek hazırlık işlemidir. Kod çıktılarının elle hesaplandığını açıkça yaz.
3. Her görev için mümkünse yeni ve bağımsız oturum kullan. Bunu yapamıyorsan aynı bağlamda toplu/tek geçişli yanıt olduğunu belirt; bağımsız tekrarlar uydurma.
4. Yanıtları task_id ile ayrı kaydet, her yanıtın sonunda 0–1 güven belirt. Ulaşamadığın görevleri, eksik girdileri ve araç/profil sapmalarını açıkla. Yanıtları tamamladıktan sonra sabitle ve puanlama sırasında değiştirme.
5. Bu aşamada yalnız yanıtları ve koşu kaydını teslim et; kendi beyanını doğrulanmış skor olarak sunma. Model kimliğini, sürümünü, süreyi, token kullanımını veya çalıştırılmış testleri bilmiyorsan uydurma.
```

Bu istemle `text` profilinde 12 yanıt alınır; standart önerideki üç tekrar tamamlanmış olmaz. Bir asistanı yalnız metin profiline uygun kullanamıyorsanız elde edilen çıktıyı standart text koşusu gibi etiketlemeyin. `tools` ve `full` için izin verilen araçlar, ekler ve görev kapsamı `RUN_GUIDE_TR.md` içindedir.

## Puanlama nasıl yapılır?

Yanıtlar tamamlanıp sabitlendikten sonra aynı modelle ikinci aşamaya geçmek için **[öz puanlama promptunu](SELF_GRADING_TR.md)** verin. Bu isteğe bağlı akış yanıt üretiminden sonra başlar; çıktısı öz değerlendirme olarak kaydedilir. Aşağıdaki ayrı değerlendirici akışı bağımsız puanlama içindir.

Yanıtlar sabitlendikten sonra ayrı değerlendirici, `evaluator/answer_key.jsonl` rubriğini kullanır; kod yanıtlarını ayrı ortamda çalıştırır ve kanıtları kaydeder. Aynı LLM'in kendi cevabını puanlaması yalnız öz değerlendirmedir. Ayrı LLM hakem de insan uzman doğrulamasının yerine geçmez.

Tek geçişli denemede sonuç CSV'si her text görevi için yalnız `repeat=1` satırını içermelidir. Üç tekrarlı şablonun diğer tekrarlarını yapılmış gibi doldurmayın. Dışarıda puanlanmış 12 satır hazır olduğunda:

```bash
python3 scripts/score_results.py   --tasks public/tasks.jsonl   --results runs/modelA/results_text_once.csv   --repeats 1   --out runs/modelA/scores_text_once.json
```

Toplamanın `complete` dönmesi, yalnız seçilen tekrar sayısı için tabloyu tamamladığınızı gösterir; koşunun kör, bağımsız veya bilimsel olarak doğrulanmış olduğunu göstermez.

## Yayın için gereken ayrım

Cevap anahtarı açık olduğu için modele yalnız “okuma” demek erişim izolasyonu sağlamaz. Üstelik anahtarın kopyaları ileride internette veya eğitim verisinde bulunabilir. Açık starter görevler geliştirme/kalibrasyon içindir; burada ilk kez denenmek, görevin daha önce görülmediğini kanıtlamaz.

Kontrollü değerlendirmede hazırlık süreci depoyu okur ve `export_task.py` ile yalnız tek görevin girdilerini çıkarır. Aday model ayrı, kısıtlı ortamda sadece bu paketi görür; değerlendirme deposuna, cevap anahtarlarına, testlere ve internete erişmez. Aday oturumlar görev/tekrar arasında paylaşılmaz. Paket dışa aktarma betiği bu izolasyonu kendisi uygulamaz.

Makalede model karşılaştırması için ayrıca insan uzmanlarca doğrulanmış, aday modellerden gizli tutulmuş yeni test görevleri; sabit bütçeler; kayıtlı model/ajan ayarları ve bağımsız puanlama gerekir. Henüz böyle bir gizli test sürümü veya otomatik API koşucusu bu depoda yoktur. Gizli görevler ve anahtarlar ayrı erişim kontrollü depoda tutulmalı; public Git geçmişine hiç eklenmemelidir.
