from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..core.security import get_current_user
from ..db import models

router = APIRouter()

@router.delete("/delete/interview/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(id:int, db:Session=Depends(get_db), curren_user=Depends(get_current_user)):
    interview = db.query(models.Interview).filter(
                    models.Interview.user_id==curren_user.id,
                    models.Interview.id == id
    ).first()

    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="INTERVIEW NOT FOUND")
    
    db.delete(interview)
    db.commit()


@router.delete("/delete/history", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    interviews = (
        db.query(models.Interview)
        .filter(models.Interview.user_id == current_user.id)
        .all()
    )

    for interview in interviews:
        db.delete(interview)

    db.commit()