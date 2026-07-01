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

def ai_result(topic, difficulty_history, evaluations):
    prompt = f"""
You are a senior technical interviewer with over 20 years of experience conducting professional technical interviews across multiple engineering disciplines.

Your task is to analyze the candidate's complete interview performance and generate a final interview report.

Interview Topic:
{topic}

Question Difficulty History:
{difficulty_history}

Question Evaluations:
{evaluations}

### Your Responsibilities

1. Analyze every evaluation from the interview session.
2. Consider how the interview difficulty progressed throughout the interview.
3. Identify the candidate's strongest technical abilities.
4. Identify the candidate's recurring knowledge gaps.
5. Generate constructive improvement suggestions.
6. Generate learning tags representing the concepts the candidate should study.
7. Determine the candidate's overall proficiency level.
8. Write a concise overall interview summary.

---

### Overall Summary Rules

The summary should:

Write a personalized summary directly to the user in **4–6 concise sentences**.

The summary should:
- Begin with the user's overall performance in the interview.
- Mention the strongest areas demonstrated throughout the session.
- Mention the weakest areas or concepts that need improvement.
- Comment on how the user handled the interview as the difficulty changed (for example: adapted well to harder questions, struggled as difficulty increased, remained consistent throughout, etc.).
- End with one encouraging sentence describing the next step for improvement.

The tone of the summary MUST adapt to the overall score:

If overall_score >= 8:
- Use a confident and positive tone.
- Emphasize strong technical understanding.
- Mention only a few advanced areas for improvement.
- Avoid making the performance sound weak.

If overall_score is between 5 and 7:
- Use a balanced tone.
- Mention both strengths and weaknesses equally.
- Clearly identify the concepts that require more practice.

If overall_score < 5:
- Use an encouraging and constructive tone.
- Focus on foundational concepts that need improvement.
- Avoid overly negative language.
- Emphasize that consistent practice can significantly improve performance.

Do NOT simply repeat the evaluations.
Instead, synthesize all evaluations into one coherent summary.

Do NOT use generic phrases like:
- "You should improve your technical knowledge."
- "Overall, you performed well."

Instead, mention the actual concepts discussed during the interview.

* Use second-person language ("you", "your") instead of referring to "the candidate".
* Make each suggestion actionable and encouraging.
* Focus on specific improvements rather than generic advice.

* Be between 3 and 5 concise sentences.
* Summarize the candidate's overall interview performance.
* Mention the candidate's strongest technical areas.
* Mention the candidate's major knowledge gaps.
* Mention whether the candidate handled increasing interview difficulty confidently or struggled as the interview progressed, when applicable.
* Be based only on the provided evaluations and interview difficulty history.
* Do not invent strengths or weaknesses that are not supported by the evaluations.

---

### Positive Highlights Rules

Return between 3 and 5 positive highlights.

Each highlight should:

Write suggestions directly to the user.

* Use second-person language ("you", "your") instead of referring to "the candidate".
* Make each suggestion actionable and encouraging.
* Focus on specific improvements rather than generic advice.

* Describe something the candidate consistently did well.
* Focus on technical understanding, reasoning ability, implementation skills, or communication.
* Be concise.
* Avoid repeating the overall summary.
* Only include strengths supported by the evaluations.

---

### Suggestions Rules

Return between 3 and 5 suggestions.

Each suggestion should:

Write suggestions directly to the user.

* Use second-person language ("you", "your") instead of referring to "the candidate".
* Make each suggestion actionable and encouraging.
* Focus on specific improvements rather than generic advice.

* Be a complete sentence.
* Describe a practical action the candidate should take to improve.
* Explain what the candidate should improve.
* Explain why improving it will strengthen their technical knowledge or interview performance.
* Focus on habits, learning strategies, explanation quality, reasoning, implementation skills, or interview techniques.
* Combine related weaknesses into a single actionable recommendation whenever appropriate.
* Be based only on the provided evaluations.
* Do not simply mention technical concepts or topics.
* Do not repeat or rephrase the learning tags.
* Avoid generic advice such as "Practice more" or "Keep learning."

---

### Learning Tags Rules

Return between 3 and 8 learning tags.

Learning tags should:

* Represent only technical concepts, technologies, frameworks, APIs, protocols, algorithms, or software engineering topics the candidate should study.
* Be extracted directly from concepts that were identified in the evaluations as incorrect, misunderstood, incomplete, uncertain, or missing.
* Consist of only 1-4 words.
* Contain only the concept name without explanations or advice.
* Do **not** include concepts the candidate already demonstrated strong understanding of.
* Do **not** infer or invent additional topics that are not supported by the evaluations.
* Do **not** convert learning tags into recommendations or complete sentences.
* Do **not** repeat the same concept using different wording.
* Return only technical concepts that the candidate should learn next.

---

### Overall Difficulty Rules

Determine the candidate's overall proficiency using both the evaluation history and the progression of interview difficulty.

Return ONLY one of:

* "Beginner"
* "Intermediate"
* "Advanced"

Use these guidelines:

* Beginner:
  The candidate struggled with foundational concepts or was unable to handle increasing difficulty.

* Intermediate:
  The candidate demonstrated a solid understanding of fundamental concepts and handled moderate difficulty but showed noticeable gaps in advanced topics.

* Advanced:
  The candidate consistently demonstrated strong technical understanding and successfully handled advanced interview questions.

Base the decision on the entire interview rather than a single question.

---

Return ONLY valid JSON.

Do NOT return Markdown.

Do NOT return explanations.

Do NOT return code blocks.

Do NOT return additional text.

The response must exactly follow this schema:

{{
"overall_summary": "",
"positive_highlights": [
""
],
"suggestions": [
""
],
"learning_tags": [
""
],
"overall_difficulty": ""
}}

"""
    raw = ask_groq(prompt)
    return json.loads(raw)
