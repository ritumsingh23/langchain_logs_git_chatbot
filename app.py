import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import tempfile
import git
import shutil
from ingest.github_loader import clone_and_load_repo
from ingest.log_loader import load_log_files
from vectorstore.embedder import get_embedding_model
from vectorstore.store import store_embeddings
from rag.retriever import load_vectorstore
from rag.qa_chain import get_qa_chain
from dotenv import load_dotenv

load_dotenv()

# Step 1: Load documents
code_docs = clone_and_load_repo("https://github.com/ritumsingh23/expedition-o2-predictor")
log_docs = load_log_files("./log/")
all_docs = code_docs + log_docs

# Step 2: Embed and store
embeddings = get_embedding_model()
db = store_embeddings(all_docs, embeddings)

# Step 3: Load retriever and QA chain
retriever = load_vectorstore("chroma_index", embeddings)
qa_chain = get_qa_chain(retriever)

# Step 4: Ask questions
# while True:
#     query = input("Ask a question about the code or logs: ")
#     if query.lower() in ["exit", "quit"]:
#         break
#     result = qa_chain({"query": query})
#     print("\n--- Answer ---\n")
#     print(result["result"])
#     print("\n--- Sources ---\n")
#     for doc in result['source_documents']:
#         print(doc.metadata.get('source', ''))

# Load environment variables (expects OPENAI_API_KEY in .env)
# load_dotenv()

# Initialize OpenAI LLM and embedding model
# llm = ChatOpenAI(model_name="gpt-4", temperature=0)
# embedding_model = OpenAIEmbeddings()

# Helper to read and embed uploaded file
# def process_file(file):
#     temp_path = os.path.join(tempfile.gettempdir(), file.name)
#     with open(temp_path, "wb") as f:
#         f.write(file.read())
    
#     loader = TextLoader(temp_path)
#     docs = loader.load()
    
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunks = splitter.split_documents(docs)
    
#     db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db")
#     db.persist()
#     return db.as_retriever()

# def clone_and_process_repo(repo_url):
#     temp_repo_dir = os.path.join(tempfile.gettempdir(), "repo")
#     if os.path.exists(temp_repo_dir):
#         shutil.rmtree(temp_repo_dir)
#     git.Repo.clone_from(repo_url, temp_repo_dir)

#     # Load .py, .md, .txt files
#     docs = []
#     for root, dirs, files in os.walk(temp_repo_dir):
#         for file in files:
#             if file.endswith((".py", ".md", ".txt", ".log")):
#                 file_path = os.path.join(root, file)
#                 loader = TextLoader(file_path)
#                 docs.extend(loader.load())

    # Split and embed
    # splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # chunks = splitter.split_documents(docs)
    # db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db")
    # db.persist()
    # return db.as_retriever()

# UI
st.set_page_config(page_title="Code/Log File Chatbot", layout="wide")
st.title("📘 RAG Code/Log QA Bot")

# uploaded_file = st.file_uploader("Upload a log file or source code file", type=["txt", "log", "py", "md"])
user_query = st.text_input("Ask a question about the uploaded file(s):")

# if "retriever" not in st.session_state and uploaded_file:
#     with st.spinner("Processing file and building vector index..."):
#         st.session_state.retriever = process_file(uploaded_file)
#         st.success("Vector DB created successfully.")

print("--------------------------")
print(st.session_state)
print("--------------------------")
print(user_query)

# if user_query and "retriever" in st.session_state:
if user_query:
    print(f"I was here - user {user_query} -------")
    with st.spinner("Thinking..."):
        response = qa_chain({"query": user_query})
        st.markdown("### 💬 Answer")
        st.write(response["result"])

        st.markdown("### 📄 Context")
        for i, doc in enumerate(response["source_documents"]):
            st.markdown(f"**Snippet {i+1}**")
            st.code(doc.page_content[:1000])

# if user_query and "retriever" in st.session_state:
#     with st.spinner("Thinking..."):
#         chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type="stuff",
#             retriever=st.session_state.retriever,
#             return_source_documents=True,
#         )
#         response = chain({"query": user_query})
#         st.markdown("### 💬 Answer")
#         st.write(response["result"])
        
#         st.markdown("### 📄 Context")
#         for i, doc in enumerate(response["source_documents"]):
#             st.markdown(f"**Snippet {i+1}**")
#             st.code(doc.page_content[:1000])

# st.sidebar.markdown("### 📥 GitHub Codebase")
# github_url = st.sidebar.text_input("Paste GitHub Repo URL:")

# if github_url and "retriever" not in st.session_state:
#     with st.spinner("Cloning and processing repo..."):
#         try:
#             st.session_state.retriever = clone_and_process_repo(github_url)
#             st.success("Repository processed successfully.")
#         except Exception as e:
#             st.error(f"Failed to clone or process repo: {e}")

