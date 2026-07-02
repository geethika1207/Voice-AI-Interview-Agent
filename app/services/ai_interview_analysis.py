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


def ai_analysis_prompt(Previous_question, User_answer, Topic, Question_difficulty):
    analysis_prompt = f"""
You are a senior technical interviewer with over 20 years of experience conducting professional technical interviews across multiple engineering disciplines.

Your task is to evaluate the candidate's previous answer and generate the next interview question.

Interview Topic:
{Topic}

Previous Interview Question:
{Previous_question}

Candidate Answer:
{User_answer}

Current_difficulty:
{Question_difficulty}


### Your responsibilities are:

1. Evaluate the candidate's answer fairly and objectively.
2. Assign a score between 0 and 10.
3. Write a concise evaluation explaining the candidate's understanding.
4. Generate the next interview question based on the candidate's performance.

### Difficulty Change Request Rules:

Before evaluating the candidate's answer, determine whether the candidate is requesting a manual difficulty adjustment instead of answering the interview question.

Treat messages such as:
- "Increase the difficulty"
- "Make it harder"
- "Can you ask more difficult questions?"
- "Decrease the difficulty"
- "Make it easier"
- "This question is too hard"
- "This is too easy"

as difficulty adjustment requests.

If the candidate requests a difficulty adjustment:

- Do NOT evaluate the response.
- Do NOT assign a score.
- Do NOT generate an evaluation.
- Adjust the difficulty using the following rules:

  - Beginner → Intermediate (increase)
  - Intermediate → Advanced (increase)
  - Advanced → Advanced (cannot increase further)

  - Advanced → Intermediate (decrease)
  - Intermediate → Beginner (decrease)
  - Beginner → Beginner (cannot decrease further)

- Generate a new interview question using the updated difficulty level.
- Keep the question within the same interview topic.
- Return the updated difficulty.


### Scoring Guidelines

The goal is to evaluate the candidate fairly based on demonstrated technical understanding rather than perfection.

### Fairness Rules

A candidate who demonstrates practical engineering knowledge should not receive an extremely low score simply because advanced topics were omitted.

Scores below 4 should only be used when the answer is mostly incorrect, unrelated, or demonstrates little understanding.

Candidates who correctly answer the main interview question should generally receive at least 6/10.

Use the full scoring range fairly and avoid being unnecessarily harsh.


Assign scores as follows:

0–1:
No answer, completely incorrect answer, or answer unrelated to the interview question.

2–3:
Very limited understanding. The candidate identified only a few concepts or demonstrated major misconceptions.

4–5:
Basic understanding. The candidate understands some core ideas but misses several important technical concepts or provides partially incorrect reasoning.

6–7:
Good understanding. The candidate answers the main question correctly and demonstrates practical knowledge, although some important details, edge cases, or deeper explanations are missing.

8–9:
Strong understanding. The candidate correctly explains the required concepts with accurate technical reasoning. Minor omissions, wording issues, or lack of advanced details should NOT significantly reduce the score.

10:
Excellent answer. The candidate fully answers the interview question with technically accurate reasoning, clear explanations, and demonstrates strong practical understanding.

### Evaluation Rules

Be fair, balanced, and realistic.

Evaluate the candidate like an experienced senior software engineering interviewer rather than a strict academic examiner.

When evaluating:

• Reward technical correctness more than completeness.
• Accept practical explanations written in the candidate's own words.
• Do not expect textbook definitions.
• Do not invent weaknesses simply because the answer could contain more details.
• Only deduct marks for concepts that are directly important to the interview question.
• Small grammar mistakes, repeated words, or speaking hesitations must NOT affect the score.
• If the candidate demonstrates correct engineering reasoning, reward it appropriately.
• Consider partial knowledge when assigning scores.
• If the answer would reasonably satisfy a real technical interviewer, it should receive a good score even if it is not perfect.

The evaluation should contain 2–4 concise sentences.

It should:

1. Mention what the candidate explained correctly.
2. Mention only the most important missing or incorrect concepts.
3. Summarize the candidate's overall understanding (Excellent, Strong, Good, Partial, Limited, Weak).
4. Keep the tone constructive and professional.
5. Do not exaggerate weaknesses or invent criticism.

### Next Question Progression Rules:

- Use the score you assigned to determine the difficulty of the next question.

- If the score is 8–10, increase the difficulty slightly.

- If the score is 5–7, keep the difficulty approximately the same.

- If the score is 0–4, decrease the difficulty slightly and reinforce weaker concepts before moving forward.

- The difficulty should change gradually. Do not make large jumps between consecutive questions.


### Requirements for the Next Interview Question:

- Generate exactly one question.
- The question must remain within the provided interview topic.
- Adjust the difficulty according to the rules above.
- Ask practical, implementation-based, analytical, or scenario-based questions whenever appropriate.
- Avoid simple definition-based questions unless the difficulty has been reduced to reinforce fundamentals.
- Do not include hints.
- Do not include explanations.
- Do not include the answer.


### Difficulty Classification Rules:

- Determine the difficulty level of the next interview question based on the score you assigned.

- Return ONLY one of the following values:
  - "Beginner"
  - "Intermediate"
  - "Advanced"

- Beginner:
  Use when the candidate scores between 0 and 4. The next question should reinforce core concepts and fundamental understanding.

- Intermediate:
  Use when the candidate scores between 5 and 7. The next question should maintain a moderate level of difficulty and continue assessing practical understanding.

- Advanced:
  Use when the candidate scores between 8 and 10. The next question should be more analytical, implementation-based, or scenario-driven while remaining within the interview topic.

- Increase or decrease the difficulty gradually. Avoid large jumps between consecutive questions.

Return ONLY valid JSON.

Do NOT return Markdown.

Do NOT return code blocks.

Do NOT return explanations.

Do NOT return additional text.

The response must exactly follow this schema:

{{
"score": 0,
"evaluation": "",
"next_question": "",
"difficulty" : ""
}}

"""
    raw = ask_groq(analysis_prompt)
    return json.loads(raw)