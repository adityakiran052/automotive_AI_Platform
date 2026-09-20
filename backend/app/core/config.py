import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"

CHROMA_PERSIST_DIR = str(DATA_DIR / "chromadb")
SQLITE_DB_PATH = str(DATA_DIR / "sqlite" / "autosar_audit.db")

# Models for local deployment
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
HF_LLM_MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
DEVICE = "cuda" if os.getenv("USE_CUDA", "0") == "1" else "cpu"

os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
os.makedirs(Path(SQLITE_DB_PATH).parent, exist_ok=True)


