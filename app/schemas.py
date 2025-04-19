from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional

# ----------------------------------------------------------------------
# 질문 관련 스키마 (question_infos, multiple_choice_questions, short_answer_questions)
# ----------------------------------------------------------------------


# ===== QuestionInfo 관련 =====
class QuestionInfoBase(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime


class QuestionInfoCreate(QuestionInfoBase):
    pass


class QuestionInfoUpdate(BaseModel):
    title: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# 리스트 조회용 (GET /question-infos)
class QuestionInfoOut(BaseModel):
    id: int
    title: str
    start_date: datetime
    end_date: datetime

    model_config = ConfigDict(from_attributes=True)


# --- 객관식/주관식 문제를 중첩하여 보여주기 위한 스키마 ---
class MultipleChoiceQuestionNested(BaseModel):
    id: int
    title: str
    score: int
    answer_num: int
    text1: str
    text2: str
    text3: str
    text4: str
    img_src: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ShortAnswerQuestionNested(BaseModel):
    id: int
    title: str
    score: int
    answer_ex: Optional[str] = None
    img_src: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# 상세 조회용 (GET /question-infos/{id})
# 전체 테이블 필드 + 객관식 문제 배열(multiples) + 주관식 문제 배열(shorts)
class QuestionInfoDetail(QuestionInfoOut):
    # 추가 필드
    created_at: datetime
    updated_at: datetime
    multiple_choice_questions: List[MultipleChoiceQuestionNested] = Field(
        default_factory=list, alias="multiples"
    )
    short_answer_questions: List[ShortAnswerQuestionNested] = Field(
        default_factory=list, alias="shorts"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# ===== MultipleChoiceQuestion 관련 =====
class MultipleChoiceQuestionBase(BaseModel):
    title: str
    score: int
    text1: str
    text2: str
    text3: str
    text4: str
    answer_num: int
    question_info_id: int
    img_src: Optional[str] = None


class MultipleChoiceQuestionCreate(MultipleChoiceQuestionBase):
    pass


class MultipleChoiceQuestionUpdate(BaseModel):
    title: Optional[str] = None
    score: Optional[int] = None
    text1: Optional[str] = None
    text2: Optional[str] = None
    text3: Optional[str] = None
    text4: Optional[str] = None
    answer_num: Optional[int] = None
    question_info_id: Optional[int] = None
    img_src: Optional[str] = None


# question_info 객체를 간략하게 반환하는 스키마 (id, title)
class QuestionInfoSimple(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class MultipleChoiceQuestionOut(BaseModel):
    id: int
    title: str
    score: int
    text1: str
    text2: str
    text3: str
    text4: str
    answer_num: int
    img_src: Optional[str] = None
    question_info: QuestionInfoSimple

    model_config = ConfigDict(from_attributes=True)


# ===== ShortAnswerQuestion 관련 =====
class ShortAnswerQuestionBase(BaseModel):
    title: str
    score: int
    question_info_id: int
    img_src: Optional[str] = None
    answer_ex: Optional[str] = None


class ShortAnswerQuestionCreate(ShortAnswerQuestionBase):
    pass


class ShortAnswerQuestionUpdate(BaseModel):
    title: Optional[str] = None
    score: Optional[int] = None
    question_info_id: Optional[int] = None
    img_src: Optional[str] = None
    answer_ex: Optional[str] = None


class ShortAnswerQuestionOut(BaseModel):
    id: int
    title: str
    score: int
    img_src: Optional[str] = None
    answer_ex: Optional[str] = None
    question_info: QuestionInfoSimple

    model_config = ConfigDict(from_attributes=True)
