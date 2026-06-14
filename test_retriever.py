from ingest import load_and_chunk_all
from retriever import embed_and_store, retrieve

chunks = load_and_chunk_all()
embed_and_store(chunks)

results = retrieve("Is Professor Schmitz a tough grader?")
for r in results:
    print(f"[{r['source']}] (dist: {r['distance']:.3f})")
    print(r['text'][:150])
    print()