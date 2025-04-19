from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class QuestionInfo(Base):
    __tablename__ = "question_infos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # 1:N 관계 설정: 하나의 QuestionInfo가 여러 개의 MultipleChoiceQuestion, ShortAnswerQuestion를 가질 수 있음.
    multiple_choice_questions = relationship(
        "MultipleChoiceQuestion",
        back_populates="question_info",
        cascade="all, delete-orphan",
    )
    short_answer_questions = relationship(
        "ShortAnswerQuestion",
        back_populates="question_info",
        cascade="all, delete-orphan",
    )


# 추상 베이스 클래스
class Question(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    question_info_id = Column(Integer, ForeignKey("question_infos.id"), nullable=False)
    img_src = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )


# 객관식 문제: 추상 클래스로부터 상속받으며, 추가적인 필드들을 정의
class MultipleChoiceQuestion(Question):
    __tablename__ = "multiple_choice_questions"

    # 문제 타입을 명시적으로 재정의 (default와 server_default 포함)
    type = Column(String(10), nullable=False, default="객관식", server_default="객관식")
    # 객관식 선택지 관련 필드
    text1 = Column(String(50), nullable=False)
    text2 = Column(String(50), nullable=False)
    text3 = Column(String(50), nullable=False)
    text4 = Column(String(50), nullable=False)
    answer_num = Column(Integer, nullable=False)

    # 관계 설정: 이 질문의 상위 QuestionInfo
    question_info = relationship(
        "QuestionInfo", back_populates="multiple_choice_questions"
    )


# 주관식 문제: 추상 클래스로부터 상속받으며, 추가적인 필드들을 정의
class ShortAnswerQuestion(Question):
    __tablename__ = "short_answer_questions"

    # 문제 타입을 명시적으로 재정의 (default와 server_default 포함)
    type = Column(String(10), nullable=False, default="주관식", server_default="주관식")
    # 주관식의 경우 예시 답안을 첨부할 수 있음
    answer_ex = Column(String(200), nullable=True)

    # 관계 설정: 이 질문의 상위 QuestionInfo
    question_info = relationship(
        "QuestionInfo", back_populates="short_answer_questions"
    )
