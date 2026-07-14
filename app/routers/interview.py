from fastapi import APIRouter, Depends, status, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from ..db.database import SessionLocal, get_db
from ..core.security import get_current_user
from ..schemas import interview
from ..db import models
from ..services.ai_interview import ai_prompt
from ..services.ai_interview_analysis import ai_analysis_prompt
from ..services.tts_service import text_to_speech
from ..services.stt_service import SpeechToText
from ..services.vad_service import VoiceActivityDetector
from ..services.buffer_service import AudioBuffer
import os
import asyncio

os.makedirs("temp", exist_ok=True)

stt = SpeechToText()
buffer = AudioBuffer()


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
        print("Interview created:", new_interview.id)

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


@router.websocket("/ws/interview/{id}")
async def interview_socket(
    websocket: WebSocket,
    id: int,
    db: Session = Depends(get_db)
):

    await websocket.accept()

    print("Hello")
    
    interview = (
        db.query(models.Interview)
        .filter(models.Interview.id == id)
        .first()
    )

    if not interview:
        await websocket.send_json(
            {"error": "Interview not found"}
        )
        await websocket.close()
        return                                        # return says "stop executing this endpoint."


    recent_response = db.query(models.Response).filter(
         models.Response.interview_id == interview.id
     ).order_by(
         models.Response.created_at.desc()
     ).first()


    if not recent_response:
        await websocket.send_json(
            {"error": "Interview not found"}
        )
        await websocket.close()
        return  
      
    current_difficulty = recent_response.difficulty or "Beginner"


    # ---------------------------------
    # Services

    stt = SpeechToText()

    vad = VoiceActivityDetector()


    await stt.connect()


    # ---------------------------------
    # Queues

    deepgram_queue = asyncio.Queue()

    vad_queue = asyncio.Queue()

    buffer_queue = asyncio.Queue()

    vad_finished = asyncio.Event()


    # =================================
    # Deepgram Worker

    async def deepgram_worker():

        while True:

            chunk = await deepgram_queue.get()

            await stt.send_chunk(chunk)

            deepgram_queue.task_done()



    # =================================
    # VAD Worker

    async def vad_worker():

        while True:

            chunk = await vad_queue.get()

            if vad.is_speech_finished(chunk):           # statement under if executes only if the speech completed by the user

                vad_finished.set()                      # VAD signal ON 

            vad_queue.task_done()



    # =================================
    # Buffer Worker

    async def buffer_worker():

        while True:

            chunk = await buffer_queue.get()

            buffer.add_chunk(chunk)

            buffer_queue.task_done()



    # ---------------------------------
    # Start Workers

    deepgram_task = asyncio.create_task(
        deepgram_worker()
    )

    vad_task = asyncio.create_task(
        vad_worker()
    )

    buffer_task = asyncio.create_task(
        buffer_worker()
    )


    idle_count = 0 
    
    try:

        while True:

            try:

                chunk = await asyncio.wait_for(

                    websocket.receive_bytes(),

                    timeout=5

                )
                
                await deepgram_queue.put(chunk)

                await vad_queue.put(chunk)

                await buffer_queue.put(chunk)

            except asyncio.TimeoutError:

                if not vad_finished.is_set():

                    idle_count += 1

                    if idle_count == 1:

                        await websocket.send_text(
                            "Are you still there?"
                        )

                        continue

                    else:

                        await websocket.send_text(
                            "Moving to next question..."
                        )

                        vad_finished.set()

            if not vad_finished.is_set():
                continue
            
            # Reset for next question

            vad_finished.clear()

            idle_count = 0

            transcript = await stt.get_transcript()

            await stt.reset_transcript()

            vad.reset()

            try:

                result = await asyncio.wait_for(
                    ai_analysis_prompt(
                        recent_response.question,
                        transcript,
                        interview.topics,
                        current_difficulty
                    ),
                    timeout=20
                )
                

            except asyncio.TimeoutError:

                await websocket.send_text(
                    "AI server is busy. Please wait..."
                )

                return

            # ==============================
            # Save

            # Update current question
            recent_response.answer = transcript
            recent_response.marks = result.get("score")
            recent_response.evaluation = result.get("evaluation")
            recent_response.difficulty = current_difficulty

            #Insert next question

            next_response = models.Response(
                interview_id=id,
                question=result["next_question"],
                difficulty=result["difficulty"]      
            )

            db.add(next_response)
            db.commit()
            db.refresh(next_response)


            # ==============================
            # TTS

            filename = await text_to_speech(
                result["next_question"]
            )

            await websocket.send_json({

                "question": result["next_question"],

                "audio_url": f"/audio/{filename}"

            })


    except WebSocketDisconnect:

        print("Client disconnected")

    finally:

        deepgram_task.cancel()
        vad_task.cancel()
        buffer_task.cancel()

        await stt.close()

        await websocket.close()
        

# ENDPOINT FOR AUDIO FILE UPLOAD FOR HTTP REQUEST WE DONT HAVE TO WRITE CONNECT AND CLOSE...

# @router.post("/interview/{id}/answer")
# async def answer_analysis(
#     id: int,
#     audio: UploadFile = File(...),  
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
    
#     interview = db.query(models.Interview).filter(
#         models.Interview.id == id,
#         models.Interview.user_id == current_user.id
#     ).first()

#     if not interview:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Interview not found."
#         )

#     recent_response = db.query(models.Response).filter(
#         models.Response.interview_id == interview.id
#     ).order_by(
#         models.Response.created_at.desc()
#     ).first()

#     if not recent_response:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No interview question found."
#         )

#     current_difficulty = recent_response.difficulty or "Beginner"

#     try:

#         file_path = f"temp/{uuid.uuid4()}.mp3"

#         with open(file_path, "wb") as f:
#             f.write(await audio.read())

#         transcript = await speech_to_text(file_path)
#         print(transcript)

#         result = ai_analysis_prompt(
#             recent_response.question,
#             transcript,
#             interview.topics,
#             current_difficulty
#         )

#         print(result.get("score"))
#         print(result.get("evaluation"))

#         # Update current question
#         recent_response.answer = transcript
#         recent_response.marks = result.get("score")
#         recent_response.evaluation = result.get("evaluation")
#         recent_response.difficulty = current_difficulty

#         # Insert next question
#         next_response = models.Response(
#             interview_id=id,
#             question=result["next_question"],
#             difficulty=result["difficulty"]
#         )

#         db.add(next_response)
#         db.commit()
#         db.refresh(next_response)

#         audio_filename = await text_to_speech(next_response.question)

#         return {
#             "interview_id" : id,
#             "question": next_response.question,
#             "difficulty": next_response.difficulty,
#             "audio_url": f"/audio/{audio_filename}",
#             "created_at": next_response.created_at
#         }

#     except Exception as e:
#         db.rollback()
#         traceback.print_exc()   
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"INTERNAL SERVER ERROR : {str(e)}"
#         )