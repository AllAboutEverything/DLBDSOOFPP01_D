import reflex as rx
from app.components.dashboard import dashboard_component


def sidebar_link(text: str, href: str, icon: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5 mr-3"),
        rx.el.span(text),
        href=href,
        class_name="flex items-center px-3 py-2 text-gray-700 font-medium rounded-md hover:bg-gray-200 hover:text-gray-900 transition-colors",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("graduation-cap", class_name="h-8 w-8 text-blue-600"),
                rx.el.h1("Studium", class_name="ml-3 text-2xl font-bold text-gray-800"),
                class_name="flex items-center px-4",
            ),
            rx.el.nav(
                sidebar_link("Dashboard", "#", "layout-grid"),
                sidebar_link("My Courses", "#", "book-marked"),
                sidebar_link("Calendar", "#", "calendar"),
                sidebar_link("Settings", "#", "settings"),
                class_name="mt-8 space-y-2",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=MaxMustermann",
                    class_name="h-10 w-10 rounded-full",
                ),
                rx.el.div(
                    rx.el.p(
                        "Max Mustermann",
                        class_name="text-sm font-semibold text-gray-800",
                    ),
                    rx.el.p(
                        "max.mustermann@uni.de", class_name="text-xs text-gray-500"
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="p-4 border-t border-gray-200",
        ),
        class_name="flex flex-col w-64 border-r border-gray-200 bg-gray-50 h-screen sticky top-0",
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(sidebar(), dashboard_component(), class_name="flex"),
        class_name="bg-gray-100 font-['Inter'] min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="Study Dashboard")