import asyncio
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.parser import extract_text_from_pdf
from backend.llm import generate_cover_letter, generate_cold_email

app = FastAPI()

# Allow Streamlit (running on a different port) to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "backend is running"}


@app.post("/generate_cover_letter")
async def generate_cl(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    tone: str = Form(...),
    notes: str = Form(""),
):
    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)
    cover_letter = await generate_cover_letter(resume_text, job_description, tone, notes)
    return {"cover_letter": cover_letter}

@app.post("/generate_cold_email")
async def generate_ce(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    tone: str = Form(...),
    notes: str = Form(""),
):
    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)
    cold_email = await generate_cold_email(resume_text, job_description, tone, notes)
    return {"cold_email": cold_email}

