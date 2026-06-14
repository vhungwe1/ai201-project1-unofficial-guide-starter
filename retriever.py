import chromadb
from chromadb.utils import embedding_functions

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_PATH = "./chroma_db"
CHROMA_COLLECTION = "unofficial_guide"
N_RESULTS = 4

_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def embed_and_store(chunks):
    """Embed chunks and store in ChromaDB."""
    _collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"]} for c in chunks],
        ids=[c["chunk_id"] for c in chunks],
    )
    print(f"Stored {_collection.count()} total chunks in vector database.")


def retrieve(query, n_results=N_RESULTS):
    """Find most relevant chunks for a query."""
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i],
        })

    return chunks