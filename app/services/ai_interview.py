import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))

def ask_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    raw = response.choices[0].message.content
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()


def ai_prompt(Topic:str):
    prompt = f"""
You are a senior technical interviewer with over 20 years of experience conducting software engineering interviews. 

Your task is to generate a professional interview title, a short welcome message, and the first interview question based on the interview topic provided by the user.

Interview Topic:
{Topic}

### Input validation
Before generating the interview, determine whether the provided interview topic is a valid technical interview topic.
- Determine whether the provided input is a valid technical interview topic suitable for a B.Tech or engineering interview.
- Accept only meaningful academic or technical subjects, technologies, frameworks, programming languages, engineering concepts, tools, or domain-specific topics.
- If the input is random text, meaningless words, everyday objects, greetings, or does not represent a valid interview topic, do not generate a title, welcome message, or interview question.
- Instead, return only this :
    {{
        "error": "Please enter a valid technical topic to begin the interview."
    }}

### Requirements for the title:
- Generate a concise and professional interview title.
- The title must clearly represent the interview topic.
- Keep the title between 3 and 6 words.
- Do not use quotation marks.
- Do not end the title with punctuation.
- Do not include unnecessary words such as "Interview on".

### Requirements for the welcome message:

- Keep the message under 35 words.
- Sound friendly, confident, and professional.
- Welcome the user to the AI interview.
- Inform the user that the interview starts with foundational questions and gradually increases in difficulty based on performance.
- Inform the user that the user can request easier or harder questions at any time during the interview.
- Inform the user that the interview can be ended at any time by clicking the **"End Interview"** button.
- End the message naturally before introducing the first question.
- Vary the wording, sentence structure, and greeting for each interview session so the welcome message feels natural and does not appear repetitive.
- Preserve the same meaning and instructions across all sessions while changing only the phrasing and style of the message.

### Requirements for the first interview question:
- Generate exactly one interview question.
- The question must be directly related to the provided interview topic.
- Begin with a strong foundational interview question.
- Do NOT ask simple definition-based questions such as "What is FastAPI?", "What is Redis?", or similar textbook questions.
- The first question should test one core concept of the topic rather than combining multiple concepts into a single question.
- Prefer questions that allow the candidate to explain one implementation detail in depth.
- Keep the question concise and professional.
- Do not include hints, explanations, or answers.

### Return ONLY valid JSON.

Do NOT return Markdown.
Do NOT return code blocks.
Do NOT return explanations.
Do NOT return additional text.
Do NOT return notes before or after the JSON.

The response must exactly follow this schema:

{{
  "title": "",
  "message": "",
  "question": ""
}}

"""
    raw =  ask_groq(prompt)
    return json.loads(raw)