import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
LLM_MODEL = "llama-3.3-70b-versatile"


def generate_response(query, retrieved_chunks):
    """Generate a grounded answer from retrieved chunks."""
    if not retrieved_chunks:
        return "I couldn't find anything relevant in the loaded documents. Try rephrasing your question."

    # Format retrieved chunks into context block
    context = ""
    for chunk in retrieved_chunks:
        context += f"[Source: {chunk['source']}]\n{chunk['text']}\n\n"

    # Call Groq LLM with grounding instruction
    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that answers questions about Babson College professors. "
                    "Answer using ONLY the review text provided below. "
                    "Do not draw on outside knowledge. "
                    "Always state which professor your answer is about. "
                    "If the answer is not in the provided text, say so explicitly — do not guess."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {query}\n\nReview text:\n{context}",
            },
        ],
    )

    return response.choices[0].message.content