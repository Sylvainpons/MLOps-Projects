import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import shutil

load_dotenv()

# ─────────────────────────── CONFIG & UI ───────────────────────────
st.set_page_config(page_title="KVAC Visa Bot", page_icon="South Korea", layout="centered")

st.title("KVAC Paris Visa Assistant")
st.markdown("**Français · English · 한국어** – Posez n’importe quelle question sur vos documents KVAC")

# Bouton re-index
if st.sidebar.button("Re-indexer les PDFs (nouveaux docs ?)"):
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")
    if "vectorstore" in st.session_state:
        del st.session_state.vectorstore
    st.success("Index supprimé → rechargement au prochain message !")
    st.rerun()

# Langue
lang = st.sidebar.radio("Language / 언어 / Langue", ["English", "Français", "한국어"])

# ─────────────────────────── RAG CHAIN (cached) ───────────────────────────
@st.cache_resource
def get_retriever():
    with st.spinner("Chargement et indexation des PDFs... (première fois ~30s)"):
        loader = PyPDFDirectoryLoader("pdfs/")
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        embedding = UpstageEmbeddings(model="solar-embedding-1-large")
        vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embedding,
            persist_directory="./chroma_db"
        )
        return vectordb.as_retriever(search_kwargs={"k": 6})

retriever = get_retriever()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2, streaming=True)

prompt = prompt = ChatPromptTemplate.from_template("""
Vous êtes assistant(e) pour les tâches de réponse aux questions.
Utilisez les éléments de contexte suivants pour répondre à la question.
Si vous ne connaissez pas la réponse, dites simplement que vous ne savez pas.
Répondez de façon concise en trois phrases maximum.

Question: {question}

Context: {context}

Réponse:
""")

def format_docs(docs):
    return "\n\n".join(
        f"**Source : {doc.metadata['source'].split('/')[-1]} – Page {doc.metadata['page']+1}**\n{doc.page_content}"
        for doc in docs
    )

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ─────────────────────────── CHAT ───────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요 ! E-7, D-8, F-2, H-1 등 뭐든 물어보세요. 정확한 페이지 번호와 함께 답변드립니다."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input("Votre question sur le visa Corée..."):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        response = st.write_stream(rag_chain.stream(question))
        
        # Sources magnifiques
        docs = retriever.invoke(question)
        if docs:
            with st.expander(f"Sources ({len(docs)} pages trouvées)", expanded=True):
                for i, doc in enumerate(docs, 1):
                    st.markdown(f"**{i}. {doc.metadata['source'].split('/')[-1]} – Page {doc.metadata['page']+1}**")
                    st.caption(doc.page_content[:800] + ("..." if len(doc.page_content) > 800 else ""))

    st.session_state.messages.append({"role": "assistant", "content": response})