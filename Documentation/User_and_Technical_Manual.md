# AUTOSAR HLD AI ASSISTANT: TECHNICAL AND USER MANUAL

## 1. System Overview
The AUTOSAR HLD Document Analysis Assistant is a desktop/intranet engineering tool designed to streamline architecture reviews, enforce dependency tracking, and provide cited question answering from complex PDF specifications[cite: 4, 5].

---

## 2. Architecture & Data Flow

```text
[ Engineering PDF ] 
         │ (Upload)
         ▼
[ PyMuPDF Parser ] ──> [ Recursive Chunker ] ──> [ all-MiniLM-L6-v2 Embedder ]
                                                               │
                                                               ▼
                                                    [ ChromaDB Vector Store ]
                                                               │
[ User Query ] ─────────> [ Top-K Retrieval ] ─────────────────┘
                                   │
                                   ▼
             [ Evidence Prompt + Context Assembly ]
                                   │
                                   ▼
          [ Hugging Face LLM (Qwen2.5-Coder-1.5B) ]
                                   │
                                   ▼
               [ Grounded Answer + Citations ]
                                   │
                                   ▼
        [ Engineer Disposition Form (Accept/Modify/Reject) ]
                                   │
                                   ▼
               [ SQLite Audit Database (autosar_audit.db) ]