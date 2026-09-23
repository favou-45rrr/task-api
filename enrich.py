from fastapi import APIRouter
from pydantic import BaseModel,Field
from dotenv import load_dotenv
import os

load_dotenv()


router = APIRouter()

class EnrichIn(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=500)
@router.post("/enrich")
def enrich_record(payload:EnrichIn):
    llm_stub = os.getenv("LLM_STUB")
    if llm_stub == "1":
        return {"category":"poetry",
        "summary":"a call to action",
        "confidence":1,
        "quality_flags":[]}
    return{"received": payload.title}

