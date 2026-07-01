
from fastapi import HTTPException, status, APIRouter, Depends
from ..db import models
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..core.security import get_current_user
from ..services.ai_interview_result import ai_result

router = APIRouter()

def get_interview_information(id:int, db:Session):
    interview_details = (
        db.query(models.Response)
        .filter(
            models.Response.interview_id == id,
            models.Response.answer.isnot(None)
        )
        .all())
    
    if not interview_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO INTERVIEW FOUND")
    
    interview_marks = [response.marks for response in interview_details]
    interview_evaluation = [response.evaluation for response in interview_details]
    interview_difficulty = [response.difficulty for response in interview_details]

    return interview_marks, interview_evaluation, interview_difficulty


def calculate_marks(marks):
    total_marks = round(sum(marks)/len(marks))
    return total_marks


@router.post("/interview/end/interview/{id}")
def interview_analysis(id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    interview = db.query(models.Interview).filter(models.Interview.id==id, models.Interview.user_id==current_user.id).first()

    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="INTERVIEW NOT FOUND")
    
    session_topic = interview.topics

    interview_marks, interview_evaluation, interview_difficulty = get_interview_information(id, db)

    try:
        result = ai_result(session_topic, interview_difficulty, interview_evaluation)

        total_marks = calculate_marks(interview_marks)

        overall_analysis = models.interview_analysis(
                                interview_id = id,
                                summary = result.get("overall_summary"),
                                positive_aspects = result.get("positive_highlights"),
                                suggestions = result.get("suggestions"),
                                learning_tags = result.get("learning_tags"),
                                overall_difficulty = result.get("overall_difficulty"),
                                marks = total_marks
        )

        db.add(overall_analysis)
        db.commit()
        db.refresh(overall_analysis)

        return {
            "interview_id": id,
            "summary": result.get("overall_summary"),
            "positive_aspects": result.get("positive_highlights"),
            "suggestions": result.get("suggestions"),
            "learning_tags": result.get("learning_tags"),
            "overall_difficulty": result.get("overall_difficulty"),
            "marks" : total_marks
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )