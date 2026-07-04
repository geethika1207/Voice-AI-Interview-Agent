from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..core.security import get_current_user
from ..db import models

router = APIRouter()

@router.get("/interview/history")
def get_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    interviews = db.query(models.Interview)\
        .filter(models.Interview.user_id == current_user.id)\
        .all()               # outerloop , inner loop

    if not interviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No interviews found"
        )

    result = []

    for i in interviews:

        analysis = []

        for a in i.overall_analysis:     #i.overall_analysis correctly nested per interview to make sure the analysis are related to that interview
            analysis.append({
                "marks": a.marks,
                "difficulty": a.overall_difficulty
            })

        result.append({
            "interview_id": i.id,
            "title": i.title,
            "topic": i.topics,
            "created_at": i.created_at,
            "analysis": analysis
        })

    return result         


@router.get("/history/interview/{id}")
def get_interview_history(id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    interview = db.query(models.Interview).filter(
        models.Interview.user_id==current_user.id,
        models.Interview.id==id
    ).first() #inner loop to convert orm obj to json lists

    if not interview:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="INVALID CREDENTIALS")
    
    responses = interview.user_response
    analysis = interview.overall_analysis
    print(analysis)
    
    blueprint = [{
                    "interview_id" : id,
                    "summary" : a.summary,
                    "positive_aspects" : a.positive_aspects,
                    "suggestions" : a.suggestions,
                    "learning_tags" : a.learning_tags,
                    "overall_difficulty" : a.overall_difficulty,
                    "marks" : a.marks,
                    "created_at" : a.created_at
                } 
                for a in analysis
    ]

    response = [{
                    "question" : r.question,
                    "difficulty" : r.difficulty,
                    "answer" : r.answer,
                    "evaluation" : r.evaluation,
                    "marks" : r.marks,
                    "created_at" : r.created_at
    }
    for r in responses
    ]

    return{
            "analysis" : blueprint,
            "responses" : response
    }


