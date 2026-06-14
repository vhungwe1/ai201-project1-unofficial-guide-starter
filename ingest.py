import os

DOCS_PATH = "documents"

def load_documents():
    """Load all .txt files from the documents folder."""
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt") and filename != ".gitkeep":
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            source_name = filename.replace(".txt", "").replace("_", " ").title()
            documents.append({
                "source": source_name,
                "filename": filename,
                "text": text,
            })
    print(f"Loaded {len(documents)} documents: {[d['source'] for d in documents]}")
    return documents


def chunk_text(text, source, chunk_size=300, overlap=50):
    """Split text into chunks using sliding window."""
    chunks = []
    prefix = source.lower().replace(" ", "_")
    counter = 0
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) >= 50:
            chunks.append({
                "text": chunk,
                "source": source,
                "chunk_id": f"{prefix}_{counter}",
            })
            counter += 1
        start += chunk_size - overlap

    return chunks


def load_and_chunk_all():
    """Load all documents and chunk them."""
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"], doc["source"])
        all_chunks.extend(chunks)
    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks