from pydantic import BaseModel


class GetAiData(BaseModel):
    ai_id: str
    ai_name: str
    ai_description: str
    ai_category: str
    owner: str
    company: str


class CreateAiData(BaseModel):
    ai_name: str
    ai_description: str
    ai_category: str
    owner: str
    company: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
