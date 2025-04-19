from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{short_id}", response_model=schemas.ShortAnswerQuestionOut)
def get_short(short_id: int, db: Session = Depends(get_db)):
    short = (
        db.query(models.ShortAnswerQuestion)
        .filter(models.ShortAnswerQuestion.id == short_id)
        .first()
    )
    if not short:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 주관식 질문이 존재하지 않습니다.",
        )
    return short


@router.post(
    "/",
    response_model=schemas.ShortAnswerQuestionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_short(
    short: schemas.ShortAnswerQuestionCreate, db: Session = Depends(get_db)
):
    db_short = models.ShortAnswerQuestion(**short.model_dump())
    db.add(db_short)
    db.commit()
    db.refresh(db_short)
    return db_short


@router.patch("/{short_id}", response_model=schemas.ShortAnswerQuestionOut)
def update_short(
    short_id: int,
    update_data: schemas.ShortAnswerQuestionUpdate,
    db: Session = Depends(get_db),
):
    short = (
        db.query(models.ShortAnswerQuestion)
        .filter(models.ShortAnswerQuestion.id == short_id)
        .first()
    )
    if not short:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 주관식 질문이 존재하지 않습니다.",
        )

    data = update_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="업데이트할 필드를 최소 한 개 이상 제공해야 합니다.",
        )

    for key, value in data.items():
        setattr(short, key, value)
    db.commit()
    db.refresh(short)
    return short


@router.delete("/{short_id}", status_code=status.HTTP_200_OK)
def delete_short(short_id: int, db: Session = Depends(get_db)):
    short = (
        db.query(models.ShortAnswerQuestion)
        .filter(models.ShortAnswerQuestion.id == short_id)
        .first()
    )
    if not short:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 주관식 질문이 존재하지 않습니다.",
        )
    db.delete(short)
    db.commit()
    return {"message": "주관식 질문이 삭제되었습니다."}
