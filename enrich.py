import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

router = APIRouter()

PROMPT_PATH = Path(__file__).parent / "prompts" / "enrich-v1.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)


class EnrichIn(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=2000)


@router.post("/enrich")
def enrich_record(payload: EnrichIn):
    if os.getenv("LLM_STUB") == "1":
        return {
            "category": "poetry",
            "summary": "a call to action",
            "confidence": 1,
            "quality_flags": [],
        }

    book = json.dumps({"title": payload.title, "description": payload.description})

    res = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": book},
        ],
        temperature=0,
    )
    return {"raw": res.choices[0].message.content}