from pathlib import Path

import dash_mantine_components as dmc
import numpy as np
from dash import Input, Output, State, callback, ctx, dcc, html, no_update

from ..inference import get_image, model_inference

ROOT = Path(__file__).parents[1]
CROP_IMG_PATH = ROOT / "data" / "crop_images"
DATA_PATH = ROOT / "data" / "crops.csv"
TRAINED_MODEL_PATH = ROOT / "ml_model" / "model.pkl"

input_boxes = {
    "nitrogen": "nitrogen content",
    "phosphorous": "phosphorous content",
    "potassium": "Potassium content",
    "temparature": "Temparature in °C",
    "humidity": "Humidity in %",
    "ph_value": "PH value (between 2-9)",
    "rainfall": "Rainfall in mm",
}

dmc_input_boxes = [
    dmc.TextInput(
        label=f"{name.capitalize()}:",
        placeholder=f"Enter the {name.capitalize()}",
        id=id_name,
        bd=10,
        required=True,
    )
    for id_name, name in input_boxes.items()
]


def layout():
    return html.Div(
        [
            dcc.Store(id="store_inputs"),
            dmc.Text(
                "Note:",
                size="xl",
                style={
                    "padding-top": "20px",
                },
            ),
            dmc.Text(
                "1. Precision agriculture is currently popular. "
                "It helps farmers to develop intelligent "
                "agricultural strategies.",
            ),
            dmc.Text(
                "2. Based on seven characteristics, this "
                "application will recommend the ideal crop "
                "for farmers to grow on their fileds.",
            ),
            html.Br(),
            dmc.SimpleGrid(
                [
                    html.Div(
                        [
                            dmc.Text(
                                "Soil test parameters:",
                                size="xl",
                                td="underline",
                            ),
                            dmc.Card(
                                children=[
                                    *dmc_input_boxes,
                                    html.Br(),
                                    dmc.Group(
                                        [
                                            dmc.Button(
                                                "Predict",
                                                id="predict_button",
                                                color="#494646",
                                            )
                                        ],
                                        justify="center",
                                    ),
                                ],
                                radius="md",
                                w="80%",
                                style={
                                    "border": "gray",
                                    "backgroundColor": "#222222",
                                },
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            dmc.Text(
                                "Prediction:",
                                size="xl",
                                td="underline",
                            ),
                            dmc.Card(
                                [
                                    dmc.Image(
                                        id="prediction_image",
                                        radius="md",
                                        h=400,
                                        w=400,
                                        fit="contain",
                                    ),
                                    html.Div(id="crop_name"),
                                ],
                                style={
                                    "border": "gray",
                                    "backgroundColor": "#222222",
                                },
                            ),
                        ],
                    ),
                ],
                cols=2,
                spacing="xs",
            ),
        ]
    )


@callback(
    Output("store_inputs", "data"),
    Input("nitrogen", "value"),
    Input("phosphorous", "value"),
    Input("potassium", "value"),
    Input("temparature", "value"),
    Input("humidity", "value"),
    Input("ph_value", "value"),
    Input("rainfall", "value"),
)
def store_inputs(
    nitrogen,
    phosphorous,
    potassium,
    temparature,
    humidity,
    ph_value,
    rainfall,
):
    feat_strings = [
        nitrogen,
        phosphorous,
        potassium,
        temparature,
        humidity,
        ph_value,
        rainfall,
    ]
    if (
        len(feat_strings) == 7
        and None not in feat_strings
        and "" not in feat_strings
    ):
        return feat_strings


@callback(
    Output("prediction_image", "src"),
    Output("crop_name", "children"),
    Input("predict_button", "n_clicks"),
    State("store_inputs", "data"),
)
def update_crop_name(
    predict_button,
    stored_inputs,
):
    if stored_inputs is not None:
        feat_floats = np.array([[float(feat) for feat in stored_inputs]])

        prediction = model_inference(feat_floats)
        fig = get_image(prediction)

        if ctx.triggered_id and "predict_button" == ctx.triggered_id:
            return fig, dmc.Text(
                [
                    f"Recommended crop:  {prediction.capitalize()}",
                    html.Br(),
                    f"Our ML model suggests '{prediction.capitalize()}' "
                    f"crop based on given parameters!",
                ],
                c="white",
            )

        else:
            return no_update
    else:
        return no_update


@callback(
    Output("nitrogen", "value"),
    Output("phosphorous", "value"),
    Output("potassium", "value"),
    Output("temparature", "value"),
    Output("humidity", "value"),
    Output("ph_value", "value"),
    Output("rainfall", "value"),
    Input("predict_button", "n_clicks"),
)
def reset_inputs(click):
    if ctx.triggered_id and "predict_button" == ctx.triggered_id:
        return [""] * 7
    return no_update
