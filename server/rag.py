import os
import chromadb
from sentence_transformers import SentenceTransformer

# In-process ChromaDB — no server needed
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("icar_advisories")

# Multilingual embeddings for Hindi/Marathi/Bhojpuri
embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def add_documents(texts: list[str], ids: list[str]):
    """Add advisory chunks to ChromaDB."""
    embeddings = embedder.encode(texts).tolist()
    collection.add(documents=texts, embeddings=embeddings, ids=ids)

def retrieve(query: str, top_k: int = 3) -> str:
    """Retrieve top-k relevant advisory chunks for a query."""
    if collection.count() == 0:
        return ""
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    chunks = results["documents"][0]
    return "\n".join(chunks)