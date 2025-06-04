import os
from git import Repo
from langchain.document_loaders import TextLoader

def clone_and_load_repo(repo_url, local_dir="tmp_repo"):
    if os.path.exists(local_dir):
        os.system(f"rm -rf {local_dir}")
    Repo.clone_from(repo_url, local_dir)

    docs = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith((".py", ".js", ".java", ".log", ".txt")):
                path = os.path.join(root, file)
                loader = TextLoader(path)
                docs.extend(loader.load_and_split())
    return docs
