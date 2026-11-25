# CampusResolve AI
Evidence-based university student support and grievance drafting with Gemini and retrieval-augmented generation (RAG).

## Windows quick start
1. Extract the ZIP completely. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ (enable Add Python to PATH).
2. Double-click `start_windows.bat`. First launch needs internet to install packages. Keep the terminal open.
3. The app opens in your browser, normally at http://localhost:8501. Select Offline demo to try it immediately.
4. For actual GenAI generation, obtain your own Gemini API key at https://aistudio.google.com/apikey, choose Live Gemini LLM in the sidebar and paste the key. Internet and supported model access/quota are required. The default model is gemini-2.5-flash; change it if your account no longer supports it. Never share your API key or commit it to GitHub.

## Manual startup (Windows PowerShell)
```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
On macOS/Linux use `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`, and `.venv/bin/python -m streamlit run app.py`.

## Structure
- app.py: Streamlit front end and server-side orchestration
- engine.py: document loading, chunking, TF-IDF retrieval, Gemini API client, grounding prompts and grievance generation
- data/: 10 synthetic policy documents, 100 labelled benchmark queries, 5 out-of-scope queries
- build_data.py: reproducible sample data creation
- evaluate.py: benchmark script
- tests/test_engine.py: automated regression tests
- requirements.txt: dependencies
- start_windows.bat: one-click setup and startup
- DEMO_AND_VIVA.md: presentation and viva notes

## Data and architecture
Student query -> TF-IDF vectorization -> cosine similarity -> threshold and top 3 passages -> evidence prompt -> Gemini -> source-ID validation -> answer and sources.
PDF/TXT upload -> extraction -> overlapping chunks -> retrieval index. Sample documents are explicitly synthetic and do not represent any specific university's official rules. Turn off sample data when using verified official policies. PDF extraction supports text PDFs, not scanned images. No LLM training is performed. TF-IDF is lexical retrieval, not neural embeddings.

## Validation
From the project root run `python -m pytest -q` and `python evaluate.py` (use the virtual environment Python if needed). The initial local run passed 5 tests; top-1 category accuracy 94/100, out-of-scope abstention 5/5. The benchmark is authored alongside the synthetic corpus, not independently collected. It measures retrieval rather than generated answer correctness. Some paraphrases and ambiguous questions fail. Do not claim production accuracy or 100% hallucination prevention.

## Limitations and privacy
The offline mode is extractive retrieval plus template drafting, not a generative LLM. Live Gemini calls require a valid user key. A failed API request is displayed and the app falls back to offline output. The citation check verifies reference IDs, not whether each assertion is supported. The threshold is heuristic, not calibrated confidence. No account system, database persistence or automatic grievance submission. No real student records are included. Avoid submitting confidential data; live mode sends prompts and relevant passages to Google. Verify official rules and deadlines before taking action. This is an educational prototype. The engine and benchmark were executed locally; Streamlit and actual Gemini API integration were not executed in the build environment.

## Local API key setup (Windows)
Run configure_key.bat once and paste a new Gemini API key at the hidden prompt. Then run start_windows.bat. The local .gemini_key file is ignored by Git; never share it or zip it. Alternatively paste the key into the app sidebar each session. Revoke any previously exposed key.
