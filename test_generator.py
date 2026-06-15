from ingest import load_and_chunk_all
from retriever import embed_and_store, retrieve
from generator import generate_response

chunks = load_and_chunk_all()
embed_and_store(chunks)

query = "Is Professor Schmitz a tough grader?"
results = retrieve(query)
answer = generate_response(query, results)
print(answer)