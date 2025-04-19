from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./question.db"

# SQLite는 싱글 스레드 검사 옵션이 필요합니다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def init_db():
    # 모델을 임포트해서 테이블 생성 시키기 (순환 임포트 주의)
    from app import models

    Base.metadata.create_all(bind=engine)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()