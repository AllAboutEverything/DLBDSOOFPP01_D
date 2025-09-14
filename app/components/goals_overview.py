import reflex as rx
from app.states.study_state import StudyState


def progress_bar(value: rx.Var[int], color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            style={"width": value.to_string() + "%"},
            class_name=f"h-2 rounded-full {color_class}",
        ),
        class_name="w-full bg-gray-200 rounded-full h-2",
    )


def goal_card(
    icon: str,
    title: str,
    description: rx.Var[str],
    progress: rx.Var[int],
    progress_color: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-gray-500"),
            class_name="p-3 bg-gray-100 rounded-full",
        ),
        rx.el.div(
            rx.el.h3(title, class_name="text-md font-semibold text-gray-800"),
            rx.el.p(description, class_name="text-sm text-gray-500"),
            class_name="mt-2",
        ),
        progress_bar(progress, progress_color),
        class_name="flex flex-col justify-between p-4 bg-white rounded-lg shadow-sm border border-gray-200 space-y-3 h-full",
    )


def goals_overview_component() -> rx.Component:
    gpa_progress = rx.cond(
        StudyState.average_grade == 0.0,
        0,
        (100 * (4.0 - StudyState.average_grade) / (4.0 - StudyState.target_gpa)).to(
            int
        ),
    )
    return rx.el.div(
        rx.el.h2("My Goals", class_name="text-xl font-semibold text-gray-900"),
        rx.el.div(
            goal_card(
                "graduation-cap",
                "Degree Completion",
                f"{StudyState.total_ects} / {StudyState.total_degree_ects} ECTS",
                StudyState.ects_progress_percent,
                "bg-blue-500",
            ),
            goal_card(
                "award",
                "Target GPA",
                f"Current: {StudyState.average_grade.to_string()} (Target: {StudyState.target_gpa.to_string()})",
                gpa_progress,
                "bg-purple-500",
            ),
            goal_card(
                "trending-up",
                "Study Pace",
                f"{StudyState.study_pace_percent}% of target pace",
                StudyState.study_pace_percent,
                "bg-green-500",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4",
        ),
        class_name="w-full",
    )