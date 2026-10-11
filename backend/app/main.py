from fastapi import Depends, FastAPI, HTTPException, Query, Response
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas import (
    CourseResponse,
    SectionResponse,
    SectionCapacityUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
)

app = FastAPI(title="CourseHub API")


@app.get("/")
def read_root():
    return {"message": "CourseHub API dang hoat dong"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )

@app.get("/lecturers")
def get_lecturers(db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            SELECT id, name
            FROM lecturers
            ORDER BY id
        """)
    ).mappings().all()

    return [dict(row) for row in result]



@app.get("/courses", response_model=list[CourseResponse])
def get_courses(
    q: str | None = Query(default=None, description="Tim theo ma hoac ten mon hoc"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
    db: Session = Depends(get_db),
):
    sql = """
        SELECT code, name, credits
        FROM courses
    """
    params = {}

    if q is not None:
        q = q.strip()

        if not q:
            raise HTTPException(
                status_code=400,
                detail="Search keyword cannot be empty",
            )

        sql += """
            WHERE code ILIKE :keyword
               OR name ILIKE :keyword
        """
        params["keyword"] = f"%{q}%"

    sql += " ORDER BY code LIMIT :limit OFFSET :skip"
    params["limit"] = limit
    params["skip"] = skip

    result = db.execute(text(sql), params).mappings().all()
    return [dict(row) for row in result]



@app.get("/courses/{course_code}", response_model=CourseResponse)
def get_course(
    course_code: str,
    db: Session = Depends(get_db),
):
    result = db.execute(
        text("""
            SELECT code, name, credits
            FROM courses
            WHERE code = :course_code
        """),
        {"course_code": course_code},
    ).mappings().first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return dict(result)


@app.get("/sections", response_model=list[SectionResponse])
def get_sections(
    available_only: bool = False,
    db: Session = Depends(get_db),
):
    sql = """
        SELECT
            class_id AS id,
            course_code,
            capacity,
            enrolled AS enrolled_count,
            remaining AS remaining_slots
        FROM v_section_summary
    """

    if available_only:
        sql += " WHERE remaining > 0"

    sql += " ORDER BY class_id"

    result = db.execute(text(sql)).mappings().all()
    return [dict(row) for row in result]

@app.get("/sections/{section_id}")
def get_section_detail(
    section_id: str,
    db: Session = Depends(get_db),
):
    result = db.execute(
        text("""
            SELECT
                cs.id AS id,
                cs.course_code,
                c.name AS course_name,
                sem.code AS semester_code,
                sem.name AS semester_name,
                l.id AS lecturer_id,
                l.name AS lecturer_name,
                v.capacity,
                v.enrolled,
                v.remaining
            FROM class_sections AS cs
            JOIN courses AS c
                ON c.code = cs.course_code
            JOIN semesters AS sem
                ON sem.code = cs.semester_code
            JOIN lecturers AS l
                ON l.id = cs.lecturer_id
            JOIN v_section_summary AS v
                ON v.class_id = cs.id
            WHERE cs.id = :section_id
        """),
        {"section_id": section_id},
    ).mappings().first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Class section not found",
        )

    return dict(result)

@app.patch("/sections/{section_id}/capacity")
def update_section_capacity(
    section_id: str,
    payload: SectionCapacityUpdate,
    db: Session = Depends(get_db),
):
    section = db.execute(
        text("""
            SELECT capacity
            FROM class_sections
            WHERE id = :section_id
        """),
        {"section_id": section_id},
    ).mappings().first()

    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Class section not found",
        )

    enrolled_count = db.execute(
        text("""
            SELECT COUNT(*) AS total
            FROM enrollments
            WHERE class_section_id = :section_id
        """),
        {"section_id": section_id},
    ).scalar_one()

    if payload.capacity < enrolled_count:
        raise HTTPException(
            status_code=409,
            detail="Capacity cannot be lower than current enrollment",
        )

    db.execute(
        text("""
            UPDATE class_sections
            SET capacity = :capacity
            WHERE id = :section_id
        """),
        {
            "capacity": payload.capacity,
            "section_id": section_id,
        },
    )
    db.commit()

    return {
        "id": section_id,
        "capacity": payload.capacity,
        "enrolled_count": enrolled_count,
        "remaining": payload.capacity - enrolled_count,
    }


@app.get(
    "/students/{student_id}/enrollments",
    response_model=list[EnrollmentResponse],
)
def get_student_enrollments(
    student_id: str,
    db: Session = Depends(get_db),
):
    student = db.execute(
        text("SELECT id FROM students WHERE id = :student_id"),
        {"student_id": student_id},
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    result = db.execute(
        text("""
            SELECT student_id, class_section_id, registered_at
            FROM enrollments
            WHERE student_id = :student_id
            ORDER BY class_section_id
        """),
        {"student_id": student_id},
    ).mappings().all()

    return [dict(row) for row in result]


@app.post(
    "/enrollments",
    response_model=EnrollmentResponse,
    status_code=201,
)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
):
    try:
        student = db.execute(
            text("SELECT id FROM students WHERE id = :student_id"),
            {"student_id": enrollment.student_id},
        ).first()

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        section = db.execute(
            text("""
                SELECT id, capacity
                FROM class_sections
                WHERE id = :section_id
                FOR UPDATE
            """),
            {"section_id": enrollment.class_section_id},
        ).first()

        if section is None:
            raise HTTPException(
                status_code=404,
                detail="Class section not found",
            )

        existing = db.execute(
            text("""
                SELECT 1
                FROM enrollments
                WHERE student_id = :student_id
                  AND class_section_id = :section_id
            """),
            {
                "student_id": enrollment.student_id,
                "section_id": enrollment.class_section_id,
            },
        ).first()

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Student already enrolled in this class section",
            )

        enrolled_count = db.execute(
            text("""
                SELECT COUNT(*)
                FROM enrollments
                WHERE class_section_id = :section_id
            """),
            {"section_id": enrollment.class_section_id},
        ).scalar_one()

        if enrolled_count >= section.capacity:
            raise HTTPException(
                status_code=409,
                detail="Class section is full",
            )

        result = db.execute(
            text("""
                INSERT INTO enrollments (
                    student_id,
                    class_section_id
                )
                VALUES (
                    :student_id,
                    :section_id
                )
                RETURNING student_id, class_section_id, registered_at
            """),
            {
                "student_id": enrollment.student_id,
                "section_id": enrollment.class_section_id,
            },
        ).mappings().one()

        db.commit()
        return dict(result)

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create enrollment",
        )

@app.delete(
    "/enrollments/{student_id}/{class_section_id}",
    status_code=204,
)
def delete_enrollment(
    student_id: str,
    class_section_id: str,
    db: Session = Depends(get_db),
):
    try:
        result = db.execute(
            text("""
                DELETE FROM enrollments
                WHERE student_id = :student_id
                  AND class_section_id = :section_id
                RETURNING student_id
            """),
            {
                "student_id": student_id,
                "section_id": class_section_id,
            },
        ).first()

        if result is None:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Enrollment not found",
            )

        db.commit()
        return Response(status_code=204)

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete enrollment",
        )