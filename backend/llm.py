import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_cover_letter(resume_text: str, job_description: str, tone: str) -> str:
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
- Do not include a date or address header, start directly with "Dear Hiring Manager,"

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Write the cover letter now:
"""
    response = model.generate_content(prompt)
    return response.text

def generate_cold_email(resume_text: str, job_description: str, tone: str) -> str:
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
- One clear call to action at the end (e.g. ask for a 15 minute call)
- Do not invent experience not present in the resume

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Write the cold email now:
"""
    response = model.generate_content(prompt)
    return response.text
