# Deliberate Tradeoffs

### 1. Real-time Carbon Emission Factor Matching

- **What we omitted:** We do not hit live DEFRA or EPA APIs to calculate the exact $CO_2e$ metric tons.
- **Why:** The assignment emphasized _ingestion, normalization, and review UX_. Fetching emission factors introduces network latency and third-party dependencies. We focused on solidifying the data shape (`amount`, `unit`) so the math engine can be cleanly appended later.

### 2. Async Background Task Processing (Celery/Redis)

- **What we omitted:** Multi-megabyte file uploads are parsed synchronously in the HTTP request cycle.
- **Why:** For a 4-day prototype with small sample payloads, introducing Redis/Celery increases deployment complexity on platforms like Railway/Render without adding immediate validation value for the analysts.

### 3. Complex PDF Parsing (OCR)

- **What we omitted:** We chose CSV portal exports over processing raw utility PDF bills via AI/OCR.
- **Why:** PDF parsing is notoriously brittle and prone to hallucinated metrics. Building a deterministic CSV ingestion channel demonstrates data safety better than a shaky OCR wrapper.
