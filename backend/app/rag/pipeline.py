import pymupdf as fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from backend.app.core.config import (
    CHROMA_PERSIST_DIR,
    EMBEDDING_MODEL_NAME,
    HF_LLM_MODEL_NAME,
    DEVICE
)

class RAGPipeline:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RAGPipeline, cls).__new__(cls)
            cls._instance.init_resources()
        return cls._instance

    def init_resources(self):
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.embed_model = SentenceTransformer(EMBEDDING_MODEL_NAME, device=DEVICE)
        
        self.tokenizer = AutoTokenizer.from_pretrained(HF_LLM_MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(HF_LLM_MODEL_NAME)
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=400,
            device=0 if DEVICE == "cuda" else -1
        )

    def get_collection(self):
        return self.chroma_client.get_or_create_collection(name="autosar_hld_store")

    def extract_and_chunk_pdf(self, file_bytes: bytes, filename: str, chunk_size: int = 400, overlap: int = 60):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        chunks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            words = text.split()
            
            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                chunk_text = " ".join(chunk_words).strip()
                if chunk_text:
                    chunks.append({
                        "text": chunk_text,
                        "metadata": {
                            "source": filename,
                            "page": page_num + 1,
                            "chunk_id": f"{filename}_p{page_num+1}_c{i}"
                        }
                    })
        return chunks

    def ingest_pdf(self, file_bytes: bytes, filename: str):
        collection = self.get_collection()
        chunks = self.extract_and_chunk_pdf(file_bytes, filename)
        
        if not chunks:
            return 0
            
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [c["metadata"]["chunk_id"] for c in chunks]
        
        embeddings = self.embed_model.encode(texts).tolist()
        collection.upsert(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
        return len(chunks)

    def retrieve(self, query: str, top_k: int = 3):
        collection = self.get_collection()
        query_embedding = self.embed_model.encode([query]).tolist()
        results = collection.query(query_embeddings=query_embedding, n_results=top_k)
        
        context_blocks = []
        if results and results["documents"]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                context_blocks.append({
                    "text": doc,
                    "citation": f"{meta['source']} (Page {meta['page']})"
                })
        return context_blocks

    def generate_grounded_answer(self, query: str, contexts: list):
        if not contexts:
            return "Information not found in approved documentation. Please upload the AUTOSAR HLD."
        
        evidence_text = "\n---\n".join([f"Source: {c['citation']}\nContent: {c['text']}" for c in contexts])
        prompt = (
            f"You are an AUTOSAR Architecture Expert. Answer the question STRICTLY using the verified sources below.\n"
            f"Always cite the exact Source for every assertion.\n\n"
            f"EVIDENCE:\n{evidence_text}\n\n"
            f"QUESTION: {query}\n\n"
            f"ENGINEERING ANSWER (WITH CITATIONS):"
        )
        self.generator = pipeline("text-generation",model=self.model,tokenizer=self.tokenizer,device=0 if DEVICE == "cuda" else -1)        
        output = self.generator(prompt,max_new_tokens=120, do_sample=False)
        return output[0]["generated_text"][len(prompt):].strip()

rag_engine = RAGPipeline()