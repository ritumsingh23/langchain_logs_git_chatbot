from openai import AzureOpenAI
import pymongo
import os
from datetime import datetime

# Function to generate embeddings
def generate_embedding(text, model="text-embedding-3-large"):  # e.g., "text-embedding-ada-002"

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint="https://bh-us-openai-404fraudnotfound.openai.azure.com/",
        api_key="ae2700bd11b045198da43944f7a38705",
        api_version="2024-12-01-preview"  # Use the appropriate API version
    )

    cosmos_connection_string = "mongodb+srv://fraudstore:hackmongo%401@mongofraudstore.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=true&w=majority&maxIdleTimeMS=120000"
    mongo_client = pymongo.MongoClient(cosmos_connection_string)
    db = mongo_client["mongofraudstore"]  # e.g., "LogDatabase"
    collection = db["testCollection"]  # e.g., "LogEmbeddings"
    try:
        response = client.embeddings.create(
            model=model,
            input=text
        )
        # print(response)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
