# ============================================================
# COURSEHUB - BUOI 1
# Co so du lieu Web va he thong thong tin
# On tap Python: list, dictionary, dieu kien, vong lap,
# ham, try/except va mo phong quy tac nghiep vu.
# ============================================================


# ============================================================
# 1. DU LIEU MO PHONG
# ============================================================

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


# ============================================================
# 2. TIM KIEM SINH VIEN
# ============================================================

def find_student(student_id):
    """Tim sinh vien theo ma sinh vien."""
    for student in students:
        if student["id"] == student_id:
            return student

    return None


# ============================================================
# 3. TIM KIEM HOC PHAN
# ============================================================

def find_course(course_code):
    """Tim hoc phan theo ma hoc phan."""
    for course in courses:
        if course["code"] == course_code:
            return course

    return None


# ============================================================
# 4. KIEM TRA SINH VIEN DA DANG KY HOC PHAN
# ============================================================

def is_enrolled(student_id, course_code):
    """Kiem tra sinh vien da dang ky hoc phan hay chua."""
    for enrollment in enrollments:
        if (
            enrollment["student_id"] == student_id
            and enrollment["course_code"] == course_code
        ):
            return True

    return False


# ============================================================
# 5. KIEM TRA DIEU KIEN DANG KY
# ============================================================

def can_enroll(student_id, course_code):
    """
    Kiem tra cac dieu kien co ban truoc khi dang ky hoc phan.

    Thu tu kiem tra:
    1. Sinh vien phai ton tai.
    2. Hoc phan phai ton tai.
    3. Sinh vien khong duoc dang ky trung.
    4. Lop phai con cho.
    """

    # Kiem tra sinh vien
    student = find_student(student_id)

    if student is None:
        return False, "Sinh vien khong ton tai"

    # Kiem tra hoc phan
    course = find_course(course_code)

    if course is None:
        return False, "Hoc phan khong ton tai"

    # Kiem tra dang ky trung
    if is_enrolled(student_id, course_code):
        return False, "Sinh vien da dang ky hoc phan nay"

    # Kiem tra suc chua
    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"

    return True, "Co the dang ky"


# ============================================================
# 6. DANG KY HOC PHAN
# ============================================================

def enroll_student(student_id, course_code):
    """
    Dang ky hoc phan neu tat ca dieu kien hop le.

    Neu thanh cong:
    - Them mot ban ghi vao enrollments.
    - Tang so luong enrolled cua hoc phan len 1.
    """

    allowed, message = can_enroll(student_id, course_code)

    if not allowed:
        return False, message

    course = find_course(course_code)

    enrollments.append(
        {
            "student_id": student_id,
            "course_code": course_code,
        }
    )

    course["enrolled"] += 1

    return True, "Dang ky thanh cong"


# ============================================================
# 7. TIM KIEM HOC PHAN THEO MA HOAC TEN
# ============================================================

def search_courses(keyword):
    """
    Tim hoc phan theo ma hoac ten.

    - Bo khoang trang thua o dau/cuoi keyword.
    - Khong phan biet chu hoa va chu thuong.
    - Tra ve danh sach hoc phan phu hop.
    """

    normalized = keyword.strip().lower()
    results = []

    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()

        if normalized in code or normalized in name:
            results.append(course)

    return results


# ============================================================
# 8. TINH SO CHO CON LAI
# ============================================================

def get_remaining_slots(course):
    """Tinh so cho con lai cua mot hoc phan."""
    return course["capacity"] - course["enrolled"]


# ============================================================
# 9. HIEN THI DANH SACH SINH VIEN
# ============================================================

def print_students():
    """Hien thi danh sach sinh vien dang co trong he thong."""
    print("--- Danh sach sinh vien ---")

    for student in students:
        print(
            f'{student["id"]} - '
            f'{student["name"]} - '
            f'{student["major"]}'
        )


# ============================================================
# 10. HIEN THI DANH SACH HOC PHAN
# ============================================================

def print_courses():
    """Hien thi danh sach hoc phan va so cho con lai."""
    print("--- Danh sach hoc phan ---")

    for course in courses:
        remaining = get_remaining_slots(course)

        print(
            f'{course["code"]} - '
            f'{course["name"]} - '
            f'suc chua: {course["capacity"]} - '
            f'da dang ky: {course["enrolled"]} - '
            f'con lai: {remaining}'
        )


# ============================================================
# 11. HIEN THI DANH SACH DANG KY
# ============================================================

def print_enrollments():
    """Hien thi danh sach cac ban ghi dang ky."""
    print("--- Danh sach dang ky ---")

    for enrollment in enrollments:
        print(
            f'Sinh vien {enrollment["student_id"]} -> '
            f'Hoc phan {enrollment["course_code"]}'
        )


# ============================================================
# 12. IN SO CHO CON LAI CUA TUNG HOC PHAN
# ============================================================

def print_course_summary():
    """Hien thi so cho con lai cua moi hoc phan."""
    print("--- So cho con lai ---")

    for course in courses:
        remaining = get_remaining_slots(course)

        print(
            f'{course["code"]} - con {remaining} cho'
        )


# ============================================================
# 13. HIEN THI KET QUA TIM KIEM
# ============================================================

def print_search_results(keyword):
    """Tim va hien thi cac hoc phan phu hop voi keyword."""
    results = search_courses(keyword)

    print(
        f'--- Ket qua tim kiem: "{keyword}" ---'
    )

    if not results:
        print("Khong tim thay hoc phan phu hop")
        return

    for course in results:
        print(
            f'{course["code"]} - {course["name"]}'
        )


# ============================================================
# 14. XU LY INPUT SO LUONG HOC PHAN
# ============================================================

def show_courses_by_limit():
    """
    Nhap so luong hoc phan muon hien thi.

    Neu input khong phai so nguyen, xu ly ValueError
    thay vi de chuong trinh dung dot ngot.
    """

    try:
        limit = int(
            input(
                "Nhap so luong hoc phan muon hien thi: "
            )
        )

        if limit < 0:
            print("So luong khong duoc la so am")
            return

        print(courses[:limit])

    except ValueError:
        print("So luong phai la so nguyen")


# ============================================================
# 15. KIEM THU 05 TINH HUONG DANG KY
# ============================================================

def run_enrollment_tests():
    """
    Chay 05 tinh huong kiem thu theo yeu cau bai thuc hanh.

    Test 1: Dang ky thanh cong.
    Test 2: Dang ky trung.
    Test 3: Lop da day.
    Test 4: Hoc phan khong ton tai.
    Test 5: Sinh vien khong ton tai.
    """

    # --------------------------------------------------------
    # TEST 1 - Dang ky thanh cong
    # --------------------------------------------------------
    print("--- TEST 1: Dang ky thanh cong ---")

    result = enroll_student(
        "22000002",
        "INT2204",
    )

    print(result)

    # --------------------------------------------------------
    # TEST 2 - Dang ky trung
    # --------------------------------------------------------
    print("\n--- TEST 2: Dang ky trung ---")

    result = enroll_student(
        "22000002",
        "INT2204",
    )

    print(result)

    # --------------------------------------------------------
    # TEST 3 - Lop da day
    # --------------------------------------------------------
    print("\n--- TEST 3: Lop da day ---")

    result = enroll_student(
        "22000002",
        "INT2205",
    )

    print(result)

    # --------------------------------------------------------
    # TEST 4 - Hoc phan khong ton tai
    # --------------------------------------------------------
    print("\n--- TEST 4: Hoc phan khong ton tai ---")

    result = enroll_student(
        "22000002",
        "INT9999",
    )

    print(result)

    # --------------------------------------------------------
    # TEST 5 - Sinh vien khong ton tai
    # --------------------------------------------------------
    print("\n--- TEST 5: Sinh vien khong ton tai ---")

    result = enroll_student(
        "99999999",
        "INT2204",
    )

    print(result)


# ============================================================
# 16. CHUONG TRINH CHINH
# ============================================================

def main():
    """Chay toan bo noi dung thuc hanh Buoi 1."""

    print("CourseHub - Buoi 1")
    print()

    # --------------------------------------------------------
    # Danh sach sinh vien
    # --------------------------------------------------------
    print_students()
    print()

    # --------------------------------------------------------
    # Danh sach hoc phan
    # --------------------------------------------------------
    print_courses()
    print()

    # --------------------------------------------------------
    # So cho con lai
    # --------------------------------------------------------
    print_course_summary()
    print()

    # --------------------------------------------------------
    # Tim hoc phan theo ma
    # --------------------------------------------------------
    print("--- Tim hoc phan ---")

    course = find_course("INT2204")
    print(course)
    print()

    # --------------------------------------------------------
    # Tim sinh vien theo ma
    # --------------------------------------------------------
    print("--- Tim sinh vien ---")

    student = find_student("22000002")
    print(student)
    print()

    # --------------------------------------------------------
    # Kiem tra can_enroll
    # --------------------------------------------------------
    print("--- Kiem tra can_enroll ---")

    print(
        can_enroll(
            "22000002",
            "INT2204",
        )
    )
    print()

    # --------------------------------------------------------
    # Xu ly input so luong hoc phan
    # --------------------------------------------------------
    show_courses_by_limit()
    print()

    # --------------------------------------------------------
    # Tim kiem hoc phan theo keyword
    # --------------------------------------------------------
    print("--- Tim kiem hoc phan ---")

    print(search_courses("web"))
    print()

    # --------------------------------------------------------
    # Hien thi them mot ket qua tim kiem
    # --------------------------------------------------------
    print_search_results("kHAI")
    print()

    # --------------------------------------------------------
    # Chay 5 test bat buoc
    # --------------------------------------------------------
    run_enrollment_tests()
    print()

    # --------------------------------------------------------
    # Hien thi trang thai sau khi test
    # --------------------------------------------------------
    print_enrollments()
    print()

    print_courses()


# ============================================================
# 17. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()