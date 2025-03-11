import os
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
from pydantic import BaseModel
import json
from prompt_templates import ADVICE_PROMPT

app = FastAPI(title="Career Counseling Assistant")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration for open-webui API
WEBUI_ENABLED = True  # Set to use open-webui API
WEBUI_BASE_URL = "https://chat.ivislabs.in/api"
API_KEY = "sk-0f5afb1ff7714ddcb15e2e35c98e652f"  # Replace with your actual API key if needed

class AdviceRequest(BaseModel):
    experience: str
    career_goal: str
    advice_type: str  # "resume" or "interview"
    tone: Optional[str] = "professional"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_advice(
    experience: str = Form(...),
    career_goal: str = Form(...),
    advice_type: str = Form("resume"),
    tone: str = Form("professional")
):
    try:
        prompt = ADVICE_PROMPT.format(
            experience=experience,
            career_goal=career_goal,
            advice_type=advice_type,
            tone=tone
        )
        
        if WEBUI_ENABLED:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{WEBUI_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gemma2:2b",  # Default model
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=60.0
                )
                
                if response.status_code != 200:
                    raise HTTPException(status_code=500, detail="Failed to generate career advice")
                
                result = response.json()
                generated_advice = result.get("choices", [{}])[0].get("message", {}).get("content", "No advice generated.")
                
                return {"generated_advice": generated_advice}
        
        raise HTTPException(status_code=500, detail="AI service unavailable")
    except Exception as e:
        print(f"Error generating career advice: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating career advice: {str(e)}")
