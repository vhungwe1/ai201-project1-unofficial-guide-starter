# The Unofficial Guide — Project 1

---

## Domain

Student reviews of Babson College professors collected from Rate My Professors. This knowledge is valuable because official course catalogs and syllabi don't tell students what professors are actually like to learn from — how hard their exams are, whether participation is graded heavily, or whether the workload is manageable. Students rely on word of mouth and review sites to make informed course selection decisions, but this information is scattered and hard to search.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors | Professor reviews | documents/prof_paul_schmitz.txt |
| 2 | Rate My Professors | Professor reviews | documents/prof_paul_schmitz.txt |
| 3 | Rate My Professors | Professor reviews | documents/prof_paul_schmitz.txt |
| 4 | Rate My Professors | Professor reviews | documents/prof_lee_gustafson.txt |
| 5 | Rate My Professors | Professor reviews | documents/prof_lee_gustafson.txt |
| 6 | Rate My Professors | Professor reviews | documents/prof_lee_gustafson.txt |
| 7 | Rate My Professors | Professor reviews | documents/prof_vincent_onyemah.txt |
| 8 | Rate My Professors | Professor reviews | documents/prof_vincent_onyemah.txt |
| 9 | Rate My Professors | Professor reviews | documents/prof_kandice_hauf.txt |
| 10 | Rate My Professors | Professor reviews | documents/prof_kandice_hauf.txt |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** Each professor review is short (2-5 sentences). A 300-character chunk is large enough to contain one complete review thought without cutting it in half, but small enough to return targeted results for specific questions. Overlap of 50 characters ensures that if a key opinion spans a chunk boundary, it still appears intact in at least one chunk.

**Final chunk count:** 18 chunks across 4 documents

---

## Sample Chunks

| # | Source document | Chunk text |
|---|----------------|------------|
| 1 | prof_paul_schmitz.txt | Professor: Paul Schmitz. Course: SES. School: Babson College. Review 1: Great professor. Really knows a lot about his material. Can be lecture-heavy at times, but classes are always discussion-oriented. |
| 2 | prof_paul_schmitz.txt | He is a great professor, very energetic and makes class interesting. However he is quite a tough grader and gives a lot of content to read. Beware of his pop quizzes. No midterms, very tough final. |
| 3 | prof_lee_gustafson.txt | Professor Gustafson is super funny and keeps things engaging. As long as you do the pre work and participate, an A is very doable. There is extra credit and a group project in the second half. |
| 4 | prof_vincent_onyemah.txt | Vini is an AMAZING, funny guy and his classes are undoubtedly engaging. However, his grading policy is VERY heavy on participation. Be prepared to speak up every single class. |
| 5 | prof_kandice_hauf.txt | She gives a lot of work and rarely gives above 90s on papers. Her exams are very easy but the class requires a lot of work and gives ALOT of readings and an assignment online for every class. |

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key needed)

**Production tradeoff reflection:** For a production system I would consider text-embedding-3-small from OpenAI for higher accuracy on domain-specific text. However it costs money per token. all-MiniLM-L6-v2 is free and runs locally with no rate limits, making it ideal for this project. For a multilingual student body, a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would be worth exploring. Context length is also a consideration — all-MiniLM-L6-v2 handles up to 256 tokens which is sufficient for short reviews but would be limiting for longer documents.

---

## Retrieval Test Results

**Query 1:** Is Professor Schmitz a tough grader?

Top returned chunks:
- [Prof Paul Schmitz] (dist: 0.215) — chunk about tough finals and detailed pop quizzes
- [Prof Lee Gustafson] (dist: 0.506) — loosely related chunk about homework load
- [Prof Paul Schmitz] (dist: 0.509) — chunk with general Schmitz introduction
- [Prof Paul Schmitz] (dist: 0.528) — chunk about pre-class readings

Relevance explanation: The top result (distance 0.215) is highly relevant — it directly mentions Schmitz's tough exams and pop quizzes. The other results are weaker matches pulled in because of the small corpus size.

---

**Query 2:** Does Vincent Onyemah grade heavily on participation?

Top returned chunks:
- [Prof Vincent Onyemah] — chunk stating grading policy is VERY heavy on participation
- [Prof Lee Gustafson] — loosely related chunk about homework and group work
- [Prof Paul Schmitz] — chunk about readings and participation

Relevance explanation: The top chunk is directly relevant — it contains the exact phrase "VERY heavy on participation" and explains students must speak up every class. The other chunks are weaker matches from the small corpus.

---

**Query 3:** What do students say about Lee Gustafson's teaching style?

Top returned chunks:
- [Prof Lee Gustafson] — chunk saying he only talks but nothing about marketing comes out
- [Prof Lee Gustafson] — chunk saying he is super funny and keeps things engaging
- [Prof Paul Schmitz] — loosely related chunk about teaching style

Relevance explanation: Both top chunks are directly relevant and show the mixed reviews about Gustafson — one negative and one positive. This is good retrieval because it captures both perspectives students have expressed.

---

## Grounded Generation

**System prompt grounding instruction:** "You are a helpful assistant that answers questions about Babson College professors. Answer using ONLY the review text provided below. Do not draw on outside knowledge. Always state which professor your answer is about. If the answer is not in the provided text, say so explicitly — do not guess."

**How source attribution is surfaced in the response:** The retrieved chunk sources are displayed in a separate Sources field in the UI, listing each professor whose reviews were retrieved. The LLM is also instructed to name the professor in its response.

---

## Example Responses

**Grounded response 1**

Query: Is Professor Schmitz a tough grader?

Response: My answer is about Professor Schmitz. According to the review text, Professor Schmitz has "tough final" exams and his "exam questions are tough" in his SES class, which suggests that he may be a tough grader.

Source attribution: Prof Paul Schmitz

---

**Grounded response 2**

Query: Does Vincent Onyemah grade heavily on participation?

Response: According to Review 1, Professor Vincent Onyemah grades heavily on participation. The review states that his grading policy is "VERY heavy on participation" and that students should "be prepared to speak up every single class" to do well.

Source attribution: Prof Vincent Onyemah

---

**Out-of-scope query**

Query: What is the best restaurant near Babson?

System response: The review text does not mention any information about restaurants near Babson College for any of the professors mentioned, including Vincent Onyemah, Kandice Hauf, Lee Gustafson, or Paul Schmitz.

---

## Query Interface

**Input fields:** A single text box labeled "Your question" where the user types a question about Babson professors.

**Output format:** Two text boxes — "Answer" showing the grounded response from the LLM, and "Sources" listing which professor reviews were retrieved to generate the answer.

---

**Sample Interaction Transcript**

> **User:** Does Kandice Hauf give easy exams?

> **System:** According to Review 2, Professor Kandice Hauf's exams are very easy. Additionally, Review 2 and another review mention that her pop quizzes are easy as well.

> **Sources:** Prof Kandice Hauf, Prof Paul Schmitz

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is Professor Schmitz a tough grader? | Yes — tough final, detailed pop quizzes | Correctly identified tough finals and pop quizzes | Relevant | Accurate |
| 2 | Does Vincent Onyemah grade heavily on participation? | Yes — tracks participation every class | Correctly stated grading is VERY heavy on participation | Relevant | Accurate |
| 3 | What do students say about Lee Gustafson's teaching style? | Mixed — some find him engaging, others don't learn | Correctly presented both positive and negative reviews | Relevant | Accurate |
| 4 | Does Kandice Hauf give easy exams? | Yes — exams are easy but papers rarely get above 90s | Correctly identified easy exams and pop quizzes | Relevant | Accurate |
| 5 | Which Babson professor is most enthusiastic? | Vincent Onyemah | Incorrectly attributed the quote to Lee Gustafson | Partially relevant | Partially inaccurate |

---

## Failure Case Analysis

**Question that failed:** Which Babson professor is most enthusiastic?

**What the system returned:** The system said Lee Gustafson is the most enthusiastic professor, quoting "Extremely enthusiastic and energy fills the room."

**Root cause (tied to a specific pipeline stage):** This is a chunking failure. The quote "Extremely enthusiastic and energy fills the room" was separated from the chunk containing Vincent Onyemah's name due to the 300-character chunk boundary. When the chunk was retrieved, it did not contain enough context identifying which professor it was about, so the LLM could not correctly attribute the quote.

**What you would change to fix it:** Increase chunk size to 500 characters so each chunk is more likely to contain both the professor's name and the review content together. Alternatively, add professor name as a metadata field that gets injected into every chunk's text prefix.

---

## Spec Reflection

**One way the spec helped you during implementation:** The chunking strategy section of planning.md forced me to think about chunk size before writing any code. Deciding on 300 characters with 50 overlap upfront meant I didn't have to make those decisions mid-implementation, and I had a clear target to verify against when I printed sample chunks.

**One way your implementation diverged from the spec, and why:** The spec anticipated cleaner source attribution, but the implementation sometimes retrieves chunks from professors unrelated to the query because the corpus is small (only 18 chunks). With a larger document collection, retrieval would be more precise and sources would better match the query.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md and document structure (short professor reviews in .txt files)
- *What it produced:* A chunk_text() function using 300-character sliding window with 50-character overlap
- *What I changed or overrode:* I verified the chunk count (18 chunks) and printed sample chunks to confirm they were self-contained before moving on

**Instance 2**

- *What I gave the AI:* My grounding requirement — answer only from retrieved context, cite professor name as source
- *What it produced:* A generate_response() function with a system prompt prohibiting outside knowledge
- *What I changed or overrode:* I tested the out-of-scope question "What is the best restaurant near Babson?" to verify the system refused to answer rather than hallucinating, confirming the grounding instruction worked