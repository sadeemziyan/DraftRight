import streamlit as st
import streamlit.components.v1 as components
import requests

BACKEND_URL = "https://localhost:8000"


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DraftRight",
    page_icon="✍️",
    layout="centered"
)

if "results" not in st.session_state:
    st.session_state.results = None

# ── Title ──────────────────────────────────────────────────────────────────────
st.title("✍️ DraftRight")
st.caption("Upload your resume and paste a job description to get a tailored cover letter and cold email instantly.")

st.divider()

# ── Inputs ─────────────────────────────────────────────────────────────────────
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

# Copy button
def copy_button(text, key):
    components.html(f"""
        <button onclick="navigator.clipboard.writeText(`{text}`)" 
            style="background-color:#ff4b4b; color:white; border:none; 
            padding:8px 16px; border-radius:4px; cursor:pointer;">
            Copy to Clipboard
        </button>
    """, height=45)

# ── Generate button ─────────────────────────────────────────────────────────────
if st.button("Generate", type="primary", use_container_width=True):

    # Validate inputs before sending
    if not resume_file:
        st.error("Please upload your resume PDF.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Generating your cover letter and cold email..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    files={"resume": (resume_file.name, resume_file.getvalue(), "application/pdf")},
                    data={"job_description": job_description, "tone": tone}
                )
                response.raise_for_status()
                st.session_state.results = response.json()

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Make sure FastAPI is running on port 8000.")
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    st.error("The AI service is temporarily unavailable due to rate limits. Please try again in a few minutes.")
                else:
                    st.error(f"Something went wrong: {e}")

if st.session_state.results:
    st.success("Done! Your drafts are ready.")
    st.divider()

    st.subheader("Cover Letter")
    st.text_area("", value=st.session_state.results["cover_letter"], height=800, key="cover_letter_box")
    copy_button(st.session_state.results["cover_letter"], key="cover_letter_copy")
    st.download_button(
        label="Download Cover Letter",
        data=st.session_state.results["cover_letter"],
        file_name="cover_letter.txt",
        mime="text/plain"
    )

    st.divider()

    st.subheader("Cold Email")
    st.text_area("", value=st.session_state.results["cold_email"], height=400, key="cold_email_box")
    copy_button(st.session_state.results["cold_email"], key="cold_email_copy")
    st.download_button(
        label="Download Cold Email",
        data=st.session_state.results["cold_email"],
        file_name="cold_email.txt",
        mime="text/plain"
    )