from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    credits: int


class SectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    course_code: str
    capacity: int
    enrolled_count: int
    remaining_slots: int

class SectionCapacityUpdate(BaseModel):
    capacity: int = Field(gt=0)

class EnrollmentCreate(BaseModel):
    student_id: str = Field(
        min_length=8,
        max_length=8,
        examples=["22000004"],
    )
    class_section_id: str = Field(
        min_length=1,
        max_length=20,
        examples=["WEB-01"],
    )


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: str
    class_section_id: str
    registered_at: datetime | None = None
