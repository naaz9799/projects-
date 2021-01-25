# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 12:50:01 2021

@author: USER
"""

import pickle
import pandas as pd
import webbrowser
# !pip install dash
import dash
import dash_html_components as html
import dash_core_components as dcc

import plotly.express as px

from dash.dependencies import Input, Output ,State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

app = dash.Dash()
project_name = None

def load_model():
    global df
    df = pd.read_csv('balanced_reviews.csv')
 
    global pickle_model
    file = open("pickle_model.pkl", 'rb')
    pickle_model = pickle.load(file)

    global vocab
    file = open("feature.pkl", 'rb')
    vocab = pickle.load(file)
   
    print(df.sample(5))

def open_browser():
    # Open the default web browser
    webbrowser.open_new('http://127.0.0.1:8050/')
   
def check_review(reviewText):

    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))


    # Add code to test the sentiment of using both the model
    #[0] == negative   [1] == positive
    return pickle_model.predict(reviewText)

def create_app_ui():
   
    global dfff
    dfff = pd.read_csv('reviews_etsy.csv')
   
   
   
    # Create the UI of the Webpage here
    main_layout = html.Div(
    [
    html.H1(children='Sentiments Analysis with Insights',style ={
    "color":"black","font-family": "Andalus",
    "text-align": "center","width":"100%"
}, id='Main_title'),
            # style={'textAlign': 'center','color':'springgreen'}),
   
    #piechart section
   
    html.H1(children='Pie Chart', id='Main_title2',
            style={'textAlign': 'left','color':'grey'}),
   
    html.Label("Pie Chart of Reviews"),
   
    dcc.Dropdown(id='chart',
                options=[
                   {'label':'Review','value':'overall'}],
                 value='overall',
                 multi=False,
                 clearable=False,
                style={'width':"50%"}
                 ),
     html.Button(children='Review Status', id='button_click', n_clicks=0,
                style={'color':'blue'}),
    dcc.Graph(id='piechart'),
   
   
    html.H1(children=None, id='result', style={'textAlign': 'center','color':'Violet'}),
    #review_check section
   
    html.H1(children='Review Check Section', id='Main_title3',
            style={'textAlign': 'Left','color':'Brown'}),
   
   
    #dropdown
  
    #dcc.Dropdown(
        #id='drop_down',
        #options = [
           # {'label': i,'value': i}for i in dfff['Reviews_df'].sample(30)
           # ],
        #optionHeight =100,
        #searchable = True,
        #),
   
  
   
    #text_review
   
    dcc.Textarea(
        id='textarea_review',
        placeholder='Enter the review here...',
        style={'width': '100%', 'height': 100, 'background':'cherrypink'},
        ),
   
    html.Button(children='Review Status', id='button_click1', n_clicks=0,
                style={'color':'blue'}),
   
    html.H1(children=None, id='result1', style={'textAlign': 'center','color':'mediumturquoise'}),
   
   
   
    ]
    )
   
    return main_layout

@app.callback(
    Output("piechart", "figure"),
    [Input("chart", "value")
     ])
def generate_chart(chart):
    dff=df
   
    fig = px.pie(
        data_frame=dff,
        names=chart)
    return fig


#text_area

@app.callback(
    Output('result1', 'children'),
    [
    Input('button_click1', 'n_clicks')
    ],
    [
    State('textarea_review', 'value')
    ]
    )
def update_app_ui(n_clicks,textarea_value):
   
    print("Data Type  = ", str(type(textarea_value)))
    print("Value      = ", str(textarea_value))

   
    result_list = check_review(textarea_value)
   
    if (result_list[0] == 0 ):
        result = 'Negative'
    elif (result_list[0] == 1 ):
        result = 'Positive'
    else:
        result = 'Unknown'
   
    return result

#for_drop_down

@app.callback(
    Output('result', 'children'),
    [
    Input('button_click', 'n_clicks'),
    ],
    [
    State('drop_down', 'value') ,
    ]
    )
def update_app_ui_drop(n_clicks,drop_down):
   
    print("Data Type  = ", str(type(drop_down)))
    print("Value      = ", str(drop_down))

   
    result_list = check_review(drop_down)
   
    if (result_list[0] == 0 ):
        result = 'Negative'
    elif (result_list[0] == 1 ):
        result = 'Positive'
    else:
        result = 'Unknown'
   
    return result

def main():
    load_model()   
    open_browser()
   

    global project_name
    project_name = "Sentiments Analysis with Insights"
     
    global app
    app.layout = create_app_ui()
    app.title = project_name
   
    app.run_server() # debug=True
 
    print("This would be executed only after the script is closed")
    app = None
    project_name = None

if __name__ == '__main__':
    main()
