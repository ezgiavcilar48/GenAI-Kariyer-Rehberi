import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


# Sabitler
CHROMA_PATH = "chroma_db"
PROJECT_NAME = "Kariyer Asistanı Chatbotu"

# !!! API ANAHTARINIZI BURAYA YAZIN !!! 
GEMINI_API_KEY_LOCAL = "AIzaSyB_ZHXZq4FX-PRHeH6A_oFoUC2w-SC4qYY" 

# Streamlit arayüzünün başlıklarını ayarlar
st.set_page_config(page_title=PROJECT_NAME, page_icon="💼")
st.title(f"💼 {PROJECT_NAME}")

# Oturum durumunu (Session State) kullanarak sohbet geçmişini başlatır
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# --- Fonksiyonlar ---

def initialize_rag_chain():
    """RAG zincirini ve bileşenlerini (LLM, DB, Memory) yükler ve oluşturur."""
        
    try:
        # 1. Embedding Modelini Yükle (Anahtar doğrudan veriliyor)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="text-embedding-004",
            google_api_key=GEMINI_API_KEY_LOCAL
        )
        
        # 2. ChromaDB Veritabanını Yükle
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        
        # 3. LLM (Generation Model) Yükle (Anahtar doğrudan veriliyor)
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0.2,
            google_api_key=GEMINI_API_KEY_LOCAL
        )
        
        # 4. Sohbet Hafızasını (Memory) Oluştur
        memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True, 
            output_key='answer'
        )

        # 5. RAG Zincirini Oluştur
        rag_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(), 
            memory=memory,
            return_source_documents=False,
            verbose=False
        )
        return rag_chain
    
    except Exception as e:
        # Hata durumunda (örneğin DB oluşturulmamışsa)
        st.error(f"Uygulama başlatılamadı. Veritabanının ({CHROMA_PATH}) oluşturulduğundan emin olun. Hata: {e}")
        return None

# RAG zincirini Streamlit'in önbelleğine alır
rag_chain = st.cache_resource(initialize_rag_chain)()

# --- Arayüz ve Kullanıcı Etkileşimi ---

# Sohbet geçmişini arayüzde gösterir
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan gelen girişi alır ve işler
if user_query := st.chat_input("Kariyer yolculuğun hakkında bir soru sor..."):
    
    # Kullanıcı mesajını geçmişe ekler ve arayüzde gösterir
    st.session_state["chat_history"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # RAG zinciri mevcutsa devam eder
    if rag_chain:
        with st.spinner("Kariyer asistanı yanıt hazırlıyor..."):
            try:
                # RAG zincirini çalıştırır
                response = rag_chain.invoke({"question": user_query})
                
                # Modelden gelen yanıtı alır
                assistant_response = response["answer"]
                
                # Asistan yanıtını geçmişe ekler ve arayüzde gösterir
                st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})
                with st.chat_message("assistant"):
                    st.markdown(assistant_response)

            except Exception as e:
                # LLM veya API hatası yakalanırsa
                error_msg = f"Yanıt oluşturulurken bir sorun oluştu. Hata: {e}"
                st.session_state["chat_history"].append({"role": "assistant", "content": error_msg})
                with st.chat_message("assistant"):
                    st.error(error_msg)
    else:
        # RAG zinciri başlatılamadıysa uyarı gösterir
        with st.chat_message("assistant"):
            st.warning("Chatbot sistemi hazır değil. Lütfen kurulum adımlarını kontrol edin.")