from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import SessionLocal
from sqlalchemy.orm import joinedload

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.QuestionInfoOut])
def read_questions(db: Session = Depends(get_db)):
    questions = db.query(models.QuestionInfo).all()
    return questions


@router.get("/{question_id}", response_model=schemas.QuestionInfoDetail)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = (
        db.query(models.QuestionInfo)
        .filter(models.QuestionInfo.id == question_id)
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="질문지가 존재하지 않습니다."
        )
    return question


@router.post(
    "/", response_model=schemas.QuestionInfoDetail, status_code=status.HTTP_201_CREATED
)
def create_question(
    question: schemas.QuestionInfoCreate, db: Session = Depends(get_db)
):
    db_question = models.QuestionInfo(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.patch("/{question_id}", response_model=schemas.QuestionInfoDetail)
def update_question(
    question_id: int,
    update_data: schemas.QuestionInfoUpdate,
    db: Session = Depends(get_db),
):
    question = (
        db.query(models.QuestionInfo)
        .filter(models.QuestionInfo.id == question_id)
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="질문지가 존재하지 않습니다."
        )

    data = update_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="업데이트할 필드를 최소 한 개 이상 제공해야 합니다.",
        )

    for key, value in data.items():
        setattr(question, key, value)
    db.commit()
    db.refresh(question)
    return question


@router.delete("/{question_id}", status_code=status.HTTP_200_OK)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = (
        db.query(models.QuestionInfo)
        .filter(models.QuestionInfo.id == question_id)
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="질문지가 존재하지 않습니다."
        )
    db.delete(question)
    db.commit()
    return {"message": "질문지가 삭제되었습니다."}
