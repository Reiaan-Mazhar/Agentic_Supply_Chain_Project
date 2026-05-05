from pydantic import BaseModel, Field
from typing import List

class GuardrailResult(BaseModel):
    is_safe: bool = Field(description="Whether the user input is safe and on-topic.")
    reason: str = Field(description="Reason for the safety classification.")

FORBIDDEN_TOPICS = [
    "ignore all previous instructions",
    "pretend",
    "dan",
    "delete the database",
    "drop table"
]

def is_input_safe_deterministic(user_input: str) -> bool:
    """Checks input against forbidden keywords."""
    lower_input = user_input.lower()
    for topic in FORBIDDEN_TOPICS:
        if topic in lower_input:
            return False
    return True
