import asyncio
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.parser import extract_text_from_pdf
from backend.llm import generate_cover_letter, generate_cold_email

app = FastAPI()

# Allow Streamlit (running on a different port) to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "backend is running"}


@app.post("/generate")
async def generate(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    tone: str = Form(...),
):
    file_bytes = await resume.read()

    resume_text = extract_text_from_pdf(file_bytes)

    # Step 3: generate both outputs from Gemini
    cover_letter = await generate_cover_letter(resume_text, job_description, tone)
    await asyncio.sleep(2)
    cold_email = await generate_cold_email(resume_text, job_description, tone)

    return {
        "cover_letter": cover_letter,
        "cold_email": cold_email,
    }