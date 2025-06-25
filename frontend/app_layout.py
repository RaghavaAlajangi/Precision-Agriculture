import os

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# from dash import callback_context as ctx
from dash import (
    Dash,
    Input,
    Output,
    State,
    _dash_renderer,
    callback,
    dcc,
    html,
    no_update,
)
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager, UserMixin, current_user, login_user

from .credentials import VALID_USERNAME_PASSWORD
from .pages import login, logout, main, predict, visualize

load_dotenv()

# Exposing the Flask Server to enable configuring it for logging in
server = Flask(__name__)

_dash_renderer._set_react_version("18.2.0")

# Dash Bootstrap CSS URL
DBC_CSS = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap"
    "-templates@V1.0.1/dbc.min.css"
)

app = Dash(
    server=server,
    suppress_callback_exceptions=True,
    title="AgroWise",
    assets_folder="assets",
    external_stylesheets=[dbc.themes.DARKLY, DBC_CSS, dbc.icons.BOOTSTRAP],
)
app._favicon = "icon.svg"

SECRET_KEY = os.getenv("SECRET_KEY", "Test123456789")

server.config.update(SECRET_KEY=SECRET_KEY)

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/"


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the
    user from a user database. We won't be registering or looking up users
    in this example, since we'll just login using LDAP server. So we'll
    simply return a User object with the passed in username.
    """
    return User(username)


app.layout = dmc.MantineProvider(
    [
        dcc.Location(id="app_url", refresh=False),
        dcc.Location(id="main_url", refresh=False),
        html.Div(id="app_content"),
    ]
)


@callback(
    Output("auth_status", "children"),
    Input("app_url", "pathname"),
)
def update_auth_status(_):
    if current_user.is_authenticated:
        return no_update
    return dcc.Location(href="/", id="login_link")


@callback(
    Output("show_auth_status", "children"),
    Input("login_button", "n_clicks"),
    State("username_box", "value"),
    State("password_box", "value"),
    prevent_initial_call=True,
)
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        if VALID_USERNAME_PASSWORD.get(username) is None:
            return "Invalid Username"
        if VALID_USERNAME_PASSWORD.get(username) == password:
            login_user(User(username))
            return dcc.Location(href="/main", id="chatbot_link")
        return "Invalid Credentials"


@callback(
    Output("app_content", "children"),
    Input("app_url", "pathname"),
)
def display_app_pages(pathname):
    if pathname == "/":
        return login.layout()
    elif pathname == "/logout":
        return logout.layout()
    else:
        return main.layout()


@callback(
    Output("page_content", "children"),
    Input("main_url", "pathname"),
)
def navigate_main_content(pathname):
    if pathname == "/main":
        return main.layout()
    elif pathname == "/predict":
        return predict.layout()
    elif pathname == "/visualize":
        return visualize.layout()
    else:
        return main.layout()
