import reflex as rx
from app.states.study_state import StudyState, Course
from app.components.add_course_modal import add_course_modal
from app.components.goals_overview import goals_overview_component


def stat_card(icon_name: str, title: str, value: rx.Var, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name="h-6 w-6"),
            class_name=f"p-3 rounded-full bg-{color}-100 text-{color}-600",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-semibold text-gray-900"),
            class_name="ml-4",
        ),
        class_name="flex items-center p-4 bg-white rounded-lg shadow-sm border border-gray-200",
    )


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Passed",
                "px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800 w-fit",
            ),
            (
                "In Progress",
                "px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800 w-fit",
            ),
            (
                "Failed",
                "px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800 w-fit",
            ),
            "px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800 w-fit",
        ),
    )


def course_table_row(course: Course) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            course["name"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            course["lecturer"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            course["semester"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center",
        ),
        rx.el.td(
            course["ects"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center",
        ),
        rx.el.td(
            rx.cond(course["grade"], course["grade"].to_string(), "-"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center",
        ),
        rx.el.td(
            status_badge(course["status"]),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: StudyState.delete_course(course["id"]),
                class_name="text-gray-400 hover:text-red-600 transition-colors",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors",
    )


def dashboard_component() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Study Dashboard", class_name="text-3xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Welcome back, here's your academic progress.",
                    class_name="mt-1 text-gray-500",
                ),
            ),
            stat_card("book-open", "Total ECTS", StudyState.total_ects, "blue"),
            stat_card(
                "check_check",
                "Courses Completed",
                StudyState.completed_courses,
                "green",
            ),
            stat_card(
                "award", "Average Grade", StudyState.average_grade.to_string(), "purple"
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        goals_overview_component(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "My Courses", class_name="text-xl font-semibold text-gray-900"
                    ),
                    rx.el.p(
                        "Manage and track all your university courses.",
                        class_name="text-sm text-gray-500",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search courses...",
                            on_change=StudyState.set_search_query,
                            class_name="w-full md:w-64 pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-blue-500 focus:border-blue-500",
                        ),
                        class_name="relative",
                    ),
                    rx.el.select(
                        rx.foreach(
                            ["All", "Passed", "In Progress", "Failed"],
                            lambda s: rx.el.option(s, value=s),
                        ),
                        on_change=StudyState.set_filter_status,
                        value=StudyState.filter_status,
                        class_name="w-full md:w-40 border-gray-300 rounded-lg shadow-sm text-sm focus:ring-blue-500 focus:border-blue-500",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="h-4 w-4 mr-2"),
                        "Add Course",
                        on_click=StudyState.toggle_add_modal,
                        class_name="flex items-center justify-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                    ),
                    class_name="flex flex-col md:flex-row items-center gap-4",
                ),
                class_name="flex flex-col md:flex-row justify-between items-start md:items-center gap-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Course",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Lecturer",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Semester",
                                    scope="col",
                                    class_name="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "ECTS",
                                    scope="col",
                                    class_name="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Grade",
                                    scope="col",
                                    class_name="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    scope="col",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    rx.el.span("Actions", class_name="sr-only"),
                                    scope="col",
                                    class_name="relative px-6 py-3",
                                ),
                            ),
                            class_name="bg-gray-50",
                        ),
                        rx.el.tbody(
                            rx.foreach(StudyState.filtered_courses, course_table_row),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                    ),
                    class_name="overflow-x-auto",
                ),
                rx.cond(
                    StudyState.filtered_courses.length() == 0,
                    rx.el.div(
                        rx.icon("search-x", class_name="h-12 w-12 text-gray-400"),
                        rx.el.p(
                            "No Courses Found",
                            class_name="mt-4 text-lg font-semibold text-gray-700",
                        ),
                        rx.el.p(
                            "Try adjusting your search or filter.",
                            class_name="mt-1 text-sm text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center text-center p-16 bg-gray-50 rounded-lg",
                    ),
                    rx.fragment(),
                ),
                class_name="align-middle inline-block min-w-full mt-6 shadow-sm border border-gray-200 rounded-lg overflow-hidden",
            ),
        ),
        add_course_modal(),
        class_name="flex-1 p-8 space-y-8",
    )