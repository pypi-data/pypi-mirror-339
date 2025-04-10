from pydantic import BaseModel


class SeedPrompt(BaseModel):
    question: str


class SeedPropmts(BaseModel):
    seed_prompts: list[SeedPrompt]


class Answer(BaseModel):
    raw_topic: str
    answer: str


def pydantic_encoder(obj):
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
