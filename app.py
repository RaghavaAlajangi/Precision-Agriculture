# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 17:01:33 2021

@author: raghava
"""
import os
import dash
import pickle
import base64
import numpy as np 
import pandas as pd
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

CROP_IMG_PATH = 'crops'
DATA_PATH = 'Crop_recommendation.csv'
TRAINED_MODEL_PATH = 'KNN_model_crop_prediction.pkl'

crop_img_files = [os.path.join(CROP_IMG_PATH, f) for f in os.listdir(CROP_IMG_PATH)]

def crop_id_col(df = None):
    mapping = {c : i for i, c in enumerate(list(df['label'].unique()), 1)}
    df['crop_id'] = [mapping[c] for c in df['label']]
    return df

# def get_sample_data(df = None, col_name = None, No_of_samples = 20):
#     mapping = {c : i for i, c in enumerate(list(df['label'].unique()), 1)}
#     frames = []
#     for k, v in mapping.items():
#         samp = df.loc[(df[col_name] ==v)].iloc[:No_of_samples]
#         frames.append(samp)
#     return pd.concat(frames)

def data_grouping(df):
    dummy = pd.DataFrame()
    dummy['Nitrogen'] = pd.cut(df["N"], [-1, 70, 170], labels = ['N(0-70)', 'N(70-140)'])
    dummy['Phosphorous'] = pd.cut(df["P"], [-1, 80, 170], labels = ['P(0-80)', 'P(80-150)'])
    dummy['Potassium'] = pd.cut(df["K"], [-1, 50, 100, 150, 220], labels = ['K(0-50)', 'K(50-100)', 'K(100-150)', 'K(150-210)'])
    dummy['Temp(°C)'] = pd.cut(df["temperature"], [-1, 15, 30, 50], labels = ['T(0-15°C)', 'T(15-30°C)', 'T(30-50°C)'])
    dummy['Humidity(%)'] = pd.cut(df["humidity"], [-2, 30, 60, 110], labels = ['H(0-30%)', 'H(30-60%)', 'H(60-100%)'])
    dummy['PH'] = pd.cut(df["ph"], [0, 5, 12], labels = ['ph(0-5)', 'ph(5-10)'])
    dummy['Rainfall(mm)'] = pd.cut(df["rainfall"], [-1, 100, 200, 350], labels = ['rain(0-100mm)', 'rain(100-200mm)', 'rain(200-30mm)'])
    dummy['Crop_name'] = df['label']
    dummy['Crop_id'] = df['crop_id']
    return dummy

def model_inference(feature_arr):
    with open(TRAINED_MODEL_PATH, 'rb') as pickle_file:
        model = pickle.load(pickle_file)
    pred = model.predict(feature_arr)
    return pred

def get_img_file(pred, crops_list = crop_img_files):
    crop_name = pred[0]
    img_file = [f for f in crops_list if crop_name in f][0]
    return img_file
    
def get_image(img_path):
    encoded_image = base64.b64encode(open(img_path, 'rb').read())
    img_src = 'data:image/png;base64,{}'.format(encoded_image.decode())
    return img_src

def table_fig(data_df):
        drop_table = go.Figure(
                data=[go.Table(
                header=dict(values=list(data_df.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[data_df.N, data_df.P, data_df.K, data_df.temperature, 
                                   data_df.humidity, data_df.ph, data_df.rainfall, data_df.label],
                           fill_color='lavender',
                           align='left'))
                    ])
        drop_table.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                  'paper_bgcolor': 'rgba(0, 0, 0, 0)'
                                })
        return drop_table

def build_fig(df):
    layout = go.Layout(
        margin={'l': 33, 'r': 40, 't': 20, 'b': 10},
        )
    fig = go.Figure(
        go.Parcats(
            dimensions=[
                {'label': 'Nitrogen',
                 'values': list(df['Nitrogen'])},
                {'label': 'Phosphorous',
                 'values': list(df['Phosphorous'])},
                {'label': 'Potassium',
                 'values': list(df['Potassium'])},
                {'label': 'Temperature',
                 'values': list(df['Temp(°C)'])},
                {'label': 'Humidity',
                 'values': list(df['Humidity(%)'])},
                {'label': 'PH',
                 'values': list(df['PH'])},
                {'label': 'Rainfall',
                 'values': list(df['Rainfall(mm)'])},
                {'label': 'Crop_name',
                 'values': list(df['Crop_name'])},
                    ],
             labelfont={'size': 16, 'family': 'Times', 'color':'yellow'},
             tickfont={'size': 16, 'family': 'Times', 'color':'yellow'},
             hoveron = 'category',
             hoverinfo = 'count+probability',
             # line = go.parcats.Line(color='#00FA9A', shape= 'hspline'),
             line={'color': df.Crop_id}
                ),
        layout=layout)
    
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
                     })
    return fig


# data_df = pd.read_csv(DATA_PATH)
# mod_df = crop_id_col(df = data_df)
# vis_df = data_grouping(mod_df)

# Initialise the app
app = dash.Dash(__name__)

server = app.server

# Define the app
app.layout = html.Div(children=[
                  html.Div(className='row',  # Define the row element
                           children=[
                           html.Div(className='four columns div-user-controls',
                                    children = [
                                        html.P('Crop recommendation application', style = {'font-size': '35px'}),
                                        html.H2('1. Precision agriculture is currently popular. It helps farmers to develop intelligent agricultural strategies.', style = {'font-size': '20px'}),
                                        html.H2('2. Based on seven characteristics, this application will recommend the ideal crop for farmers to grow on their fileds.', style = {'font-size': '20px'}),
                                        html.Br(),
                                        html.Div([
                                              html.H2('Nitrogen content in soil:', style = {'font-size': '15px'}),

                                              dcc.Input(id="N",
                                                        placeholder='Enter Nitrogen content in soil...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '400px'}
                                                       )]),
                                        html.Div([
                                              html.H2('Phosphorous content in soil:', style = {'font-size': '15px'}),
                                              dcc.Input(id="P",
                                                        placeholder='Enter Phosphorous content in soil...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '400px'}
                                                       )]),
                                        html.Div([
                                              html.H2('Potassium content in soil:', style = {'font-size': '15px'}),
                                              dcc.Input(id="K",
                                                        placeholder='Enter Potassium content in soil...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '400px'}
                                                       )]),
                                        html.Div([
                                              html.H2('Temparature in °C:', style = {'font-size': '15px'}),
                                              dcc.Input(id="temp",
                                                        placeholder='Enter Temp in °C...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '400px'}
                                                       )]),
                                        html.Div([
                                              html.H2('Humidity in %:', style = {'font-size': '15px'}),
                                              dcc.Input(id="hum",
                                                        placeholder='Enter Humidity in %...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '400px'}
                                                       )]),
                                        html.Div([
                                              html.H2('PH value of the soil (between 2-9):', style = {'font-size': '15px'}),
                                              dcc.Input(id="ph",
                                                        placeholder='Enter PH value of the soil...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '400px'}
                                                       )]),
                                        html.Div([
                                              html.H2('Rainfall in mm:', style = {'font-size': '15px'}),
                                              dcc.Input(id="rain",
                                                        placeholder='Enter rainfall in mm...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '400px'}
                                                       )]),
                                        html.Br(), html.Br(), 
                                        dcc.Store(id = 'store_inputs'),
                                        html.Button('Submit', id='submit_button', n_clicks=0, disabled=False, 
                                                    style = {'font-size': '15px',
                                                              'cursor': 'pointer',
                                                              'text-align': 'center',
                                                              'color': 'white',
                                                            }
                                                    ),
                                        
                                  ]),  # four column Div
                                   
                           html.Div(className='eight columns div-for-charts bg-grey',  # Define the right element
                                    style={'background-image':'url("/assets/agriculture.png")','height':150,'width':1300},
                                    children = [
                                    html.H2('Precision Agriculture', style = {'text-align':'center', "padding-top": "10px", 
                                                                    'font-size': '35px', 'color': 'red'}),
                                     
                                    html.H2('Data visualization:', style = {"padding-top": "80px", 
                                                                "padding-left": "0",'font-size': '25px'
                                                                }),
                                    
                                    html.Div([
                                        dcc.Dropdown(
                                                   id="drop_down",
                                                   options=[
                                                       {'label': 'Categorical graph', 'value': 'graph'},
                                                       {'label': 'Data table', 'value': 'table'},
                                                   ],
                                                   style={'height':30, 'width':600},
                                                   value='graph',
                                                   clearable=False)
                                            ]),
                                    html.Br(),
                                    html.Div([
                                    dcc.Graph(id='data_visualization',
                                              config={'displaylogo': False},
                                              style={'height':550,'width':1200},
                                              #animate=True,
                                              #figure = build_fig(vis_df)
                                              )
                                            ]),
                                    
                                    html.Div([
                                        html.Div([ 
                                            html.H2('Prediction will be displayed here:', style = {"padding-top": "0px", 'font-size': '25px'}),
                                            
                                            html.Img(id = "prediction_image")
                                            
                                        ], className="six columns"),
                                        
                                        html.Div(id='crop_name', className="six columns"),
                                    ], className="row"),
                                        
                                   ]),  # eight column Div
                           html.Br(),html.Br(),html.Br()
                               
                          ]) # row Div
                    ]) # main Div


@app.callback(Output("data_visualization", "figure"),
              Input('drop_down', 'value'),
              )
def dropdown_options(drop_value):
    data_df = pd.read_csv(DATA_PATH)
    fig_table = table_fig(data_df)
    
    mod_df = crop_id_col(df = data_df)
    vis_df = data_grouping(mod_df)
    fig_graph = build_fig(vis_df)
    
    if drop_value == 'table':
        return fig_table
    
    if drop_value == 'graph':
        return fig_graph
    
    else:
        dash.no_update

@app.callback(Output("store_inputs", "data"),
              [Input('N', 'value'),
               Input("P", "value"),
               Input("K", "value"),
               Input("temp", "value"),
               Input("hum", "value"),
               Input("ph", "value"),
               Input("rain", "value")])

def store_inputs(N, P, K, temp, hum, ph, rain):
    features_str = [N, P, K, temp, hum, ph, rain]
    if len(features_str) == 7 and None not in features_str and '' not in features_str:
        return {'N':N, 'P':P, 'K': K, 'temp':temp, 'hum':hum, 'ph':ph, 'rain':rain}

@app.callback([Output("prediction_image", "src"),
               Output('crop_name', 'children')], 
               Input('submit_button', 'n_clicks'),
               State('store_inputs', 'data'))

def update_crop_name(click, stored_inputs):
    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if stored_inputs is not None:
        N = float(stored_inputs['N'])
        P =float(stored_inputs['P'])
        K =float(stored_inputs['K'])
        temp =float(stored_inputs['temp'])
        hum =float(stored_inputs['hum'])
        ph =float(stored_inputs['ph'])
        rain =float(stored_inputs['rain'])
        
        pred = model_inference(np.array([[N, P, K, temp, hum, ph, rain]]))
        pred_crop_name = pred[0]
        pred_img_file = get_img_file(pred)
        fig = get_image(pred_img_file)
        if 'submit_button' in trigger:
            return [fig,
                    html.P([f'Recommended crop:  {pred_crop_name.capitalize()}',
                            html.Br(),
                            'Our Al-based decision-making system is suggesting ', 
                            f'{pred_crop_name.capitalize()}', 
                            ' depending on the parameters entered.'
                            ], 
                            style = {"padding-top": "20px", 
                                     'display': 'list',
                                     'font-size': '25px',}),
                     ] 
        else:
            return dash.no_update
    else:
            return dash.no_update
    
    
@app.callback([Output('N', 'value'),
               Output("P", "value"),
               Output("K", "value"),
               Output("temp", "value"),
               Output("hum", "value"),
               Output("ph", "value"),
               Output("rain", "value")], 
               Input('submit_button', 'n_clicks'))

def reset_inputs(click):
    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit_button' in trigger:
        return ['']*7
    else:
        return dash.no_update

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)  
 
