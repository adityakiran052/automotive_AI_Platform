import streamlit as st

def render_citations(citations: list):
    if citations:
        st.markdown("##### Source Citations")
        for idx, cite in enumerate(citations, 1):
            st.info(f"**[{idx}] Source Document:** `{cite}`")
    else:
        st.warning("No explicit source citations retrieved.")