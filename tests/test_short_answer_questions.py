from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import pytest
from app.main import app


# client fixture 추가: 각 테스트마다 TestClient(app) 인스턴스를 생성합니다.
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def create_test_question_info(client):
    """
    주관식 문제를 생성하기 위한 부모(QuestionInfo)를 생성.
    """
    now = datetime.now()
    payload = {
        "title": "Parent Question Info for Shorts",
        "start_date": now.isoformat(),
        "end_date": (now + timedelta(days=1)).isoformat(),
    }
    response = client.post("/question-infos/", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def create_test_short(client, question_info_id: int):
    """
    주관식 문제(ShortAnswerQuestion)를 생성.
    """
    payload = {
        "title": "Test Short Answer",
        "score": 5,
        "question_info_id": question_info_id,
        "img_src": "http://example.com/short.png",
        "answer_ex": "Expected answer",
    }
    return client.post("/short-answer-questions/", json=payload)


def test_create_short_success(client):
    parent = create_test_question_info(client)
    response = create_test_short(client, parent["id"])
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Test Short Answer"
    assert data["score"] == 5
    assert data["answer_ex"] == "Expected answer"
    # 부모 QuestionInfo 검증
    assert "question_info" in data
    assert data["question_info"]["id"] == parent["id"]


def test_create_short_missing_field(client):
    parent = create_test_question_info(client)
    payload = {
        # "title" 누락
        "score": 5,
        "question_info_id": parent["id"],
        "img_src": "http://example.com/short.png",
        "answer_ex": "Expected answer",
    }
    response = client.post("/short-answer-questions/", json=payload)
    assert response.status_code == 422


def test_get_short_success(client):
    parent = create_test_question_info(client)
    create_resp = create_test_short(client, parent["id"])
    short_data = create_resp.json()
    short_id = short_data["id"]

    response = client.get(f"/short-answer-questions/{short_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == short_id
    assert data["title"] == "Test Short Answer"


def test_get_short_not_found(client):
    response = client.get("/short-answer-questions/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "해당 주관식 질문이 존재하지 않습니다."


def test_update_short_success(client):
    parent = create_test_question_info(client)
    create_resp = create_test_short(client, parent["id"])
    short_id = create_resp.json()["id"]

    update_payload = {
        "title": "Updated Short Answer",
        "score": 10,
        "answer_ex": "Updated expected answer",
    }
    response = client.patch(f"/short-answer-questions/{short_id}", json=update_payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Updated Short Answer"
    assert data["score"] == 10
    assert data["answer_ex"] == "Updated expected answer"


def test_update_short_no_data(client):
    parent = create_test_question_info(client)
    create_resp = create_test_short(client, parent["id"])
    short_id = create_resp.json()["id"]

    response = client.patch(f"/short-answer-questions/{short_id}", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "업데이트할 필드를 최소 한 개 이상 제공해야 합니다."


def test_update_short_not_found(client):
    response = client.patch("/short-answer-questions/999999", json={"title": "Non-existent"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "해당 주관식 질문이 존재하지 않습니다."


def test_delete_short_success(client):
    parent = create_test_question_info(client)
    create_resp = create_test_short(client, parent["id"])
    short_id = create_resp.json()["id"]

    response = client.delete(f"/short-answer-questions/{short_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "주관식 질문이 삭제되었습니다."
    # 삭제 후 GET 시 404 검증
    get_resp = client.get(f"/short-answer-questions/{short_id}")
    assert get_resp.status_code == 404


def test_delete_short_not_found(client):
    response = client.delete("/short-answer-questions/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "해당 주관식 질문이 존재하지 않습니다."
