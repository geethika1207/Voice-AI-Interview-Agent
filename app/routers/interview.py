from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..core.security import get_current_user
from ..schemas import interview
from ..db import models
from ..services.ai_interview import ai_prompt
from ..services.ai_interview_analysis import ai_analysis_prompt
from ..services.tts_service import text_to_speech
from ..services.stt_service import speech_to_text
import os
import uuid
import traceback

os.makedirs("temp", exist_ok=True)


router = APIRouter()

@router.post("/interview/start")
async def interview_topic(selected_topic : interview.InterviewTopic, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    try:
        result = ai_prompt(selected_topic.concept)
        error = result.get("error")
        
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        title = result.get("title")
        message = result.get("message")
        question = result.get("question")

        speech_text = question

        audio_filename = await text_to_speech(speech_text)

        print(audio_filename)

        new_interview = models.Interview(
                            user_id = current_user.id,
                            title = title,
                            topics = selected_topic.concept,
                            status = "active"
        )

        db.add(new_interview)
        db.commit()
        db.refresh(new_interview)

        first_question = models.Response(
                            interview_id = new_interview.id,
                            question = question
        )

        db.add(first_question)
        db.commit()
        db.refresh(first_question)

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error : {str(e)}")
    
    return {
        "id": new_interview.id,
        "title": title,
        "topics": selected_topic.concept,
        "topic_created_at": new_interview.created_at,
        "message": message,
        "question": question,
        "audio_url": f"/audio/{audio_filename}",
        "question_created_time": first_question.created_at
    }



@router.post("/interview/{id}/answer")
async def answer_analysis(
    id: int,
    audio: UploadFile = File(...),  
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    interview = db.query(models.Interview).filter(
        models.Interview.id == id,
        models.Interview.user_id == current_user.id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found."
        )

    recent_response = db.query(models.Response).filter(
        models.Response.interview_id == interview.id
    ).order_by(
        models.Response.created_at.desc()
    ).first()

    if not recent_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No interview question found."
        )

    current_difficulty = recent_response.difficulty or "Beginner"

    try:

        file_path = f"temp/{uuid.uuid4()}.mp3"

        with open(file_path, "wb") as f:
            f.write(await audio.read())

        transcript = await speech_to_text(file_path)
        print(transcript)

        result = ai_analysis_prompt(
            recent_response.question,
            transcript,
            interview.topics,
            current_difficulty
        )

        print(result.get("score"))
        print(result.get("evaluation"))

        # Update current question
        recent_response.answer = transcript
        recent_response.marks = result.get("score")
        recent_response.evaluation = result.get("evaluation")
        recent_response.difficulty = current_difficulty

        # Insert next question
        next_response = models.Response(
            interview_id=id,
            question=result["next_question"],
            difficulty=result["difficulty"]
        )

        db.add(next_response)
        db.commit()
        db.refresh(next_response)

        audio_filename = await text_to_speech(next_response.question)

        return {
            "interview_id" : id,
            "question": next_response.question,
            "difficulty": next_response.difficulty,
            "audio_url": f"/audio/{audio_filename}",
            "created_at": next_response.created_at
        }

    except Exception as e:
        db.rollback()
        traceback.print_exc()   
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"INTERNAL SERVER ERROR : {str(e)}"
        )