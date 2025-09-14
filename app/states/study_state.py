import reflex as rx
from typing import TypedDict, Literal

CourseStatus = Literal["Passed", "In Progress", "Failed"]


class Course(TypedDict):
    id: int
    name: str
    semester: int
    lecturer: str
    ects: int
    grade: float | None
    status: CourseStatus


class StudyState(rx.State):
    courses: list[Course] = [
        {
            "id": 1,
            "name": "Object-Oriented Programming",
            "semester": 2,
            "lecturer": "Dr. Python",
            "ects": 6,
            "grade": 1.3,
            "status": "Passed",
        },
        {
            "id": 2,
            "name": "Web Development with Reflex",
            "semester": 3,
            "lecturer": "Prof. UI",
            "ects": 9,
            "grade": 1.0,
            "status": "Passed",
        },
        {
            "id": 3,
            "name": "Database Systems",
            "semester": 3,
            "lecturer": "Dr. SQL",
            "ects": 6,
            "grade": None,
            "status": "In Progress",
        },
        {
            "id": 4,
            "name": "Algorithms & Data Structures",
            "semester": 2,
            "lecturer": "Prof. Logic",
            "ects": 9,
            "grade": 2.7,
            "status": "Passed",
        },
        {
            "id": 5,
            "name": "Linear Algebra",
            "semester": 1,
            "lecturer": "Dr. Matrix",
            "ects": 6,
            "grade": 4.0,
            "status": "Failed",
        },
        {
            "id": 6,
            "name": "Software Engineering",
            "semester": 4,
            "lecturer": "Prof. Agile",
            "ects": 6,
            "grade": None,
            "status": "In Progress",
        },
    ]
    show_add_modal: bool = False
    filter_status: str = "All"
    search_query: str = ""
    target_gpa: float = 2.0
    target_duration_semesters: int = 6
    total_degree_ects: int = 180

    @rx.var
    def total_ects(self) -> int:
        return sum(
            (course["ects"] for course in self.courses if course["status"] == "Passed")
        )

    @rx.var
    def completed_courses(self) -> int:
        return sum((1 for course in self.courses if course["status"] == "Passed"))

    @rx.var
    def average_grade(self) -> float:
        passed_courses = [
            course
            for course in self.courses
            if course["status"] == "Passed" and course["grade"] is not None
        ]
        if not passed_courses:
            return 0.0
        total_grade_points = sum((c["grade"] * c["ects"] for c in passed_courses))
        total_ects_points = sum((c["ects"] for c in passed_courses))
        return (
            round(total_grade_points / total_ects_points, 2)
            if total_ects_points > 0
            else 0.0
        )

    @rx.var
    def ects_progress_percent(self) -> int:
        if self.total_degree_ects == 0:
            return 0
        return int(self.total_ects / self.total_degree_ects * 100)

    @rx.var
    def study_pace_percent(self) -> int:
        if not self.courses or self.target_duration_semesters == 0:
            return 0
        highest_semester = max((course["semester"] for course in self.courses))
        ects_per_semester_target = (
            self.total_degree_ects / self.target_duration_semesters
        )
        target_ects_for_current_progress = highest_semester * ects_per_semester_target
        if target_ects_for_current_progress == 0:
            return 100
        return int(self.total_ects / target_ects_for_current_progress * 100)

    @rx.var
    def filtered_courses(self) -> list[Course]:
        def check_status(course: Course) -> bool:
            return self.filter_status == "All" or course["status"] == self.filter_status

        def check_search(course: Course) -> bool:
            return (
                self.search_query.lower() in course["name"].lower()
                or self.search_query.lower() in course["lecturer"].lower()
            )

        return [
            course
            for course in self.courses
            if check_status(course) and check_search(course)
        ]

    @rx.event
    def toggle_add_modal(self):
        self.show_add_modal = not self.show_add_modal

    @rx.event
    def add_course(self, form_data: dict):
        grade = float(form_data["grade"]) if form_data["grade"] else None
        status: CourseStatus = "In Progress"
        if grade:
            status = "Passed" if grade <= 4.0 else "Failed"
        new_course: Course = {
            "id": len(self.courses) + 1,
            "name": form_data["name"],
            "semester": int(form_data["semester"]),
            "lecturer": form_data["lecturer"],
            "ects": int(form_data["ects"]),
            "grade": grade,
            "status": status,
        }
        self.courses.append(new_course)
        self.show_add_modal = False

    @rx.event
    def delete_course(self, course_id: int):
        self.courses = [c for c in self.courses if c["id"] != course_id]