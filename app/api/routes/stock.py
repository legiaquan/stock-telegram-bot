from fastapi import APIRouter
from pydantic import BaseModel
from app.services.stock_intent_resolver import StockIntentResolver

router = APIRouter()
resolver = StockIntentResolver()

class QueryRequest(BaseModel):
    text: str

@router.post("/ask", tags=["stock"])
async def ask_stock(req: QueryRequest):
    answer = resolver.resolve(req.text)
    return {"answer": answer}