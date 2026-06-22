import streamlit as st
import requests

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DraftRight",
    page_icon="✍️",
    layout="centered"
)

# ── Title ──────────────────────────────────────────────────────────────────────
st.title("✍️ DraftRight")
st.caption("Upload your resume and paste a job description and get a tailored cover letter and cold email instantly.")

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
    options=["formal", "conversational", "confident"],
    index=0
)

st.divider()


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
                    "http://localhost:8000/generate",
                    files={"resume": (resume_file.name, resume_file.getvalue(), "application/pdf")},
                    data={"job_description": job_description, "tone": tone}
                )
                response.raise_for_status()
                result = response.json()

                # ── Results ────────────────────────────────────────────────────
                st.success("Done! Your drafts are ready.")
                st.divider()

                st.subheader("Cover Letter")
                st.text_area("", value=result["cover_letter"], height=800, key="cover_letter_box")
                st.download_button(
                    label="Download Cover Letter",
                    data=result["cover_letter"],
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )

                st.divider()

                st.subheader("Cold Email")
                st.text_area("", value=result["cold_email"], height=400, key="cold_email_box")
                st.download_button(
                    label="Download Cold Email",
                    data=result["cold_email"],
                    file_name="cold_email.txt",
                    mime="text/plain"
                )

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Make sure FastAPI is running on port 8000.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")