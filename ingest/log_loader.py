from langchain.document_loaders import TextLoader
import os

def load_log_files(log_dir):
    docs = []
    for file in os.listdir(log_dir):
        if file.endswith(".log") or file.endswith(".txt"):
            loader = TextLoader(os.path.join(log_dir, file))
            docs.extend(loader.load_and_split())
    return docs
