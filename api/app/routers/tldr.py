from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from app.tldr.short_tldr import process_content


class Tldr(BaseModel):
    sentences: int = Field(..., gt=0,
                           description="Number of sentences to be returned")
    text: str = Field(
        ...,
        max_length=8000,
        description="Original text limited to (8000 characters)"
    )


router = APIRouter()


@router.post("/tldr")
def to_tldr(text: Tldr = Body(...)):
    """
    # Return a Tldr for any given text
    """
    out = process_content(text.text, text.sentences)
    return {
        "tldr": out
    }
