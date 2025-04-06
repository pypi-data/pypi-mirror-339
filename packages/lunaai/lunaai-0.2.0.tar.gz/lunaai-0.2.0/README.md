# LunaAI

**LunaAI** is a retrieval-based QnA and code generation chatbot built using SentenceTransformer embeddings and cosine similarity.  
It can answer natural language questions and retrieve highly relevant answers from a preloaded CSV dataset — no fine-tuning required.

---

## Features

- Embedding-based search using SentenceTransformers
- Cosine similarity + fuzzy matching fallback
- Loads embeddings and CSV from Google Drive
- Clean CLI interface with feedback saving
- Lightweight and fast — works offline after setup

---

## Installation

```bash
pip install lunaai
