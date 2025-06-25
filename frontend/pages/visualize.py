from pathlib import Path

import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html, no_update

ROOT = Path(__file__).parents[2]
DATA_PATH = ROOT / "data" / "crops.csv"


def crop_id_col(df):
    mapping = {c: i for i, c in enumerate(list(df["label"].unique()), 1)}
    df["crop_id"] = [mapping[c] for c in df["label"]]
    return df


def create_table(data_df):
    drop_table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(data_df.columns),
                    fill_color="paleturquoise",
                    align="left",
                ),
                cells=dict(
                    values=[data_df[col] for col in data_df.columns],
                    fill_color="lavender",
                    align="left",
                ),
            )
        ]
    )
    drop_table.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    return drop_table


def data_grouping(df):
    dummy = pd.DataFrame()
    dummy["Nitrogen"] = pd.cut(
        df["N"], [-1, 70, 170], labels=["N(0-70)", "N(70-140)"]
    )
    dummy["Phosphorous"] = pd.cut(
        df["P"], [-1, 80, 170], labels=["P(0-80)", "P(80-150)"]
    )
    dummy["Potassium"] = pd.cut(
        df["K"],
        [-1, 50, 100, 150, 220],
        labels=["K(0-50)", "K(50-100)", "K(100-150)", "K(150-210)"],
    )
    dummy["Temp(°C)"] = pd.cut(
        df["temperature"],
        [-1, 15, 30, 50],
        labels=["T(0-15°C)", "T(15-30°C)", "T(30-50°C)"],
    )
    dummy["Humidity(%)"] = pd.cut(
        df["humidity"],
        [-2, 30, 60, 110],
        labels=["H(0-30%)", "H(30-60%)", "H(60-100%)"],
    )
    dummy["PH"] = pd.cut(df["ph"], [0, 5, 12], labels=["ph(0-5)", "ph(5-10)"])
    dummy["Rainfall(mm)"] = pd.cut(
        df["rainfall"],
        [-1, 100, 200, 350],
        labels=["rain(0-100mm)", "rain(100-200mm)", "rain(200-30mm)"],
    )
    dummy["Crop_name"] = df["label"]
    dummy["Crop_id"] = df["crop_id"]
    return dummy


def create_graph(df):
    layout = go.Layout(
        margin={"l": 33, "r": 40, "t": 20, "b": 10},
    )
    fig = go.Figure(
        go.Parcats(
            dimensions=[
                {"label": col.capitalize(), "values": list(df[col])}
                for col in df.columns
                if col != "Crop_id"  # Exclude "Crop_id"
            ],
            labelfont={"size": 16, "family": "Times", "color": "yellow"},
            tickfont={"size": 16, "family": "Times", "color": "yellow"},
            hoveron="category",
            hoverinfo="count+probability",
            # line = go.parcats.Line(color='#00FA9A', shape= 'hspline'),
            line={"color": df.Crop_id},
        ),
        layout=layout,
    )

    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )
    return fig


def layout():
    return html.Div(
        [
            dmc.Text(
                "Data visualization:",
                size="xl",
                style={
                    "padding-top": "20px",
                },
            ),
            dcc.Dropdown(
                id="drop_down",
                options=[
                    {
                        "label": "Categorical graph",
                        "value": "graph",
                    },
                    {
                        "label": "Data table",
                        "value": "table",
                    },
                ],
                style={"height": 30, "width": 600},
                value="graph",
                clearable=False,
            ),
            html.Br(),
            html.Div(
                [
                    dcc.Graph(
                        id="data_visualization",
                        config={"displaylogo": False},
                        style={"height": 550, "width": 1200},
                        # animate=True,
                        # figure = create_graph(vis_df)
                    )
                ]
            ),
        ]
    )


@callback(
    Output("data_visualization", "figure"),
    Input("drop_down", "value"),
)
def dropdown_options(drop_value):
    data_df = pd.read_csv(DATA_PATH)
    table_fig = create_table(data_df)

    updated_df = crop_id_col(df=data_df)
    grouped_df = data_grouping(updated_df)
    graph_fig = create_graph(grouped_df)

    if drop_value == "table":
        return table_fig

    if drop_value == "graph":
        return graph_fig

    return no_update
