# PROJECT SYNOPSIS

## 1. Project Title
Automotive Engineering AI Assistant: AUTOSAR HLD Document Analysis and Traceability Assistant (Pilot Implementation)[cite: 1, 2]

## 2. Domain & Technology Stack
- **Domain:** Automotive Software Engineering, AUTOSAR Classic/Adaptive Architecture[cite: 1, 4]
- **AI / NLP Stack:** Hugging Face Transformers (`Qwen/Qwen2.5-Coder-1.5B-Instruct`), Sentence-Transformers (`all-MiniLM-L6-v2`)[cite: 1, 5, 6]
- **Storage & Orchestration:** ChromaDB (Vector Store), SQLite (Audit & Review Log), Custom Grounded RAG Pipeline[cite: 1, 5, 6]
- **Application Services:** Python 3.10+, FastAPI (Backend API), Streamlit (Engineering Web UI)[cite: 1, 5, 24]

## 3. Problem Statement
Automotive software High-Level Design (HLD) specifications describe complex interactions between Software Components (SWCs), Client-Server/Sender-Receiver interfaces, ports, signals, and architectural dependencies[cite: 4]. These documents are frequently hundreds of pages long and stored as unstructured PDFs[cite: 4]. Manual review is time-consuming, prone to human oversight, and makes identifying missing dependencies or interface mismatches difficult[cite: 4]. Furthermore, external cloud LLMs risk exposing proprietary OEM/Tier-1 intellectual property[cite: 16].

## 4. Project Objectives
1. Implement a locally hosted, offline-capable Retrieval-Augmented Generation (RAG) system using open-source Hugging Face models to safeguard intellectual property[cite: 1, 3, 5].
2. Parse, chunk, and index multi-page AUTOSAR HLD documents into a persistent ChromaDB vector store[cite: 1, 5, 24].
3. Automate the extraction of core AUTOSAR entities (Software Components, Interfaces, and Ports) and flag dangling ports or orphaned components.
4. Provide semantic question-answering strictly grounded in approved documentation, returning exact page-level source citations to eliminate hallucinations[cite: 3, 5, 6].
5. Implement a human-in-the-loop review disposition workflow logging engineering sign-offs (Accepted, Modified, Rejected) to an auditable SQLite database[cite: 3, 5, 6].

## 5. System Architecture
The application adopts a decoupled client-server architecture[cite: 1, 24]:
1. **Frontend (Streamlit):** Web dashboard offering PDF document ingestion, natural language search, entity inventory visualization, and sign-off submission forms[cite: 1, 24].
2. **Backend (FastAPI):** Exposes RESTful endpoints for document upload, semantic search, architectural entity heuristic extraction, and audit log persistence[cite: 1, 24].
3. **AI Orchestration & RAG:** Uses PyMuPDF for layout and text extraction, generates dense vector representations via Sentence-Transformers, and utilizes a local Hugging Face LLM strictly bounded by prompt constraints[cite: 1, 24].
4. **Structured & Vector Storage:** ChromaDB persists vector embeddings locally; SQLite retains audit histories and engineering dispositions[cite: 1, 6, 24].

## 6. Expected Outcomes & Impact
- Substantial reduction in manual architecture review cycle times[cite: 6].
- 100% citation grounding for all architectural inquiries, preventing hallucinated dependencies[cite: 6].
- Formalized traceability and review history aligned with automotive functional safety and process governance[cite: 2, 7, 25].