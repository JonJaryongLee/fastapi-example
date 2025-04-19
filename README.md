# FastAPI + SQLite

## 필요한것들  

- Python3.13  
- SQLite3  
- GitBash (Windows)  

## 실행  

`5000` 번 포트를 사용하겠습니다.  

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

# 배포  
gunicorn 내부에서 uvicorn 을 구동합니다.  

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 app.main:app
```

워커의 갯수는 현재 4개입니다. 이것은 CPU 코어 갯수와 관련있습니다.  
워커 갯수 공식: CPU 코어 수 × 2 + 1  
단, 도커를 사용한다면 컨테이너에 할당된 코어 갯수 기준으로 계산해주세요.  

## 더미데이터를 세팅하고 싶다면?    

```bash
sqlite3 question.db < init_data.sql
``` 

# API 문서  
- http://127.0.0.1:5000/docs  
- http://127.0.0.1:5000/redoc 