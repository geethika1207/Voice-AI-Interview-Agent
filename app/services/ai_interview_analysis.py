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


### Scoring Guidelines:

    **IMPORTANT** : When assigning scores, prioritize correctness over completeness. A concise but technically correct answer should receive a higher score than a long answer containing inaccuracies.

* 0-2:
  The answer is incorrect, irrelevant, or demonstrates no understanding of the question.

* 3-4:
  The answer shows minimal understanding but contains significant misunderstandings or missing concepts.

* 5-6:
  The answer demonstrates partial understanding but misses important technical details.

* 7-8:
  The answer is mostly correct with only minor inaccuracies or missing explanations.

* 9-10:
   The answer correctly addresses the interview question, demonstrates strong technical understanding, and contains no significant inaccuracies. Minor omitted details that are not essential should not prevent awarding a high score.

### Evaluation Rules:

* Evaluate the candidate's understanding based on the meaning of the answer rather than the exact wording.
* Accept answers written in the candidate's own words if the technical meaning is correct.
* Do not require textbook definitions or exact phrasing.
* Reward practical understanding and correct technical reasoning over completeness.
* Do not reduce the score simply because the candidate omitted additional valid points that were not necessary to answer the question.
* Penalize only factual inaccuracies, incorrect reasoning, or important concepts directly required by the interview question.
* Do not invent mistakes or missing concepts that are not supported by the candidate's answer.
* If the answer is technically correct and sufficiently addresses the interview question, award a high score even if it is not exhaustive.

The evaluation must be between 2 and 4 concise sentences and should:

1. Clearly describe what the candidate explained correctly and the technical concepts they demonstrated.
2. Mention missing, incomplete, or incorrect concepts only if they meaningfully affected the quality or score of the answer.
3. Briefly summarize the candidate's overall understanding of the topic (for example: excellent, strong, good, partial, limited, or weak understanding).
4. Base every statement only on the interview question and the candidate's answer. Do not make assumptions or invent missing concepts that are not evident from the answer.
5. If the answer fully addresses the interview question and deserves a high score (9–10), do not invent weaknesses simply to provide criticism. Instead, acknowledge that the response is complete while mentioning any advanced topics only as optional improvements.

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