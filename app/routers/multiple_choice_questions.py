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


@router.get("/{multiple_id}", response_model=schemas.MultipleChoiceQuestionOut)
def get_multiple(multiple_id: int, db: Session = Depends(get_db)):
    multiple = (
        db.query(models.MultipleChoiceQuestion)
        .filter(models.MultipleChoiceQuestion.id == multiple_id)
        .first()
    )
    if not multiple:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 객관식 질문이 존재하지 않습니다.",
        )
    return multiple


@router.post(
    "/",
    response_model=schemas.MultipleChoiceQuestionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_multiple(
    multiple: schemas.MultipleChoiceQuestionCreate, db: Session = Depends(get_db)
):
    db_multiple = models.MultipleChoiceQuestion(**multiple.model_dump())
    db.add(db_multiple)
    db.commit()
    db.refresh(db_multiple)
    return db_multiple


@router.patch("/{multiple_id}", response_model=schemas.MultipleChoiceQuestionOut)
def update_multiple(
    multiple_id: int,
    update_data: schemas.MultipleChoiceQuestionUpdate,
    db: Session = Depends(get_db),
):
    multiple = (
        db.query(models.MultipleChoiceQuestion)
        .filter(models.MultipleChoiceQuestion.id == multiple_id)
        .first()
    )
    if not multiple:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 객관식 질문이 존재하지 않습니다.",
        )

    data = update_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="업데이트할 필드를 최소 한 개 이상 제공해야 합니다.",
        )

    for key, value in data.items():
        setattr(multiple, key, value)
    db.commit()
    db.refresh(multiple)
    return multiple


@router.delete("/{multiple_id}", status_code=status.HTTP_200_OK)
def delete_multiple(multiple_id: int, db: Session = Depends(get_db)):
    multiple = (
        db.query(models.MultipleChoiceQuestion)
        .filter(models.MultipleChoiceQuestion.id == multiple_id)
        .first()
    )
    if not multiple:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 객관식 질문이 존재하지 않습니다.",
        )
    db.delete(multiple)
    db.commit()
    return {"message": "객관식 질문이 삭제되었습니다."}
