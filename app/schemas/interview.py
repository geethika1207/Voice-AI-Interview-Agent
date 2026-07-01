from pydantic import BaseModel

class InterviewTopic(BaseModel):
    concept : str

class InterviewAnswer(BaseModel):
    answer : str