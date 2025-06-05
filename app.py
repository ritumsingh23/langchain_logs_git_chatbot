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
# from ingest.github_loader import clone_and_load_repo
# from ingest.log_loader import load_log_files
from qa_chain import response_output
from dotenv import load_dotenv

load_dotenv()

# UI
st.set_page_config(page_title="Code/Log File Chatbot", layout="wide")
st.title("📘 RAG Code/Log QA Bot")

# uploaded_file = st.file_uploader("Upload a log file or source code file", type=["txt", "log", "py", "md"])
user_query = st.text_input("Ask a question about the uploaded file(s):")

# if user_query and "retriever" in st.session_state:
if user_query:
    print(f"I was here - user {user_query} -------")
    with st.spinner("Thinking..."):
        # response = response_output({"query": user_query})
        response = response_output(user_query)
        st.markdown("### 💬 Answer")
        print(response)
        st.write(response)

        # st.markdown("### 📄 Context")
        # for i, doc in enumerate(response["source_documents"]):
        #     st.markdown(f"**Snippet {i+1}**")
        #     st.code(doc.page_content[:1000])

