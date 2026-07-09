import os
import streamlit as st
import streamlit.components.v1 as components
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DraftRight",
    page_icon="✍️",
    layout="wide"
)

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = None
if "cold_email" not in st.session_state:
    st.session_state.cold_email = None

# ── Title ──────────────────────────────────────────────────────────────────────
st.title("✍️ DraftRight")
st.caption("Upload your resume and paste a job description to get a tailored cover letter and cold email instantly.")

st.divider()

# ── Shared Inputs ─────────────────────────────────────────────────────────────────────
resume_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

job_description = st.text_area(
    "Paste the job description here",
    height=400,
    placeholder="Copy and paste the full job posting here..."
)

tone = st.selectbox(
    "Select tone",
    options=["Formal", "Conversational", "Confident"],
    index=0
)

st.divider()

# ── Copy button ────────────────────────────────────────────────────────────────
def copy_button(text, key):
    components.html(f"""
        <button id="{key}" onclick="
            navigator.clipboard.writeText(`{text}`);
            this.innerText = 'Copied!';
            setTimeout(() => this.innerText = 'Copy to Clipboard', 2000);
        " 
            style="background-color:#ff4b4b; color:white; border:none; 
            padding:8px 16px; border-radius:4px; cursor:pointer;">
            Copy to Clipboard
        </button>
    """, height=45)

# ── Validate shared inputs ─────────────────────────────────────────────────────
def validate_inputs():
    if not resume_file:
        st.error("Please upload your resume PDF.")
        return False
    if not job_description.strip():
        st.error("Please paste a job description.")
        return False
    return True

# ── Two columns ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)


# ── Cover Letter Column ────────────────────────────────────────────────────────
with col1:
    st.subheader("Cover Letter")
    cl_notes = st.text_area(
        "Additional notes (optional)",
        height=150,
        placeholder="e.g. mention I live on campus, use a 3 paragraph format...",
        key="cl_notes"
    )
    if st.button("Generate Cover Letter", type="primary", use_container_width=True):
        st.session_state.cold_email = None
        if validate_inputs():
            with st.spinner("Generating your cover letter..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate_cover_letter",
                        files={"resume": (resume_file.name, resume_file.getvalue(), "application/pdf")},
                        data={"job_description": job_description, "tone": tone, "notes": cl_notes}
                    )
                    response.raise_for_status()
                    st.session_state.cover_letter = response.json()["cover_letter"]
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        st.error("Rate limit reached. Please try again later.")
                    elif e.response.status_code == 503:
                        st.error("Gemini is currently busy. Please try again in a moment.")
                    else:
                        st.error(f"Something went wrong: {e}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend. Make sure FastAPI is running on port 8000.")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    if st.session_state.cover_letter:
        st.text_area("", value=st.session_state.cover_letter, height=500, key="cover_letter_box")
        copy_button(st.session_state.cover_letter, key="cover_letter_copy")
        st.download_button(
            label="Download Cover Letter",
            data=st.session_state.cover_letter,
            file_name="cover_letter.txt",
            mime="text/plain"
        )

# ── Cold Email Column ──────────────────────────────────────────────────────────
with col2:
    st.subheader("Cold Email")
    ce_notes = st.text_area(
        "Additional notes (optional)",
        height=150,
        placeholder="e.g. mention I'm available for a call this week...",
        key="ce_notes"
    )
    if st.button("Generate Cold Email", type="primary", use_container_width=True):
        st.session_state.cold_email = None
        if validate_inputs():
            with st.spinner("Generating your cold email..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate_cold_email",
                        files={"resume": (resume_file.name, resume_file.getvalue(), "application/pdf")},
                        data={"job_description": job_description, "tone": tone, "notes": ce_notes}
                    )
                    response.raise_for_status()
                    st.session_state.cold_email = response.json()["cold_email"]
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        st.error("Rate limit reached. Please try again later.")
                    elif e.response.status_code == 503:
                        st.error("Gemini is currently busy. Please try again in a moment.")
                    else:
                        st.error(f"Something went wrong: {e}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend. Make sure FastAPI is running on port 8000.")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    if st.session_state.cold_email:
        st.text_area("", value=st.session_state.cold_email, height=500, key="cold_email_box")
        copy_button(st.session_state.cold_email, key="cold_email_copy")
        st.download_button(
            label="Download Cold Email",
            data=st.session_state.cold_email,
            file_name="cold_email.txt",
            mime="text/plain"
        )