# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 17:01:33 2021

@author: ragha
"""

import os
import dash
import pickle
import base64
import numpy as np 
import pandas as pd
from PIL import Image
from dash import html
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

DATA_PATH = 'Crop_recommendation.csv'
TRAINED_MODEL_PATH = 'KNN_model_crop_prediction.pkl'
CROP_IMG_PATH = 'crops'
crop_img_files = [os.path.join(CROP_IMG_PATH, f) for f in os.listdir(CROP_IMG_PATH)]

def model_inference(feature_arr):
    with open(TRAINED_MODEL_PATH, 'rb') as pickle_file:
        model = pickle.load(pickle_file)
    pred = model.predict(feature_arr)
    return pred

def get_img_file(pred, crops_list = crop_img_files):
    crop_name = pred[0]
    img_file = [f for f in crops_list if crop_name in f][0]
    return img_file

    
def get_figure(img_path):
    encoded_image = base64.b64encode(open(img_path, 'rb').read())
    img_src = 'data:image/png;base64,{}'.format(encoded_image.decode())
    return img_src


# Initialise the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div(children=[
                  html.Div(className='row',  # Define the row element
                           children=[
                           html.Div(className='four columns div-user-controls',
                                    children = [
                                        html.P('Crop recommendation application', style = {'font-size': '35px'}),
                                        html.P('O Precision agriculture is currently popular. It helps farmers to develop intelligent agricultural strategies.', style = {'font-size': '20px'}),
                                        html.P('O Based on seven characteristics, this application will recommend the ideal crop for farmers to grow on their farms.', style = {'font-size': '20px'}),
                                        html.Br(),
                                        html.Br(),
                                        html.Div(
                                              dcc.Input(id="N",
                                                        placeholder='Enter Nitrogen content in soil...',
                                                        type='text',
                                                        persistence = True,
                                                        style={'width': '300px'}
                                                       )),
                                        html.Br(),
                                        html.Div(
                                              dcc.Input(id="P",
                                                        placeholder='Enter Phosphorous content in soil...',
                                                        type='text',
                                                        persistence = True,
                                                        style={'width': '300px'}
                                                       )),
                                        html.Br(),
                                        html.Div(
                                              dcc.Input(id="K",
                                                        placeholder='Enter Potassium content in soil...',
                                                        type='text',
                                                        persistence = True,
                                                        style={'width': '300px'}
                                                       )),
                                        html.Br(),
                                        html.Div(
                                              dcc.Input(id="temp",
                                                        placeholder='Enter Temp in °C...',
                                                        type='text',
                                                        persistence = True,
                                                        style={'width': '300px'}
                                                       )),
                                        html.Br(),
                                        html.Div(
                                              dcc.Input(id="hum",
                                                        placeholder='Enter Humidity in %...',
                                                        type='text',
                                                        persistence = True,
                                                        style={'width': '300px'}
                                                       )),
                                        html.Br(),
                                        html.Div(
                                              dcc.Input(id="ph",
                                                        placeholder='Enter PH value of the soil...',
                                                        type='text',
                                                        persistence = True,
                                                        style={'width': '300px'}
                                                       )),
                                        html.Br(),
                                        html.Div(
                                              dcc.Input(id="rain",
                                                        placeholder='Enter rainfall in mm...',
                                                        type='text',
                                                        persistence = True,
                                                        style={'width': '300px'}
                                                       )),
                                        html.Br(),
                                        html.Button('Submit', id='submit_button', n_clicks=0, disabled=False),
                                  ]),  # four column Div
                                   
                           html.Div(className='eight columns div-for-charts bg-grey',  # Define the right element
                                    style={'background-image':'url("/assets/agriculture1.png")','height':150,'width':1000},
                                    children = [
                                    html.H2('Precision-Agriculture', style = {'text-align':'center', "padding-top": "10px", 
                                                                    'font-size': '35px', 'color': 'red'}),
                                        
                                    html.Div([
                                        
                                        html.Div([ 
                                            html.H2('Crop picture!', style = {"padding-top": "200px", 'font-size': '25px'}),
                                            
                                            html.Img(id = "prediction_image", style = {'width':500})
                                            
                                        ], className="six columns"),
                                        
                                        html.Div(id='crop_name', className="six columns"),
                                    ], className="row"),
                                        
                                        
                                   ]),  # eight column Div
                               
                          ]) # row Div
                    ]) # main Div

@app.callback([Output("prediction_image", "src"),
               Output('crop_name', 'children')], 
              [Input('submit_button', 'n_clicks'),
               Input('N', 'value'),
               Input("P", "value"),
               Input("K", "value"),
               Input("temp", "value"),
               Input("hum", "value"),
               Input("ph", "value"),
               Input("rain", "value")])

def update_crop_name(click, N, P, K, temp, hum, ph, rain):
    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
    features_str = [N, P, K, temp, hum, ph, rain]
    if len(features_str) == 7 and None not in features_str and '' not in features_str:
        features = [float(s) for s in features_str]
        pred = model_inference(np.array([features]))
        pred_crop_name = pred[0]
        pred_img_file = get_img_file(pred)
        fig = get_figure(pred_img_file)

        if 'submit_button' in trigger:
            return [fig,
                    html.P([f'Recommended crop:  {pred_crop_name.capitalize()}',
                             html.Br(), 
                             'With given elements:',
                             html.Br(), 
                             f'Nitrogen content in soil.......... {N}',
                             html.Br(), 
                             f'Phosphorous content in soil.... {P}',
                             html.Br(), 
                             f'Potassium content in soil........ {K}',
                             html.Br(), 
                             f'Temperature in degree °C....... {temp}',
                             html.Br(), 
                             f'Humidity in %........................ {hum}',
                             html.Br(), 
                             f'PH value of the soil................ {ph}',
                             html.Br(), 
                             f'Rainfall in mm....................... {rain}',
                            ], 
                            style = {"padding-top": "220px", 
                                     "padding-left": "80px",
                                     'display': 'list',
                                     'font-size': '25px',}),
                     ] 
        else:
            return dash.no_update
    else:
        return dash.no_update

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=4000)  