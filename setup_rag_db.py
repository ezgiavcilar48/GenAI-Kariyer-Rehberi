import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Sabitler
CHROMA_PATH = "chroma_db"
DATA_PATH = "data"

# !!! API ANAHTARINIZI BURAYA YAZIN !!! 
# Ortam değişkeni sorununu kesin çözmek için koda gömülmüştür.
GEMINI_API_KEY_LOCAL = "AIzaSyB_ZHXZq4FX-PRHeH6A_oFoUC2w-SC4qYY" 

def load_documents():
    """data/ klasöründeki tüm .txt dosyalarını UTF-8 kodlamasıyla yükler."""
    print("1. Veri dosyaları yükleniyor...")
    
    # Türkçe karakter hatasını çözmek için encoding="utf-8" kullanılır.
    loader = DirectoryLoader(
        DATA_PATH, 
        glob="**/*.txt", 
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}  
    )
    documents = loader.load()
    print(f"Yüklenen belge sayısı: {len(documents)}")
    return documents

def split_text(documents):
    """Yüklenen belgeleri küçük, anlamlı parçalara (chunks) böler."""
    print("2. Metin parçalara ayrılıyor (Chunking)...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200, 
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Oluşturulan parça sayısı (Chunks): {len(chunks)}")
    return chunks

def create_database(chunks):
    """Parçaları vektörleştirir ve ChromaDB'ye kaydeder."""
    print("3. Vektör Gömme (Embedding) işlemi başlatılıyor...")
    
    # API Anahtarını doğrudan koda geçirerek Embedding başlatılır.
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GEMINI_API_KEY_LOCAL
    )
    
    # ChromaDB veritabanını oluşturur veya varsa yükler
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    # Veritabanının diske yazılmasını sağlar
    db.persist()
    print(f"4. {len(chunks)} parça {CHROMA_PATH} klasörüne kaydedildi.")
    print("Vektör veritabanı başarıyla oluşturuldu/güncellendi.")

def main():
    # 1. Dokümanları yükle
    documents = load_documents()
    # 2. Metni parçalara ayır
    chunks = split_text(documents)
    # 3. Vektör veritabanını oluştur ve kaydet
    create_database(chunks)

if __name__ == "__main__":
    main()