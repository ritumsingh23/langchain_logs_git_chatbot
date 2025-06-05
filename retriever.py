import numpy as np
import pymongo
from embedder import generate_embedding

# Initialize Cosmos DB client (MongoDB API)
cosmos_connection_string = "mongodb+srv://fraudstore:hackmongo%401@mongofraudstore.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=true&w=majority&maxIdleTimeMS=120000"
mongo_client = pymongo.MongoClient(cosmos_connection_string)
db = mongo_client["mongofraudstore"]  # e.g., "LogDatabase"
collection = db["testCollection"]  # e.g., "LogEmbeddings"

# Function to compute cosine similarity
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

# Function to retrieve top-k similar documents
def retrieve_similar_documents(query, top_k=3):
    query_embedding = generate_embedding(query)
    if not query_embedding:
        print("Failed to generate query embedding")
        return []

    # Retrieve all documents from Cosmos DB
    documents = []
    try:
        for doc in collection.find({}, {"_id": 1, "file_name": 1, "original_text": 1, "embedding": 1}):
            documents.append(doc)
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return []

    # Compute similarity scores
    similarities = []
    for doc in documents:
        stored_embedding = doc.get("embedding")
        if stored_embedding:
            similarity = cosine_similarity(query_embedding, stored_embedding)
            similarities.append((doc, similarity))

    # Sort by similarity and get top-k
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]
