# ⚙️ Proje Çalışma Kılavuzu

Bu proje, RAG tabanlı bir Kariyer Asistanı Chatbot'udur. Çalıştırmak için aşağıdaki adımları izleyin.

## 1. Sanal Ortam Kurulumu

Projenin bağımlılıklarını izole etmek için sanal ortam kullanılır.

1.  Proje klasörüne gidin:
    ```bash
    cd Kariyer-Asistani-RAG-Chatbot
    ```
2.  Sanal ortamı oluşturun:
    ```bash
    python -m venv venv
    ```
3.  Sanal ortamı aktive edin:
    * Windows: `venv\Scripts\activate`
    * macOS/Linux: `source venv/bin/activate`

## 2. Bağımlılıkların Kurulumu

1.  `requirements.txt` dosyasındaki tüm kütüphaneleri tek seferde kurun:
    ```bash
    pip install -r requirements.txt
    ```

## 3. API Anahtarı Ayarlama

OpenAI API anahtarınızı (veya kullanacağınız LLM'e ait anahtarı) ortam değişkeni olarak ayarlayın:

* Windows: `set OPENAI_API_KEY="Sizin-Anahtarınız"`
* macOS/Linux: `export OPENAI_API_KEY="Sizin-Anahtarınız"`

## 4. Chatbot'u Çalıştırma

Kodlama tamamlandıktan sonra (Genellikle `app.py` veya `chatbot.py` gibi bir dosya olacaktır):

1.  Arayüzü çalıştırma komutunu girin:
    ```bash
    streamlit run app.py
    ```
2.  Komutun çalışmasıyla tarayıcınızda otomatik olarak açılacak olan yerel adrese gidin (Genellikle: http://localhost:8501).