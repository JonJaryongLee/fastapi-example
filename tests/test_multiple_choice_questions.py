from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
import pytest


# client fixture 추가: 각 테스트마다 새 인스턴스를 생성합니다.
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def create_test_question(client):
    """
    객관식 문제를 생성하기 위한 부모(QuestionInfo)를 생성.
    """
    now = datetime.now()
    payload = {
        "title": "Parent Question for Multiples",
        "start_date": now.isoformat(),
        "end_date": (now + timedelta(days=1)).isoformat(),
    }
    response = client.post("/question-infos/", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def create_test_multiple(client, question_info_id: int):
    """
    객관식 문제(MultipleChoiceQuestion)를 생성.
    """
    payload = {
        "title": "Test Multiple",
        "score": 10,
        "text1": "Option A",
        "text2": "Option B",
        "text3": "Option C",
        "text4": "Option D",
        "answer_num": 1,
        "question_info_id": question_info_id,
        "img_src": "http://example.com/image.png",
    }
    return client.post("/multiple-choice-questions/", json=payload)


def test_create_multiple_success(client):
    parent = create_test_question(client)
    response = create_test_multiple(client, parent["id"])
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Test Multiple"
    assert data["score"] == 10
    assert data["answer_num"] == 1
    assert data["text1"] == "Option A"
    # 관계로 포함된 부모 QuestionInfo 검증
    assert "question_info" in data
    assert data["question_info"]["id"] == parent["id"]


def test_create_multiple_missing_field(client):
    """
    필수 필드(title)를 누락했을 때 422(Unprocessable Entity)가 반환되는지 확인.
    """
    parent = create_test_question(client)
    payload = {
        # "title" 누락
        "score": 10,
        "text1": "Option A",
        "text2": "Option B",
        "text3": "Option C",
        "text4": "Option D",
        "answer_num": 1,
        "question_info_id": parent["id"],
        "img_src": "http://example.com/image.png",
    }
    response = client.post("/multiple-choice-questions/", json=payload)
    assert response.status_code == 422


def test_get_multiple_success(client):
    parent = create_test_question(client)
    create_resp = create_test_multiple(client, parent["id"])
    mult_data = create_resp.json()
    mult_id = mult_data["id"]

    response = client.get(f"/multiple-choice-questions/{mult_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == mult_id
    assert data["title"] == "Test Multiple"


def test_get_multiple_not_found(client):
    response = client.get("/multiple-choice-questions/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "해당 객관식 질문이 존재하지 않습니다."


def test_update_multiple_success(client):
    parent = create_test_question(client)
    create_resp = create_test_multiple(client, parent["id"])
    mult_data = create_resp.json()
    mult_id = mult_data["id"]

    update_payload = {"title": "Updated Multiple", "score": 20}
    response = client.patch(f"/multiple-choice-questions/{mult_id}", json=update_payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Updated Multiple"
    assert data["score"] == 20


def test_update_multiple_no_data(client):
    parent = create_test_question(client)
    create_resp = create_test_multiple(client, parent["id"])
    mult_id = create_resp.json()["id"]

    response = client.patch(f"/multiple-choice-questions/{mult_id}", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "업데이트할 필드를 최소 한 개 이상 제공해야 합니다."


def test_update_multiple_not_found(client):
    response = client.patch(
        "/multiple-choice-questions/999999", json={"title": "Non-existent"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "해당 객관식 질문이 존재하지 않습니다."


def test_delete_multiple_success(client):
    parent = create_test_question(client)
    create_resp = create_test_multiple(client, parent["id"])
    mult_id = create_resp.json()["id"]

    response = client.delete(f"/multiple-choice-questions/{mult_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "객관식 질문이 삭제되었습니다."
    # 삭제 후 GET 시 404 검증
    get_resp = client.get(f"/multiple-choice-questions/{mult_id}")
    assert get_resp.status_code == 404


def test_delete_multiple_not_found(client):
    response = client.delete("/multiple-choice-questions/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "해당 객관식 질문이 존재하지 않습니다."
