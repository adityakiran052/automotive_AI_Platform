import streamlit as st
import requests
import json
from components.citations import render_citations
from components.disposition import render_disposition_form

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AUTOSAR HLD Document Assistant", layout="wide")

st.title("AUTOSAR HLD Document Analysis Assistant (Pilot)")
st.caption("AI-Assisted Architecture Extraction, Semantic Q&A, and Dependency Validation")

tab1, tab2, tab3 = st.tabs(["Document Ingestion & Search", "Architecture Inventory", "Audit & Review Log"])

# ================= TAB 1: INGESTION & SEARCH =================
with tab1:
    st.subheader("1. Ingest AUTOSAR HLD Specification")
    uploaded_file = st.file_uploader("Select HLD PDF", type=["pdf"])
    
    if uploaded_file and st.button("Ingest and Index Document"):
        with st.spinner("Extracting text and generating embeddings in local ChromaDB..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            res = requests.post(f"{BACKEND_URL}/autosar/upload", files=files)
            if res.status_code == 200:
                data = res.json()
                st.success(f"Indexed {data['chunks_indexed']} chunks from {data['filename']}.")
            else:
                st.error("Document ingestion failed.")

    st.markdown("---")
    st.subheader("2. Semantic Architecture Q&A")
    default_query = "Which software components communicate with the Brake Control component, and what interfaces are mentioned?"
    query = st.text_input("Enter architectural query:", value=default_query)
    
    # Initialize session state for query results if not present
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    if st.button("Run Grounded Query"):
        with st.spinner("Querying vector store and generating cited response..."):
            try:
                res = requests.post(f"{BACKEND_URL}/autosar/query", params={"query": query}).json()
                # Persist the output in session state so it doesn't fade on widget interaction
                st.session_state.last_result = {
                    "query": query,
                    "answer": res.get("answer", ""),
                    "citations": res.get("citations", [])
                }
            except Exception as e:
                st.error(f"Failed to query backend: {e}")

    # Render persisted result and disposition form outside the button conditional
    if st.session_state.last_result:
        st.markdown("### Grounded Answer")
        st.write(st.session_state.last_result["answer"])
        render_citations(st.session_state.last_result["citations"])
        render_disposition_form(st.session_state.last_result["query"])

# ================= TAB 2: ENTITY INVENTORY =================
with tab2:
    st.subheader("Extracted Architecture Entities & Inconsistencies")
    if st.button("Extract Inventory from Active Document"):
        with st.spinner("Analyzing architecture entities..."):
            data = requests.post(f"{BACKEND_URL}/autosar/extract-entities").json()
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("##### Software Components (SWCs)")
                for swc in data["software_components"]:
                    st.code(swc)
            with c2:
                st.markdown("##### Interfaces")
                for iface in data["interfaces"]:
                    st.code(iface)
            with c3:
                st.markdown("##### Ports")
                for port in data["ports"]:
                    st.code(port)
                    
            st.markdown("---")
            st.markdown("##### Consistency Verification")
            if data["potential_inconsistencies"]:
                for issue in data["potential_inconsistencies"]:
                    st.warning(issue)
            else:
                st.success("No apparent dangling ports or orphan SWCs identified.")
                
            st.download_button(
                "Export Architecture Inventory (JSON)",
                data=json.dumps(data, indent=2),
                file_name="autosar_extracted_inventory.json",
                mime="application/json"
            )

# ================= TAB 3: AUDIT HISTORY =================
with tab3:
    st.subheader("Traceability & Review History")
    res = requests.get(f"{BACKEND_URL}/audit/history").json()
    if res:
        st.table(res)
    else:
        st.info("No sign-offs recorded yet.")