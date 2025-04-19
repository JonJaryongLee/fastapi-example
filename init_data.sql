-- 문제 정보 테이블 생성
CREATE TABLE IF NOT EXISTS question_infos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- 객관식 문제 테이블 생성
CREATE TABLE IF NOT EXISTS multiple_choice_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    type VARCHAR(10) NOT NULL DEFAULT '객관식',
    score INTEGER NOT NULL,
    text1 VARCHAR(50) NOT NULL,
    text2 VARCHAR(50) NOT NULL,
    text3 VARCHAR(50) NOT NULL,
    text4 VARCHAR(50) NOT NULL,
    answer_num INTEGER NOT NULL,
    question_info_id INTEGER NOT NULL,
    img_src TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (question_info_id) REFERENCES question_infos(id)
);

-- 주관식 문제 테이블 생성
CREATE TABLE IF NOT EXISTS short_answer_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    type VARCHAR(10) NOT NULL DEFAULT '주관식',
    score INTEGER NOT NULL,
    answer_ex VARCHAR(200),
    question_info_id INTEGER NOT NULL,
    img_src TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (question_info_id) REFERENCES question_infos(id)
);

--------------------------------------------------
-- 더미 데이터 삽입: 문제 정보 테이블
--------------------------------------------------
-- 1. Java 리팩토링 문제 세트 (2025-01-01)
INSERT INTO question_infos (title, start_date, end_date, created_at, updated_at) VALUES 
('Java 리팩토링 문제 세트', '2025-01-01 09:00:00', '2025-01-01 11:00:00', '2025-01-01 06:00:00', '2025-01-01 06:00:00');

-- 2. Python 리팩토링 문제 세트 (2025-02-01)
INSERT INTO question_infos (title, start_date, end_date, created_at, updated_at) VALUES 
('Python 리팩토링 문제 세트', '2025-02-01 09:00:00', '2025-02-01 11:00:00', '2025-02-01 06:00:00', '2025-02-01 06:00:00');

-- 3. C++ 리팩토링 문제 세트 (2025-03-01)
INSERT INTO question_infos (title, start_date, end_date, created_at, updated_at) VALUES 
('C++ 리팩토링 문제 세트', '2025-03-01 09:00:00', '2025-03-01 11:00:00', '2025-03-01 06:00:00', '2025-03-01 06:00:00');

--------------------------------------------------
-- 더미 데이터 삽입: 객관식 문제 (multiple_choice_questions)
--------------------------------------------------

-- [Java 리팩토링 객관식 문제; question_info_id = 1]
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('메서드 추출의 목적은 무엇인가요?', 5, '코드 재사용성', '의존성 증가', '가독성 향상', '성능 저하', 3, 1, NULL, '2025-01-01 07:00:00', '2025-01-01 07:05:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('Java에서 리팩토링 시 가장 중요한 고려 사항은?', 5, '테스트 자동화', '코드 간결성', '주석 추가', '문서화', 1, 1, NULL, '2025-01-01 07:06:00', '2025-01-01 07:06:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('리팩토링 부작용 방지 방법은 무엇인가요?', 5, '코드 리뷰', '리팩토링 전후 테스트', '성능 측정', '리팩토링 배제', 2, 1, NULL, '2025-01-01 07:12:00', '2025-01-01 07:51:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('메서드 인라인의 효과는 무엇인가요?', 5, '불필요한 추상화 제거', '복잡한 알고리즘 도입', '중복 코드 생성', '오류 증가', 1, 1, NULL, '2025-01-01 07:28:00', '2025-01-01 07:28:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('클래스 추출의 주 목적은 무엇인가요?', 5, '책임 분리', '성능 최적화', '메모리 관리', 'UI 개선', 1, 1, NULL, '2025-01-01 07:36:00', '2025-01-01 07:38:00');

-- [Python 리팩토링 객관식 문제; question_info_id = 2]
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('파이썬 리팩토링 시 우선 고려사항은 무엇인가요?', 5, '코드 가독성', '메모리 최적화', '동시성 제어', 'GUI 개선', 1, 2, NULL, '2025-02-01 06:58:00', '2025-02-01 06:58:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('함수 추출의 주요 목적은 무엇인가요?', 5, '함수 분할', '중복 제거', '에러 증가', '성능 저하', 2, 2, NULL, '2025-02-01 07:02:00', '2025-02-01 07:03:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('리팩토링 후 실행해야 할 필수 절차는?', 5, '문서 리뷰', '코드 포매팅', '유닛 테스트', '코드 압축', 3, 2, NULL, '2025-02-01 07:07:00', '2025-02-01 07:07:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('리스트 내포 사용의 장점은?', 5, '코드 간결', '속도 향상', '메모리 절약', '디버깅 용이', 1, 2, NULL, '2025-02-01 07:10:00', '2025-02-01 07:12:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('함수형 프로그래밍의 리팩토링 이점은?', 5, '불변성 보장', '동적 타이핑', '반복문 사용', '예외 무시', 1, 2, NULL, '2025-02-01 07:15:00', '2025-02-01 07:15:00');

-- [C++ 리팩토링 객관식 문제; question_info_id = 3]
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('C++ 리팩토링 시 주의해야 할 사항은?', 5, '메모리 관리', '가비지 컬렉션', '동적 바인딩', '포인터 사용', 1, 3, NULL, '2025-03-01 06:30:00', '2025-03-01 06:30:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('클래스 내 함수 분할의 목적은?', 5, '코드 복잡도 감소', '함수 호출 비용 감소', '하드웨어 제어', '컴파일 시간 단축', 1, 3, NULL, '2025-03-01 06:42:00', '2025-03-01 06:53:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('템플릿 리팩토링의 장점은 무엇인가요?', 5, '유연성 향상', '러닝커브 감소', '오버헤드 증가', '메모리 누수', 1, 3, NULL, '2025-03-01 06:58:00', '2025-03-01 06:59:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('스마트 포인터 사용의 주요 이점은?', 5, '자동 메모리 관리', '성능 저하', '코드 길이 증가', '명시적 해제', 1, 3, NULL, '2025-03-01 07:16:00', '2025-03-01 07:16:00');
INSERT INTO multiple_choice_questions (title, score, text1, text2, text3, text4, answer_num, question_info_id, img_src, created_at, updated_at) VALUES 
('리팩토링 후 컴파일 에러 예방 방법은?', 5, '정적 분석 도구 사용', '주석 처리', '리팩토링 제한', '의존성 제거', 1, 3, NULL, '2025-03-01 07:18:00', '2025-03-01 07:18:00');

--------------------------------------------------
-- 더미 데이터 삽입: 주관식 문제 (short_answer_questions)
--------------------------------------------------

-- [Java 리팩토링 주관식 문제; question_info_id = 1]
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('리팩토링 시 코드 중복 감소 방법에 대해 설명하세요.', 5, '메서드 추출과 클래스 분리를 통해 중복을 제거합니다.', 1, NULL, '2025-01-01 07:38:00', '2025-01-01 07:39:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('메서드 인라인의 장단점을 설명하세요.', 5, '가독성 향상과 재사용성 감소가 주요 장단점입니다.', 1, NULL, '2025-01-01 07:40:00', '2025-01-01 07:40:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('리팩토링 전후 테스트의 중요성을 논하세요.', 5, '테스트는 변경에 따른 부작용을 검증하는 필수 단계입니다.', 1, NULL, '2025-01-01 07:41:00', '2025-01-01 07:41:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('클래스 추출 리팩토링의 적절한 시기를 설명하세요.', 5, '클래스의 역할이 모호해질 때 추출하는 것이 적절합니다.', 1, NULL, '2025-01-01 07:43:00', '2025-01-01 07:43:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('리팩토링 도구의 효과에 대해 평가하세요.', 5, '도구는 리팩토링을 일관되게 수행할 수 있게 돕습니다.', 1, NULL, '2025-01-01 07:52:00', '2025-01-01 07:54:00');

-- [Python 리팩토링 주관식 문제; question_info_id = 2]
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('파이썬에서 중복 코드를 줄이는 방법을 설명하세요.', 5, '함수와 클래스로 코드를 재구성하여 중복을 제거합니다.', 2, NULL, '2025-02-01 07:16:00', '2025-02-01 07:16:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('리팩토링 전후 테스트의 필요성을 서술하세요.', 5, '기능 보장을 위해 체계적인 테스트가 필수입니다.', 2, NULL, '2025-02-01 07:23:00', '2025-02-01 07:23:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('가독성을 높이는 리팩토링 기법을 설명하세요.', 5, '명확한 변수명과 함수 분리, PEP8 준수가 중요합니다.', 2, NULL, '2025-02-01 07:25:00', '2025-02-01 07:26:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('리스트 내포 사용 시 주의할 점을 기술하세요.', 5, '과도한 중첩은 가독성을 해칠 수 있으니 적절히 사용합니다.', 2, NULL, '2025-02-01 07:31:00', '2025-02-01 07:31:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('함수형 프로그래밍이 코드 리팩토링에 미치는 영향을 논하세요.', 5, '불변성과 순수 함수 개념이 코드를 안정적으로 만듭니다.', 2, NULL, '2025-02-01 07:32:00', '2025-02-01 07:36:00');

-- [C++ 리팩토링 주관식 문제; question_info_id = 3]
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('C++에서 포인터 사용 개선 방법을 설명하세요.', 5, '스마트 포인터 도입으로 메모리 관리를 자동화합니다.', 3, NULL, '2025-03-01 07:19:00', '2025-03-01 07:19:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('클래스 분리 리팩토링의 필요성을 서술하세요.', 5, '클래스의 책임을 분리하면 유지보수가 수월해집니다.', 3, NULL, '2025-03-01 07:20:00', '2025-03-01 07:20:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('템플릿 활용의 장단점에 대해 논하세요.', 5, '중복 제거와 유연성 향상에 도움이 되지만, 컴파일 시간이 길어질 수 있습니다.', 3, NULL, '2025-03-01 07:22:00', '2025-03-01 07:22:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('동적 메모리 관리의 문제점을 설명하세요.', 5, '직접 관리하면 메모리 누수 위험이 있으며, 스마트 포인터 사용이 권장됩니다.', 3, NULL, '2025-03-01 07:23:00', '2025-03-01 07:23:00');
INSERT INTO short_answer_questions (title, score, answer_ex, question_info_id, img_src, created_at, updated_at) VALUES 
('정적 분석 도구가 리팩토링에 미치는 영향을 평가하세요.', 5, '코드 품질을 보장하며, 리팩토링 후 오류를 예방하는 데 유용합니다.', 3, NULL, '2025-03-01 07:30:00', '2025-03-01 07:32:00');