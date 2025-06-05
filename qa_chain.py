from openai import AzureOpenAI
import pymongo
import os
from datetime import datetime
from retriever import retrieve_similar_documents
# Initialize Cosmos DB client (MongoDB API)
cosmos_connection_string = "mongodb+srv://fraudstore:hackmongo%401@mongofraudstore.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=true&w=majority&maxIdleTimeMS=120000"
mongo_client = pymongo.MongoClient(cosmos_connection_string)
db = mongo_client["mongofraudstore"]  # e.g., "LogDatabase"
collection = db["testCollection"]  # e.g., "LogEmbeddings" 

# Function to generate LLM response
def generate_llm_response(query, context_docs, model="gpt-4o-2", max_retries=3):  
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint="https://bh-us-openai-404fraudnotfound.openai.azure.com/",
        api_key="ae2700bd11b045198da43944f7a38705",
        api_version="2024-12-01-preview"  # Use the appropriate API version
    )

    # Construct prompt with context
    context = "\n".join([f"File: {doc['file_name']}\nContent: {doc['original_text'][:1000]}" for doc, _ in context_docs])
    prompt = f"""
    You are an AI assistant analyzing log files. Based on the following context from relevant log files, answer the query.

    *Context*:
    {context}

    *Query*: {query}

    *Task*: Provide a succinct answer with thorough analysis of the file.
    """

    for attempt in range(max_retries):
        try:
            print("------**")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant analyzing logs."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0
            )
            print(response.choices[0].message.content)
            return response.choices[0].message.content
        except RateLimitError as e:
            if attempt == max_retries - 1:
                print(f"Rate limit exceeded after {max_retries} attempts: {e}")
                return None
            wait_time = 60 * (2 ** attempt)
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return None
    return None


def response_output(query):
    # Example: Process a query
    top_docs = retrieve_similar_documents(query, top_k=3)

    if top_docs:
        print("Top matching documents:")
        for doc, score in top_docs:
            print(f"File: {doc['file_name']}, Similarity: {score:.4f}")

        # Generate LLM response
        response = generate_llm_response(query, top_docs)
        if response:
            print("\nLLM Response:")
            return response
        else:
            print("Failed to generate LLM response")
            return "Failed to generate LLM response"
    else:
        print("No relevant documents found")
        return "No relevant documents found"

if __name__ == "__main__":
    response_output("How many error are present?")

# # Close MongoDB connection
# mongo_client.close()
