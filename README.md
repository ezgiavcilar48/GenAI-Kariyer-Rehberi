# 🎓 Kariyer Asistanı: RAG Tabanlı Öğrenci Rehberlik Chatbot'u

## 🚀 Projenin Amacı

Bu proje, Akbank GenAI Bootcamp kapsamında geliştirilen, **RAG (Retrieval Augmented Generation) temelli** bir kariyere asistanı chatbotudur. Chatbot, özellikle öğrencilere ve yeni mezunlara yönelik olarak;
* Etkili CV hazırlama,
* Başarılı mülakat teknikleri ve ipuçları,
* Uygun staj/iş bulma stratejileri
konularında yapay zekâ destekli rehberlik sunarak bir web arayüzü üzerinden kullanıcıya sunulmayı amaçlamaktadır.

## 💾 Veri Seti Hakkında Bilgi

Proje, öğrencilere ve yeni mezunlara kariyer rehberliği sağlamak amacıyla özel olarak hazırlanmış 3 adet metin dosyası (`.txt`) kullanmaktadır. Bu veri setleri, RAG modelinin bilgi tabanını oluşturmaktadır.

**Veri Seti İçeriği (Ana Konular):**

1.  **CV Hazırlama Kılavuzu:** Etkili iletişim bilgileri, kısa özetin önemi, deneyimleri sayılarla ifade etme ve yetenek listeleme gibi konuları kapsar.
2.  **Staj ve İş Bulma Rehberi:** Profesyonel ağlar (LinkedIn), online platformlar ve başvuru takip stratejilerine odaklanır.
3.  **Mülakat İpuçları:** Mülakat öncesi hazırlık, davranışsal sorular için STAR metodu ve "Bize kendinizden bahseder misiniz?" sorusuna yanıt stratejisi gibi konuları içerir.

**Veri Seti Hazırlama Metodolojisi:**

Bu veri seti, güvenilir kariyer danışmanlığı kaynaklarından **manuel olarak derlenmiş ve projenin odağına uygun** şekilde yapılandırılmıştır. RAG sistemi için **temiz ve hedefe yönelik** (curated) metin belgeleri şeklinde hazırlanmıştır.

## 🛠 Çözüm Mimariniz ve Teknolojiler 

### Mimari Yaklaşım
Bu projenin temel amacı, hazırlanan özel bilgi setine dayalı, güvenilir ve hedefe yönelik cevaplar sunmak için **Retrieval Augmented Generation (RAG)** mimarisini kullanmaktır.

#### RAG Mimarisi Adım Adım Akış
1.  **Veri Hazırlama (Ingestion):** Kariyer rehberliği metinleri, **LangChain** kullanılarak küçük, anlamsal parçalara (chunks) ayrılır.
2.  **Gömme (Embedding) ve Depolama:** Her metin parçası, **Google'ın Embedding Modeli** ile vektörlere dönüştürülür ve **ChromaDB**'ye kaydedilir.
3.  **Geri Çağırma (Retrieval):** Kullanıcı sorusu vektöre dönüştürülerek Vektör Veritabanında en alakalı bilgi parçaları geri çağrılır.
4.  **Üretim (Generation):** Geri çağrılan bilgi ve kullanıcı sorusu, **Gemini API**'a (**Generation Model**) gönderilerek nihai cevap üretilir.

#### Kullanılan Teknolojiler
* **RAG Pipeline Framework:** **LangChain**
* **Generation Model (LLM):** **Gemini API**
* **Vektör Veritabanı:** **ChromaDB**
* **Web Arayüzü:** **Streamlit**

## 💡 Elde Edilen Sonuçlar

Geliştirilen RAG temelli sistem, kullanıcıların spesifik kariyer sorularına hızlı, bağlamsal olarak doğru ve veri setine dayalı cevaplar verebilmektedir. Proje, web arayüzü üzerinden erişilebilir, kullanıcı dostu ve verimli bir kariyer asistanı sunmaktadır.

---

## 🌐 ÇALIŞMA KILAVUZU ve DEPLOY 

### 1. Kodunuzun Çalışma Kılavuzu

Projenin yerel ortamda başarılı bir şekilde çalıştırılabilmesi için gerekenler aşağıda özetlenmiştir.

* **Detaylı Kılavuz:** Tüm sanal ortam (`venv`) kurulumu, bağımlılıkların yüklenmesi ve sorun giderme adımları için lütfen projenin ana dizininde bulunan **(CALISMA_KILAVUZU.md)** dosyasına bakınız.
* **Özet Çalıştırma Adımları:**
    1.  **Bağımlılıklar:** `pip install -r requirements.txt`
    2.  **API Anahtarı:** `export GEMINI_API_KEY="YOUR_API_KEY_HERE"`
    3.  **Veritabanı Oluşturma:** `python setup_rag_db.py`
    4.  **Projenin Başlatılması:** `streamlit run app.py`

### 2. Web Arayüzü & Product Kılavuzu

#### 🎓 Kariyer Asistanı Canlı Linki

Uygulamanın Streamlit Cloud üzerinde dağıtılmış, canlı versiyonudur.

**CANLI LİNK:** [https://genai-kariyer-rehberi.streamlit.app/](https://genai-kariyer-rehberi.streamlit.app/)

#### Kabiliyetlerin Test
### Projenin Kabiliyetlerinin Test Edilmesi

Aşağıdaki senaryolar, chatbotun veri setindeki bilgilere ne kadar doğru ve bağlamsal cevap verdiğini test etmek için kullanılmalıdır. Bu testler, RAG sisteminin doğruluğunu kanıtlar.

#### 1. CV Hazırlama Kabiliyeti Testi
* **Test Sorusu:** "CV'de deneyimleri yazarken sadece görev tanımı yapmak yerine ne yapmalıyım?"
* **Beklenen Cevap:** Cevapta mutlaka, başarıların ve şirkete katılan değeri **sayılarla** ifade eden fiil (action verb) kullanarak yazma önerisi vurgulanmalıdır.

#### 2. Mülakat İpuçları Kabiliyeti Testi
* **Test Sorusu:** "Davranışsal bir soruya (örneğin bir çatışma çözme deneyimi) nasıl cevap vermeliyim?"
***Beklenen Cevap:** Cevap, **STAR metodunun** (Situation, Task, Action, Result) adımları kullanılarak yapılandırılmış bir yanıt stratejisi sunmalıdır.

#### 3. Staj/İş Bulma Kabiliyeti Testi
* **Test Sorusu:** "Başvuru sürecinde takibi kolaylaştırmak ve moralimi yüksek tutmak için ne yapmalıyım?"
***Beklenen Cevap:** Cevap, başvuru yapılan pozisyonları, tarihleri ve geri dönüş durumlarını mutlaka bir **Excel veya Google Sheet tablosunda takip etme** önerisini içermelidir.