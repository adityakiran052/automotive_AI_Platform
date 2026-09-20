from fastapi import APIRouter, UploadFile, File
import re
from backend.app.rag.pipeline import rag_engine

router = APIRouter(prefix="/autosar", tags=["AUTOSAR HLD"])

@router.post("/upload")
async def upload_hld(file: UploadFile = File(...)):
    contents = await file.read()
    count = rag_engine.ingest_pdf(contents, file.filename)
    return {"status": "success", "chunks_indexed": count, "filename": file.filename}

@router.post("/query")
def query_hld(query: str):
    contexts = rag_engine.retrieve(query, top_k=3)
    answer = rag_engine.generate_grounded_answer(query, contexts)
    return {
        "query": query, 
        "answer": answer, 
        "citations": [c["citation"] for c in contexts]
    }

@router.post("/extract-entities")
def extract_entities(query: str = "software components interfaces ports dependencies"):
    contexts = rag_engine.retrieve(query, top_k=5)
    aggregated_text = " ".join([c["text"] for c in contexts])
    
    # AUTOSAR architectural regex matchers
    swcs = sorted(list(set(re.findall(r'\b(?:SWC_[A-Za-z0-9_]+|[A-Z][a-zA-Z0-9_]+Component)\b', aggregated_text))))
    interfaces = sorted(list(set(re.findall(r'\b(?:I[A-Z][a-zA-Z0-9_]+|if_[A-Za-z0-9_]+)\b', aggregated_text))))
    ports = sorted(list(set(re.findall(r'\b(?:Pp_[A-Za-z0-9_]+|Rp_[A-Za-z0-9_]+|Cp_[A-Za-z0-9_]+)\b', aggregated_text))))
    
    # Inconsistency & dependency checks
    missing_elements = []
    if swcs and not interfaces:
        missing_elements.append("Software components detected without declared interface bindings.")
    if ports and not interfaces:
        missing_elements.append("Ports detected without associated interface mappings.")

    return {
        "software_components": swcs,
        "interfaces": interfaces,
        "ports": ports,
        "potential_inconsistencies": missing_elements,
        "evidence_sources": [c["citation"] for c in contexts]
    }