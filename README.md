# OSS HW5 - FastAPI Course Records

FastAPI로 수강기록을 조회하고 추가하는 간단한 REST API 서버입니다. 데이터는 `courses.json` 파일에서 읽고, `POST /courses` 요청이 들어오면 같은 파일에 다시 저장합니다.

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

서버 실행 후 아래 주소에서 API 문서를 확인할 수 있습니다.

```text
http://127.0.0.1:8000/docs
```

## API

### GET /courses

현재 `courses.json`에 저장된 전체 수강기록 목록을 반환합니다.

```bash
curl http://127.0.0.1:8000/courses
```

### POST /courses

새 수강기록을 추가하고 `courses.json`에 저장합니다.

```bash
curl -X POST http://127.0.0.1:8000/courses \
  -H "Content-Type: application/json" \
  -d '{
    "course_name": "인간로봇상호작용",
    "year": "2026",
    "semester": "2",
    "grade": "A+"
  }'
```

요청 필드는 `course_name`, `year`, `semester`, `grade`입니다. 잘못된 형식의 요청은 에러 응답을 반환하며 서버는 계속 실행됩니다.
