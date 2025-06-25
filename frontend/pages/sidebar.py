import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from .logout import logout_click


def sidebar_layout():
    """Creates the sidebar layout for the dashboard."""

    return html.Div(
        children=[
            # Dashboard title
            html.Div(
                [
                    dmc.Group(
                        [
                            dmc.Image(src="assets/icon.svg", w=30),
                            dmc.Title("AgroWise", c="white", order=2),
                        ],
                        grow=False,
                    ),
                    html.Hr(
                        style={
                            "borderColor": "white",
                        }
                    ),
                ],
                style={
                    "position": "absolute",
                    "top": "20px",
                    "left": "20px",
                    "width": "calc(100% - 40px)",
                },
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            # Menu links
            html.Div(
                [
                    # Database link
                    dmc.NavLink(
                        label="Crop Predict",
                        href="/predict",
                        leftSection=DashIconify(
                            icon="hugeicons:ai-brain-01",
                            width=20,
                        ),
                        variant="subtle",
                        color="white",
                        active="partial",
                    ),
                    # New Chat link
                    dmc.NavLink(
                        label="Visualize",
                        href="/visualize",
                        leftSection=DashIconify(
                            icon="oui:app-visualize",
                            width=20,
                        ),
                        variant="subtle",
                        color="white",
                        active="partial",
                    ),
                    html.Hr(
                        style={
                            "borderColor": "white",
                        }
                    ),
                ],
                style={
                    "margin-bottom": "20px",
                    "left": "0px",
                },
            ),
            # User Logout section
            html.Div(
                [
                    html.Hr(
                        style={
                            "borderColor": "white",
                            "width": "100%",
                        }
                    ),
                    html.Div(
                        id="auth_status",
                        children=logout_click(),
                        style={
                            "margin-bottom": "10px",
                        },
                    ),
                ],
                style={
                    "position": "absolute",
                    "bottom": "20px",
                    "left": "20px",
                    "width": "calc(100% - 40px)",
                },
            ),
        ],
        id="sidebar",
        style={
            "height": "100%",
            "width": "20rem",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "overflow-x": "hidden",
            "padding": "20px",
            "background-color": "#1c1919",
            "color": "white",
        },
    )
