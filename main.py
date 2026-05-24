import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


DATA_FILE = Path(__file__).with_name("courses.json")
VALID_GRADES = {"A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F", "P", "NP"}

app = FastAPI(title="Course Records API")


class Course(BaseModel):
    course_name: str = Field(..., min_length=1)
    year: str = Field(..., min_length=4, max_length=4)
    semester: str = Field(..., min_length=1, max_length=1)
    grade: str = Field(..., min_length=1)


def read_courses() -> list[dict[str, Any]]:
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="courses.json 파일을 읽을 수 없습니다.",
        ) from exc

    if not isinstance(data, list):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="courses.json 파일은 list 형태여야 합니다.",
        )

    return data


def write_courses(courses: list[dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(courses, file, ensure_ascii=False, indent=2)
        file.write("\n")


def validate_course(course: Course) -> None:
    if not course.year.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="year는 4자리 숫자 문자열이어야 합니다.",
        )

    if course.semester not in {"1", "2"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="semester는 '1' 또는 '2'여야 합니다.",
        )

    if course.grade not in VALID_GRADES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="grade 값이 허용 범위를 벗어났습니다.",
        )


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Course Records API", "courses_url": "/courses"}


@app.get("/courses")
def get_courses() -> list[dict[str, Any]]:
    return read_courses()


@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: Course) -> dict[str, Any]:
    validate_course(course)

    courses = read_courses()
    new_course = course.model_dump() if hasattr(course, "model_dump") else course.dict()
    courses.append(new_course)
    write_courses(courses)

    return {"message": "course added", "course": new_course, "total": len(courses)}
