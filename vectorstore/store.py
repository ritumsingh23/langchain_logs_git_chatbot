from ./embedder import generate_embedding
import pymongo

log_directory = "../log/"

# Function to read log files and store embeddings
def process_and_store_logs(directory):
    # Initialize Cosmos DB client (MongoDB API)
    cosmos_connection_string = "mongodb+srv://fraudstore:hackmongo%401@mongofraudstore.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=true&w=majority&maxIdleTimeMS=120000"
    mongo_client = pymongo.MongoClient(cosmos_connection_string)
    db = mongo_client["mongofraudstore"]  # e.g., "LogDatabase"
    collection = db["testCollection"]  # e.g., "LogEmbeddings"

    for filename in os.listdir(directory):
        if filename.endswith((".txt", ".log")):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                # Truncate content if too long to avoid token limits
                content = content  # Adjust based on model limits

                # print(content)

                # Generate embedding
                embedding = generate_embedding(content)
                # print(embedding)
                if embedding:
                    # Create document for Cosmos DB
                    document = {
                        "file_name": filename,
                        "original_text": content,
                        "embedding": embedding,
                        "timestamp": datetime.utcnow().isoformat(),
                        "id": f"{filename}{datetime.utcnow().isoformat()}"  # Unique ID
                    }
                    try:
                        # Insert into Cosmos DB
                        collection.insert_one(document)
                        print(f"Stored embedding for {filename}")
                    except Exception as e:
                        print(f"Error storing embedding for {filename}: {e}")

# Process logs and store embeddings
process_and_store_logs(log_directory)
