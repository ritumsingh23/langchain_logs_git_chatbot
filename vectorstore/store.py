from langchain.vectorstores import Chroma

def store_embeddings(docs, embeddings, persist_path="chroma_index"):
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_path)
    return db
