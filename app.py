import os
from dotenv import load_dotenv
import gradio as gr
from ingest import load_and_chunk_all
from retriever import embed_and_store, retrieve
from generator import generate_response

load_dotenv()

# Load and store documents on startup
print("Loading and indexing documents...")
chunks = load_and_chunk_all()
embed_and_store(chunks)
print("Ready!")


def ask(question):
    """Handle a user query end to end."""
    if not question.strip():
        return "Please enter a question.", ""

    retrieved = retrieve(question)
    if not retrieved:
        return "No relevant information found.", ""

    answer = generate_response(question, retrieved)
    sources = "\n".join(set(f"• {r['source']}" for r in retrieved))
    return answer, sources


with gr.Blocks(title="Babson Unofficial Guide") as demo:
    gr.Markdown("# 🎓 Babson Unofficial Guide\nAsk anything about Babson professors — answers from real student reviews.")

    with gr.Row():
        inp = gr.Textbox(label="Your question", placeholder="e.g. Is Professor Schmitz a tough grader?")

    btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=6)
        sources = gr.Textbox(label="Sources", lines=6)

    btn.click(ask, inputs=inp, outputs=[answer, sources])
    inp.submit(ask, inputs=inp, outputs=[answer, sources])

demo.launch()