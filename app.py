import streamlit as st
import os # Ortam değişkenlerini yönetmek için
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_community.chains import ConversationalRetrievalChain


# --- 1. TEORİK MİMARİ AÇIKLAMASI (PDF'in 4. Adım Gereksinimi) ---

# Bu bölüm, PDF'de istenen "Çözüm Mimarisi"nin (4. Adım) teorik açıklamasını içerir.
# Bu tarz dokümantasyon, teknik anlatımlara notebook içerisinde veya Python dosyasında 
# [cite_start]yorum satırları içerisinde yer verme gereksinimini karşılar[cite: 7].

"""
ÇÖZÜM MİMARİSİ: RAG (Retrieval Augmented Generation)

A. PROBLEM ÇÖZÜMÜ:
Proje, öğrencilerin kariyer konularında (CV, mülakat, staj) sorduğu spesifik sorulara
genel internet bilgisi yerine, **özel olarak beslenmiş** dokümanlar üzerinden
**güvenilir** cevaplar verme problemini çözer. Bu, LLM'lerin halüsinasyon riskini azaltır.

[cite_start]B. KULLANILAN TEKNOLOJİLER[cite: 23, 42, 43, 44]:
1. [cite_start]LLM (Generative Model): ChatOpenAI (Genellikle gpt-3.5-turbo kullanılır) [cite: 42]
2. [cite_start]RAG Framework: LangChain [cite: 44]
3. [cite_start]Embedding Model: Sentence Transformers (Açık Kaynaklı) [cite: 43]
4. [cite_start]Vektör Database: Chroma (Lokal, hafif veritabanı) [cite: 43]
5. Arayüz: Streamlit

C. RAG MİMARİSİ ADIMLARI:
1. Loading (Yükleme): Veri Seti (`data/` klasöründeki .txt dosyaları) yüklenir.
2. Splitting (Bölme): Metinler küçük parçalara (1000 karakter) ayrılır.
3. Embedding (Gömme): Her metin parçası vektöre dönüştürülür.
4. Storage (Depolama): Bu vektörler, hızlı arama için ChromaDB'ye kaydedilir.
5. Retrieval (Geri Çağırma): Kullanıcı sorusuna en alakalı 3 vektör (metin parçası) geri çağrılır.
6. Generation (Üretme): Geri çağrılan parçalar (context) ve soru, LLM'e gönderilerek cevap oluşturulur.
"""
load_dotenv()

# --- 2. VERİ YÜKLEME VE RAG İLK KURULUM FONKSİYONLARI ---

# RAG Sisteminin Hazırlanması
@st.cache_resource # Streamlit'in bu fonksiyonu sadece bir kere çalıştırmasını sağlar
def setup_rag():
    """Veri yükleme, bölme ve ChromaDB'ye kaydetme işlemlerini yapar."""
    
    # 1. Veri Yükleme (Loading)
    try:
        # data klasöründeki tüm .txt dosyalarını yükle
        loader = DirectoryLoader('./data/', glob="**/*.txt", loader_cls=lambda p: TextLoader(p, encoding='utf8'))
        documents = loader.load()
        
    except FileNotFoundError:
        # Eğer veri seti klasörü bulunamazsa hata göster
        st.error("HATA: 'data' klasörü bulunamadı veya içinde .txt dosyası yok. Lütfen kontrol edin.")
        return None
    
    if not documents:
        st.error("HATA: Veri seti yüklenemedi. 'data' klasörünüzün boş olmadığından emin olun.")
        return None
    
    # 2. Metin Parçalama (Splitting)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    texts = text_splitter.split_documents(documents)
    
    # 3. Embedding ve Vektör DB Oluşturma (Embedding & Storage)
    # LangChain ile Sentence Transformer Embeddings kullanıyoruz
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Chroma DB oluşturulur ve metinler vektörleştirilerek DB'ye kaydedilir.
    # persist_directory, veritabanını diske kaydetmeye yarar.
    db = Chroma.from_documents(texts, embeddings, persist_directory="./chroma_db")
    db.persist() 

    # 4. LLM ve Zinciri Kurma
    # Gemini API anahtarının tanımlı olduğundan emin ol
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("HATA: GEMINI_API_KEY ortam değişkeni ayarlanmamış. Lütfen terminalde ayarlayın.")
        return None
    
    #Gemini modelini tanımla

    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.0,
    google_api_key=os.environ.get("GEMINI_API_KEY"))
    retriever = db.as_retriever(search_kwargs={"k": 3}) # En alakalı 3 belgeyi geri getir
    
    # Konuşma tabanlı RAG zincirini kur (Konuşma geçmişini korur)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=retriever, 
        return_source_documents=True,
        # Konuşma geçmişini korumak için bir lambda fonksiyonu
        get_chat_history=lambda h: h 
    )
    
    return qa_chain

# --- 3. STREAMLIT ARABİRİMİ ---

# Sayfa Yapılandırması
st.set_page_config(page_title="🎓 Kariyer Asistanı Chatbot", layout="wide")
st.title("🎓 Kariyer Asistanı: RAG Destekli Chatbot")
st.write("CV hazırlama, mülakat ipuçları ve staj bulma konularında size özel rehberlik sunuyorum.")

# RAG sistemini başlatma kontrolü
if 'qa_chain' not in st.session_state:
    with st.spinner("Kariyer verileri yükleniyor ve RAG sistemi hazırlanıyor..."):
        st.session_state['qa_chain'] = setup_rag()
        st.session_state['chat_history'] = []

qa_chain = st.session_state.get('qa_chain')

# Eğer sistem hatasız kurulduysa devam et
if qa_chain:
    # Kullanıcı girişi
    user_query = st.chat_input("Bir kariyer sorusu sorun (Örn: STAR metodu nedir?).")

    if user_query:
        # Kullanıcı sorusunu ve geçmişi zincire gönder
        with st.spinner("Cevap aranıyor..."):
             # Soruyu zincire gönder
             result = qa_chain.invoke({"question": user_query, "chat_history": st.session_state['chat_history']})
        
        # Yeni konuşmayı geçmişe ekle
        st.session_state['chat_history'].append((user_query, result["answer"]))
        
        # Son cevabın kaynaklarını session state'e kaydet (göstermek için)
        st.session_state['last_result'] = result

    # Sohbet geçmişini gösterme
    for question, answer in st.session_state['chat_history']:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(answer)
            
            # Geri çağrılan kaynakları gösterme (RAG başarısının kanıtı)
            if 'last_result' in st.session_state and st.session_state['chat_history'][-1][1] == answer:
                result = st.session_state['last_result']
                
                if 'source_documents' in result:
                    # Kaynak dosya adlarını al (Sadece dosya adını göster)
                    source_files = [doc.metadata['source'].split(os.path.sep)[-1] for doc in result['source_documents']]
                    unique_sources = list(set(source_files))
                    
                    if unique_sources:
                        st.markdown(f"**Kaynaklar:** {', '.join(unique_sources)}", help="Bu cevabın dayandığı kariyer rehberliği dokümanları.")