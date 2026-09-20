import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

def render_disposition_form(query: str):
    st.markdown("---")
    st.subheader("Architect Sign-Off & Disposition")
    
    # Using st.form prevents the page from reloading until the submit button is clicked
    with st.form(key="disposition_form"):
        c1, c2 = st.columns(2)
        with c1:
            disp = st.selectbox("Decision", ["Accepted", "Modified", "Rejected"])
            reviewer = st.text_input("Architect ID", value="AUTOSAR-ARCH-01")
        with c2:
            comments = st.text_area("Review Comments / Architecture Notes", value="Verified against HLD document.")
        
        submitted = st.form_submit_button("Commit Decision to Audit DB")
        
        if submitted:
            payload = {
                "query": query,
                "disposition": disp,
                "comments": comments,
                "reviewed_by": reviewer
            }
            try:
                res = requests.post(f"{BACKEND_URL}/audit/record-review", json=payload)
                if res.status_code == 200:
                    st.success("Decision successfully logged to SQLite audit database!")
                else:
                    st.error(f"Failed to commit: {res.text}")
            except Exception as e:
                st.error(f"Connection error to backend: {e}")