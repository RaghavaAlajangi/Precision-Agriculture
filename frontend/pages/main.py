from dash import html

from .sidebar import sidebar_layout


def layout():
    return html.Div(
        [
            sidebar_layout(),
            html.Div(
                id="page_content",
                style={
                    "align-items": "center",
                    "overflowX": "hidden",
                    "margin-left": "25rem",
                },
            ),
        ]
    )
