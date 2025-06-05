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
embeddings = generate_embedding()
db = store_embeddings(all_docs, embeddings)

# Step 3: Load retriever and QA chain
retriever = load_vectorstore("chroma_index", embeddings)
qa_chain = get_qa_chain(retriever)

# Step 4: Ask questions
while True:
    query = input("Ask a question about the code or logs: ")
    if query.lower() in ["exit", "quit"]:
        break
    result = qa_chain({"query": query})
    print("\n--- Answer ---\n")
    print(result["result"])
    print("\n--- Sources ---\n")
    for doc in result['source_documents']:
        print(doc.metadata.get('source', ''))
