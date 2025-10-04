# app.py
from fastapi import FastAPI, UploadFile, File, Form, Query, Body
from fastapi.responses import JSONResponse
from typing import Optional, Dict

from ocr_utils import read_image_bytes
from nlp_utils import extract_entities
from normalization import normalize_entities

app = FastAPI(title="AI-Powered Appointment Scheduler")

@app.post("/appointment")
async def get_appointment(
    text_form: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    text_query: Optional[str] = Query(None),
    payload: Optional[Dict] = Body(None),
):
    text_json = None
    if isinstance(payload, dict):
        text_json = payload.get("text")

    text = text_form or text_json or text_query

    if image:
        data = await image.read()
        text = read_image_bytes(data, lang="eng")

    if not text or not text.strip():
        return JSONResponse({"status": "needs_clarification", "message": "No valid input provided"})

    entities = extract_entities(text)
    normalized = normalize_entities(entities)
    return JSONResponse(normalized)
