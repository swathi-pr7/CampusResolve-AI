# Demonstration and viva
## 4–5 minute demonstration
1. Explain the problem: fragmented student policies and unsupported chatbot answers.
2. Open the app and show synthetic data warning. Select Live Gemini and enter your key privately for actual LLM generation.
3. Ask “How do I get an internship NOC?” Show answer, cited source and similarity score.
4. Ask “How to bake a chocolate cake?” Show abstention; no LLM call is made when retrieval finds no evidence.
5. Draft a grievance: “I paid my fees twice and have both receipts.” Show department suggestion, editable draft and download.
6. Upload a text-based official circular (with permission), disable sample data, and ask a question about it.
7. Run the evaluation tab and explain errors and limitations honestly.

## Viva questions
- What is GenAI? AI that generates new content, such as answers or grievance drafts.
- Which LLM? Gemini through the generateContent API; default configured model gemini-2.5-flash.
- What is RAG? Retrieving relevant external evidence and passing it to a generative model before answering.
- Why not train an LLM? RAG updates the knowledge base without retraining and reduces computational requirements.
- What is TF-IDF? A numerical representation emphasizing terms frequent in a document but uncommon across documents.
- What is cosine similarity? A measure of vector alignment used to rank passages.
- What is novelty? The combination of evidence-backed support, abstention, grievance drafting, department routing and transparent evaluation for a university workflow. This is application-level differentiation, not a claim of novel research algorithms.
- How do you reduce hallucinations? Grounding prompt, relevance threshold, citation ID check and evidence display. These do not guarantee factual correctness.
- What are frontend and backend? Streamlit browser interface and Python server-side engine/API integration.
- How is performance evaluated? Labelled query top-1 category accuracy and out-of-scope abstention; a separate human-labelled answer evaluation would be needed for LLM factual accuracy.

## Suggested resume bullet (after completing live testing)
Built CampusResolve AI, a university student-support prototype using Python, Streamlit, Gemini LLM and RAG, with document ingestion, source-backed responses, out-of-scope abstention, grievance drafting and a reproducible 100-query retrieval benchmark.
