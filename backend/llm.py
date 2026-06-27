import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

async def generate_cover_letter(resume_text: str, job_description: str, tone: str, notes: str = "") -> str:
    notes_section = f"\nADDITIONAL INSTRUCTIONS:\n{notes}" if notes.strip() else ""
    prompt = f"""
You are an expert career coach and professional writer.

Using the resume and job description below, write a tailored cover letter.

Tone: {tone}
- If formal: use professional language, no contractions, structured paragraphs
- If conversational: friendly and warm but still professional, natural phrasing
- If confident: assertive, achievement-focused, strong action verbs

Rules:
- 3 to 4 paragraphs
- Do not invent experience not present in the resume
- Highlight the most relevant skills and experiences for this specific role
- Do not include a date or address header, start directly with "Dear Hiring Manager," unless mentioned in additional instructions.
{notes_section}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Write the cover letter now:
"""
    response = client.models.generate_content(model = "gemini-2.5-flash-lite", contents = prompt)
    return response.text

async def generate_cold_email(resume_text: str, job_description: str, tone: str, notes: str = "") -> str:
    notes_section = f"\nADDITIONAL INSTRUCTIONS:\n{notes}" if notes.strip() else ""    
    prompt = f"""
You are an expert at writing cold outreach emails that get responses.

Using the resume and job description below, write a short cold email to a recruiter or hiring manager.

Tone: {tone}
- If formal: professional and respectful, clear subject line
- If conversational: approachable and human, not stiff
- If confident: direct, value-first, no fluff

Rules:
- Maximum 150 words in the email body
- Include a subject line at the very top prefixed with "Subject:"
- End with one clear call to action (e.g. ask if they're open to connecting, inquire about next steps, or request a 15-minute call)
- Do not invent experience not present in the resume
{notes_section}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Write the cold email now:
"""
    response = client.models.generate_content(model = "gemini-2.5-flash-lite", contents = prompt)
    return response.text
