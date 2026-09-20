# Automotive Engineering AI Platform: AUTOSAR HLD Assistant (Pilot)

An AI-assisted engineering workbench built for automotive software architects. This pilot implementation focuses on **Case Study 1: AUTOSAR HLD Document Analysis Assistant**, automating architecture extraction, semantic search with source citations, and human-in-the-loop review disposition tracking.

---

## Key Features

- **Document Ingestion & Local RAG**: Ingests AUTOSAR High-Level Design (HLD) specifications (PDF), extracts structural text, and generates semantic vector embeddings locally.
- **Architectural Entity Extraction**: Scans documentation to identify Software Components (`SWC_*`), communication interfaces (`I*`), and ports (`Pp_*`, `Rp_*`, `Cp_*`).
- **Context-Grounded Q&A**: Uses a local Hugging Face LLM strictly constrained to project evidence chunks, preventing architectural hallucinations.
- **Strict Evidence Citations**: Every generated finding maps directly to its source PDF and page number.
- **Human-in-the-Loop Sign-Off**: Includes an architect review panel allowing engineers to `Accept`, `Modify`, or `Reject` AI findings, logging decisions into a local SQLite audit database.

---

## System Architecture

```text
  [ Engineering User ]
           │
           ▼
  [ Streamlit Interface (Port 8501) ]
     ├── Document Ingestion & Chunking
     ├── Cited Architecture Q&A
     ├── Software Entity Inventory
     └── Architect Sign-Off & Audit History
           │
           ▼ (HTTP REST API)
  [ FastAPI Backend (Port 8000) ]
     ├── Local Embedding Pipeline (Sentence-Transformers: all-MiniLM-L6-v2)
     ├── Local Vector Database (ChromaDB Persistent Store)
     ├── Local LLM Generator (Hugging Face: Qwen2.5-Coder / Qwen2.5-0.5B)
     └── Compliance & Audit Engine (SQLite: autosar_audit.db)