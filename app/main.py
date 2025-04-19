from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import question_infos, multiple_choice_questions, short_answer_questions

# 데이터베이스 초기화
init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 포함 (prefix와 tags는 API 문서에 도움을 줍니다)
app.include_router(question_infos.router, prefix="/question-infos", tags=["QuestionInfos"])
app.include_router(
    multiple_choice_questions.router,
    prefix="/multiple-choice-questions",
    tags=["MultipleChoiceQuestions"],
)
app.include_router(
    short_answer_questions.router,
    prefix="/short-answer-questions",
    tags=["ShortAnswerQuestions"],
)


@app.get("/")
def read_root():
    return {"message": "FastAPI 프로젝트에 오신 것을 환영합니다!"}
