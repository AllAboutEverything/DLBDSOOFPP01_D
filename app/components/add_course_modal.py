import reflex as rx
from app.states.study_state import StudyState


def form_field(
    label: str, name: str, placeholder: str, type: str, required: bool = True
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            type=type,
            required=required,
            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500",
        ),
        class_name="col-span-1",
    )


def add_course_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Add New Course",
                            class_name="text-lg font-semibold text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-5 w-5"),
                            on_click=StudyState.toggle_add_modal,
                            type="button",
                            class_name="text-gray-400 hover:text-gray-600 focus:outline-none",
                        ),
                        class_name="flex justify-between items-center pb-4 border-b border-gray-200",
                    ),
                    rx.el.div(
                        form_field(
                            "Course Name", "name", "e.g., Introduction to AI", "text"
                        ),
                        form_field(
                            "Lecturer", "lecturer", "e.g., Prof. Turing", "text"
                        ),
                        form_field("Semester", "semester", "e.g., 3", "number"),
                        form_field("ECTS", "ects", "e.g., 6", "number"),
                        form_field(
                            "Grade",
                            "grade",
                            "e.g., 1.7 (leave empty if not graded)",
                            "number",
                            required=False,
                        ),
                        class_name="grid grid-cols-2 gap-6 py-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=StudyState.toggle_add_modal,
                            class_name="w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50",
                        ),
                        rx.el.button(
                            "Add Course",
                            type="submit",
                            class_name="w-full justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700",
                        ),
                        class_name="flex gap-4 pt-4 border-t border-gray-200",
                    ),
                    class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg",
                ),
                on_submit=StudyState.add_course,
                reset_on_submit=True,
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4",
        ),
        open=StudyState.show_add_modal,
    )