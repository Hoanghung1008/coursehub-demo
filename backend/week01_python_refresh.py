print("CourseHub - Buoi 1")


# =========================
# 1. DU LIEU COURSEHUB
# =========================

students = [
    {
        "id": "22000001",
        "name": "Nguyen Minh Anh",
        "major": "KHDL",
    },
    {
        "id": "22000002",
        "name": "Tran Duc Long",
        "major": "KHDL",
    },
]

courses = [
    {
        "code": "INT2204",
        "name": "Co so du lieu Web va he thong thong tin",
        "capacity": 3,
        "enrolled": 2,
    },
    {
        "code": "INT2205",
        "name": "Khai pha du lieu",
        "capacity": 2,
        "enrolled": 2,
    },
]

enrollments = [
    {
        "student_id": "22000001",
        "course_code": "INT2204",
    }
]


# =========================
# 2. DUYET DU LIEU
# =========================

print("\n--- So cho con lai ---")

for course in courses:
    remaining = course["capacity"] - course["enrolled"]
    print(course["code"], "- con", remaining, "cho")


# =========================
# 3. TIM HOC PHAN THEO MA
# =========================

def find_course(course_code):
    for course in courses:
        if course["code"] == course_code:
            return course

    return None


print("\n--- Tim hoc phan ---")
print(find_course("INT2204"))


# =========================
# 4. TIM SINH VIEN THEO MA
# =========================

def find_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return student

    return None


# =========================
# 5. KIEM TRA CO THE DANG KY
# =========================

def can_enroll(student_id, course_code):
    course = find_course(course_code)

    if course is None:
        return False, "Hoc phan khong ton tai"

    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"

    duplicated = any(
        item["student_id"] == student_id
        and item["course_code"] == course_code
        for item in enrollments
    )

    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"

    return True, "Co the dang ky"


print("\n--- Kiem tra can_enroll ---")
print(can_enroll("22000002", "INT2204"))


# =========================
# 6. XU LY INPUT SAI
# =========================

try:
    limit = int(input("\nNhap so luong hoc phan muon hien thi: "))
    print(courses[:limit])

except ValueError:
    print("So luong phai la so nguyen")


# =========================
# 7. TIM KIEM HOC PHAN
# =========================

def search_courses(keyword):
    normalized = keyword.strip().lower()

    results = []

    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()

        if normalized in code or normalized in name:
            results.append(course)

    return results


print("\n--- Tim kiem hoc phan ---")
print(search_courses("web"))


# =========================
# 8. BAI TAP: DANG KY HOC PHAN
# =========================

def enroll_student(student_id, course_code):
    student = find_student(student_id)

    if student is None:
        return False, "Sinh vien khong ton tai"

    course = find_course(course_code)

    if course is None:
        return False, "Hoc phan khong ton tai"

    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"

    duplicated = any(
        item["student_id"] == student_id
        and item["course_code"] == course_code
        for item in enrollments
    )

    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"

    enrollments.append(
        {
            "student_id": student_id,
            "course_code": course_code,
        }
    )

    course["enrolled"] += 1

    return True, "Dang ky thanh cong"


# =========================
# 9. 5 TINH HUONG KIEM THU
# =========================

print("\n--- TEST 1: Dang ky thanh cong ---")
print(enroll_student("22000002", "INT2204"))

print("\n--- TEST 2: Dang ky trung ---")
print(enroll_student("22000002", "INT2204"))

print("\n--- TEST 3: Lop da day ---")
print(enroll_student("22000001", "INT2205"))

print("\n--- TEST 4: Hoc phan khong ton tai ---")
print(enroll_student("22000001", "INT9999"))

print("\n--- TEST 5: Sinh vien khong ton tai ---")
print(enroll_student("99999999", "INT2204"))


# =========================
# 10. KIEM TRA DU LIEU SAU TEST
# =========================

print("\n--- Enrollments sau khi test ---")
print(enrollments)

print("\n--- Courses sau khi test ---")
print(courses)