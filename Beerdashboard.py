
"""
Created on Sun Apr 17 15:45:07 2022

@author: 14849
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import dash_table
import matplotlib.pyplot as plt

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

df = pd.read_csv("/Users/14849/Desktop/beer_profile_and_ratings.csv")
df.columns.values

fig1 = px.histogram(df, x = 'Style')
fig1.update_layout(title_text='Frequency of style', title_x=0.5)

fig2 = px.scatter(df, x = 'Review', y = 'ABV', hover_name= 'Beer Name', color = 'Style')
fig2.update_layout(title_text='Scatter plot for the ABV and review of each beer', title_x=0.5)

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app.layout = html.Div([
    html.H1('Beer Information Dashboard', 
            style={'fontSize' : 40, 'textAlign' : 'center', 'background-color': 'yellow', 'color' :'black', 'font-weight' : 'bold'}),
    html.P('MA705 Project | Harshmi Dharod',
          style={'fontSize' : 13, 'textAlign' : 'center', 'background-color': 'yellow', 'color' :'black'}),
   html.Div([
   html.H2('➤ Introduction:',
            style={'fontSize':20, 'textAlign':'left', 'color': 'black' }),
   html.P("This dashboard was created from a dataset obtained from Kaggel that contains the description and taste parameters of 3,186 beers from 932 breweries. "),
   html.P("The data set tells us the name of the beer, it's brewery, style, ABV - alcohol by volume, minimum and maximum IBU - International Bitterness Unit, tastes like bitter, sweet, sour, salty, fruits, spices, malty and an overall review out of 5."),
   html.H3('➤ Usage:',    
        style={'fontSize':20, 'textAlign':'left', 'color': 'black'}),
   html.P("The user can select the style of her/his choice along with the range of ABV - alcohol by volume she/he wants."), 
   html.P("The dashboard will provide with a list of beers along with other information such as brewery, IBU, taste and review.")]),
  
   html.Label('➤ Select Style:', style={'fontSize': 20, 'textAlign':'left', 'color': 'black'}),
   dcc.Dropdown(
      id='stylez',
      options=[{'label': a, 'value': a} for a in sorted(set(list(df.Style)))],
      value = ['Lager', 'IPA', 'Pilsner'],
      multi = True,
      ),
   html.Label('➤ Select a range for ABV',style={'fontSize': 20, 'textAlign':'left', 'color': 'black'}),
   dcc.RangeSlider(id = 'sliderz',
                   min=0,
                   max=60,
                   value = [5,55], 
                   step=1,
                   marks={i: str(i) for i in range(0, 65, 2)}),
   
   html.Label('➤ Search Results',
           style={'fontSize':20, 'textAlign':'left', 'color': 'black'}),
   html.Br(),
    
   html.Div([dcc.Graph(id = 'bar', figure = fig1)]),
   html.Div([dcc.Graph(id = 'scatter', figure = fig2)]),
   #html.Div([html.P("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-")]),
   #html.Div(generate_table(df), id = 'table'),
   dash_table.DataTable(df.to_dict('records'), 
                        [{"name": i, "id": i} for i in df.columns],
                        id = 'tablez',
                        page_size=10,
                        style_table={'height': '400px', 'overflowY': 'auto'},
                        style_header={'backgroundColor': 'yellow'},
                        style_cell={'textAlign':'left','color': 'black'}
                        ),
   
    
   html.A('Dataset',
           href = 'https://www.kaggle.com/datasets/ruthgn/beer-profile-and-ratings-data-set?select=beer_profile_and_ratings.csv',
           target ='_blank'), 
   
])   

@app.callback(
    Output('bar','figure'),
    Input('stylez', 'value'),
    Input('sliderz', 'value')
    )

def update_bar(style_list, slider_range):
    df1=df[(df.Style.isin(style_list)) & (df['ABV']>=slider_range[0]) & (df['ABV']<= slider_range[1])]
    fig1 = px.histogram(df1, x = 'Style')
    return fig1

@app.callback(
    Output('scatter','figure'),
    Input('stylez','value'),
    Input('sliderz','value')
    )
def update_scatter(style_list, slider_range):
    df1=df[(df.Style.isin(style_list)) & (df['ABV']>=slider_range[0]) & (df['ABV']<= slider_range[1])]
    fig2 = px.scatter(df1, x = 'Review', y = 'ABV', hover_name= 'Beer Name', color = 'Style')
    return fig2

@app.callback(
    Output('tablez','data'),
    Input('stylez','value'),
    Input('sliderz','value')
    )
def update_table(style_list, slider_range):
    df1 = df[(df.Style.isin(style_list)) & (df['ABV']>=slider_range[0]) & (df['ABV']<= slider_range[1])]
    return df1.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, port = 8055)