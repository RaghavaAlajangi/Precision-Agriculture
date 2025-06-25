import dash_mantine_components as dmc
from dash import html


def layout():
    return html.Div(
        children=[
            dmc.Container(
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "minHeight": "80vh",
                    "color": "gray",
                    "borderRadius": "8px",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
                },
                children=[
                    dmc.Fieldset(
                        children=[
                            dmc.Title(
                                "Login to RAGbot",
                                order=1,
                                c="#494646",
                                style={"textAlign": "center"},
                            ),
                            dmc.TextInput(
                                label="Username",
                                placeholder="Enter username",
                                id="username_box",
                            ),
                            dmc.PasswordInput(
                                label="Password",
                                placeholder="Enter password",
                                id="password_box",
                            ),
                            html.Br(),
                            dmc.Group(
                                [
                                    dmc.Button(
                                        "Login",
                                        id="login_button",
                                        color="#494646",
                                    )
                                ],
                                justify="center",
                            ),
                        ],
                        disabled=False,
                        variant="default",
                        radius="md",
                        w="40%",
                    ),
                ],
            ),
            html.Div(children="", id="show_auth_status"),
        ],
    )
