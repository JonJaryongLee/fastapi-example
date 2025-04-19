from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
import pytest


# client fixture 추가: 각 테스트마다 TestClient(app) 인스턴스를 제공합니다.
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_create_question_success(client):
    now = datetime.now()
    payload = {
        "title": "Test Question Info",
        "start_date": now.isoformat(),
        "end_date": (now + timedelta(days=1)).isoformat(),
    }
    response = client.post("/question-infos/", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Test Question Info"
    # 자동 생성된 필드 검증
    assert "created_at" in data
    assert "updated_at" in data

    # 중첩 필드 (multiple_choice_questions, short_answer_questions)는 빈 리스트여야 함
    assert (
        isinstance(data["multiples"], list)
        and len(data["multiples"]) == 0
    )
    assert (
        isinstance(data["shorts"], list)
        and len(data["shorts"]) == 0
    )


def test_get_question_info_list(client):
    # 목록 조회 전 새 질문 생성(리스트에 반영되었는지 확인)
    now = datetime.now()
    payload = {
        "title": "List Test Question Info",
        "start_date": now.isoformat(),
        "end_date": (now + timedelta(days=1)).isoformat(),
    }
    create_resp = client.post("/question-infos/", json=payload)
    assert create_resp.status_code == 201
    response = client.get("/question-infos/")
    assert response.status_code == 200, response.text
    question_infos = response.json()
    assert any(q["title"] == "List Test Question Info" for q in question_infos)


def test_get_question_info_success(client):
    now = datetime.now()
    payload = {
        "title": "Detail Test Question Info",
        "start_date": now.isoformat(),
        "end_date": (now + timedelta(days=1)).isoformat(),
    }
    create_resp = client.post("/question-infos/", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    q_id = created["id"]

    response = client.get(f"/question-infos/{q_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == q_id
    assert data["title"] == "Detail Test Question Info"


def test_get_question_info_not_found(client):
    response = client.get("/question-infos/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "질문지가 존재하지 않습니다."


def test_update_question_info_success(client):
    now = datetime.now()
    payload = {
        "title": "Update Test Question Info",
        "start_date": now.isoformat(),
        "end_date": (now + timedelta(days=1)).isoformat(),
    }
    create_resp = client.post("/question-infos/", json=payload)
    assert create_resp.status_code == 201
    q_id = create_resp.json()["id"]

    update_payload = {"title": "Updated Question Info Title"}
    response = client.patch(f"/question-infos/{q_id}", json=update_payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Updated Question Info Title"


def test_update_question_info_no_data(client):
    now = datetime.now()
    payload = {
        "title": "No Data Update Question Info",
        "start_date": now.isoformat(),
        "end_date": (now + timedelta(days=1)).isoformat(),
    }
    create_resp = client.post("/question-infos/", json=payload)
    assert create_resp.status_code == 201
    q_id = create_resp.json()["id"]

    response = client.patch(f"/question-infos/{q_id}", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "업데이트할 필드를 최소 한 개 이상 제공해야 합니다."


def test_update_question_info_not_found(client):
    response = client.patch("/question-infos/999999", json={"title": "Non-existent"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "질문지가 존재하지 않습니다."


def test_delete_question_info_success(client):
    now = datetime.now()
    payload = {
        "title": "Delete Test Question Info",
        "start_date": now.isoformat(),
        "end_date": (now + timedelta(days=1)).isoformat(),
    }
    create_resp = client.post("/question-infos/", json=payload)
    assert create_resp.status_code == 201
    q_id = create_resp.json()["id"]

    response = client.delete(f"/question-infos/{q_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "질문지가 삭제되었습니다."

    # 삭제 후 조회 시 404 검증
    get_response = client.get(f"/question-infos/{q_id}")
    assert get_response.status_code == 404


def test_delete_question_info_not_found(client):
    response = client.delete("/question-infos/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "질문지가 존재하지 않습니다."
