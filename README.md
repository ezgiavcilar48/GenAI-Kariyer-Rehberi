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

## 🛠 Çözüm Mimariniz ve Teknolojiler (Adım 4)

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

## 💡 Elde Edilen Sonuçlar Özet

Geliştirilen RAG temelli sistem, kullanıcıların spesifik kariyer sorularına hızlı, bağlamsal olarak doğru ve veri setine dayalı cevaplar verebilmektedir. Proje, web arayüzü üzerinden erişilebilir, kullanıcı dostu ve verimli bir kariyer asistanı sunmaktadır.

---

## 🌐 ÇALIŞMA KILAVUZU ve DEPLOY (Adım 3 & Adım 5)

### 1. Kodunuzun Çalışma Kılavuzu

Projenin yerel ortamda başarılı bir şekilde çalıştırılabilmesi için gerekenler aşağıda özetlenmiştir.

* **Detaylı Kılavuz:** Tüm sanal ortam (`venv`) kurulumu, bağımlılıkların yüklenmesi ve sorun giderme adımları için lütfen projenin ana dizininde bulunan **[SETUP_GUIDE.md](SETUP_GUIDE.md)** dosyasına bakınız.
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