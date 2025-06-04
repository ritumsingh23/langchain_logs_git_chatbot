from langchain.vectorstores import Chroma

def load_vectorstore(persist_path, embeddings):
    db = Chroma(persist_directory=persist_path, embedding_function=embeddings)
    return db.as_retriever()  # ✅ This is what RetrievalQA expects
