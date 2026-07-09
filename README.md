# CreditShield OS; Deterministic Multi-Agent Orchestrator for Credit Risk Compliance

A lightweight, deterministic multi-agent orchestration demo optimized for resource-constrained devices (Chromebook). The system simulates three cooperating nodes:

- Analyst Agent: retrieval from a local LlamaIndex + ChromaDB knowledge base (semantic retrieval, PII detection)
- Auditor Agent: structured financial metrics provider (Pydantic contracts simulating MCP/dbt)
- Judge Agent: deterministic validator enforcing safety and compliance, driving *Reflexion Retries* when policy violations occur

Streamlit
---
<img width="1920" height="943" alt="Screenshot 2026-07-09 19 42 41" src="https://github.com/user-attachments/assets/f0f22fea-0401-43a9-a694-03d81544b523" />
<img width="1509" height="937" alt="Screenshot 2026-07-09 19 42 46" src="https://github.com/user-attachments/assets/f1acca33-7a8e-4fbd-94cd-fd49818a95be" />


Architecture Flow
---
1. User issues a query via the Streamlit UI.
2. `Analyst` performs semantic retrieval from the local vector DB and extracts potential risk clauses and PII flags.
3. `Auditor` provides typed financial metrics (MRR, leverage, compliance score).
4. `Judge` validates the assembled `GraphState` using strong Pydantic contracts and either approves the deterministic report or triggers a Reflexion cycle (sanitization + retry).

Quickstart
---
```bash
git clone https://github.com/pierw95/Credit-Shield.git
cd Credit-Shield
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app_strategy.py
```

File map
---
- `schemas.py` — Pydantic contracts and `GraphState` definition
- `engine.py` — multi-agent orchestrator, nodes and the `run_credit_shield` state-machine
- `knowledge_base.py` — ChromaDB + LlamaIndex initialization (uses lightweight mock embeddings by default)
- `app_strategy.py` — Streamlit dashboard to run and visualize the multi-agent flow
- `requirements.txt`, `.gitignore` — environment and repo hygiene

Contributing / Notes
---
- Do not commit `chroma_db/` or `venv/` (already ignored).
- Replace the placeholder image streamlit before publishing for best presentation.
- The repository is intentionally lightweight: embeddings use a deterministic mock by default to avoid heavy model downloads on Chromebooks.

License
---
MIT
