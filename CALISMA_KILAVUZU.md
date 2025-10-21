# ⚙️ KARIYER ASİSTANI - DETAYLI ÇALIŞMA KILAVUZU

Bu kılavuz, GenAI-Kariyer-Rehberi projesinin yerel ortamda başarılı bir şekilde kurulması ve çalıştırılması için gereken tüm adımları içermektedir.

## 1. Ön Koşullar

Projenin başarıyla çalışması için sisteminizde aşağıdaki yazılımlar kurulu olmalıdır:

* **Python:** Sürüm 3.8 veya üzeri.
* **Git:** Proje dosyalarını klonlamak için.
* **Gemini API Anahtarı:** Google AI Studio üzerinden alınmış aktif bir API anahtarı.

## 2. Projenin Kurulumu

### Adım 2.1: Depoyu Klonlama ve Sanal Ortam Oluşturma

1.  **Depoyu Klonlayın:** Projenin GitHub deposunu yerel diskinize kopyalayın.

    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/GenAI-Kariyer-Rehberi.git](https://github.com/KULLANICI_ADINIZ/GenAI-Kariyer-Rehberi.git)
    cd GenAI-Kariyer-Rehberi
    ```

2.  **Sanal Ortam Oluşturma:** Projenin bağımlılıklarının sistemdeki diğer projelerle çakışmaması için bir sanal ortam oluşturun.

    ```bash
    python -m venv venv
    ```

3.  **Sanal Ortamı Aktifleştirme:**

    ```bash
    # Linux/macOS için:
    source venv/bin/activate
    
    # Windows (PowerShell) için:
    .\venv\Scripts\activate
    ```

### Adım 2.2: Bağımlılıkları Yükleme

1.  **`requirements.txt` ile Kütüphaneleri Yükleme:** Sanal ortam aktifken, gerekli tüm Python kütüphanelerini yükleyin.

    ```bash
    pip install -r requirements.txt
    ```

### Adım 2.3: API Anahtarını Ayarlama (ZORUNLU)

Proje, Gemini API'yi kullanmaktadır. LLM'in ve Embedding modellerinin çalışması için API anahtarınızın ortam değişkeni olarak ayarlanması gerekir.

1.  **Anahtarı Ortam Değişkeni Olarak Tanımlama:**

    ```bash
    # Linux/macOS için:
    export GEMINI_API_KEY="SİZİN_API_ANAHTARINIZ"

    # Windows (PowerShell) için:
    $env:GEMINI_API_KEY="SİZİN_API_ANAHTARINIZ"
    ```

## 3. Projenin Çalıştırılması

Proje, iki aşamada çalıştırılır: Önce veri tabanının oluşturulması, sonra uygulamanın başlatılması.

### Adım 3.1: Vektör Veritabanını Oluşturma

Bu adım, `data/` klasöründeki kariyer rehberliği metinlerini okur, vektörlere dönüştürür ve **`chroma_db`** klasörüne kaydeder. **Bu adımı sadece bir kez çalıştırmalısınız.**

1.  **Çalıştırma Komutu:**

    ```bash
    python setup_rag_db.py
    ```

2.  **Beklenen Çıktı:** Komutun sonunda `Vektör veritabanı başarıyla oluşturuldu/güncellendi.` mesajını görmelisiniz.

### Adım 3.2: Streamlit Uygulamasını Başlatma

Veritabanı oluşturulduktan sonra, web arayüzünü başlatın:

1.  **Çalıştırma Komutu:**

    ```bash
    streamlit run app.py
    ```

2.  **Erişim:** Uygulama otomatik olarak tarayıcınızda açılacaktır (Genellikle `http://localhost:8501`).

## 4. Sorun Giderme (Troubleshooting)

* **`UnicodeDecodeError`:** Eğer metin dosyalarını yüklerken bu hatayı alırsanız, `setup_rag_db.py` dosyasındaki `TextLoader`'ın `encoding='utf-8'` kullandığından emin olun.
* **`DefaultCredentialsError`:** Bu, API anahtarınızın doğru ayarlanmadığı anlamına gelir. Lütfen 2.3. adımı tekrar kontrol edin ve anahtarınızı tırnak içinde doğru bir şekilde yazdığınızdan emin olun.
* **API Hataları (400, 404):** Yeni bir API anahtarı alın ve 2.3. adımı tekrarlayın. Ayrıca, `setup_rag_db.py` ve `app.py` dosyalarındaki model isimlerinin Google API ile uyumlu olduğundan emin olun.