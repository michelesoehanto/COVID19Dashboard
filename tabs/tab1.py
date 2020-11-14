import dash
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objs as go

df = pd.read_csv("/Users/MicheleS/AppData/Local/Programs/Python/Python37/Dashboard_proj/WHO-COVID-19-global-data.csv")
dfcolor = pd.read_csv("/Users/MicheleS/AppData/Local/Programs/Python/Python37/Dashboard_proj/color-country.csv",engine="python", sep=',', quotechar='"', error_bad_lines=False)
fig = go.Figure()
first_layout = html.Div([
    ### heading
    dbc.Row([
        dbc.Col(
            html.Div(html.H4("COVID-19 Dashboard", style = {'font-weight':'bold', 
                        'font-size':28})), width = {'offset':1},md =4),
        dbc.Col(
            html.Div(html.H4("A real time COVID-19 Monitoring dashboard that tracks global deaths tolls and covid cases to 5 November 2020.  Data source: https://covid19.who.int/table ",
                             style = {
                        'font-size':16})), md =6)
        ]),
    ### headings of dropdowns
    dbc.Row([
        dbc.Col(
            html.Div(html.H4("WHO Region", style = {'font-weight':'bold', 
                        'font-size':16})),width = {'offset':1}, md =2),
        dbc.Col(
            html.Div(html.H4("Country", style = {'font-weight':'bold', 
                        'font-size':16})),md = 2),
        dbc.Col(
            html.Div(html.H4("Month Reported", style = {'font-weight':'bold', 
                        'font-size':16})),md =2),
      
        dbc.Col(
            html.Div(html.H4("Date Reported", style = {'font-weight':'bold', 
                        'font-size':16})),md = 2),
    ]),
    
    dbc.Row([
        dbc.Col(
            html.Div([

               dcc.Dropdown(id='WHO_dropdown', options=[
                        {'label': i, 'value': i} for i in df.WHO_region.unique()
                    ],placeholder='Filter by Country_code',persistence = True, persistence_type = 'session')]), width = {"offset":1},md =2),
        dbc.Col(
            html.Div([

               dcc.Dropdown(id='Country_dropdown', options=[
                        {'label': i, 'value': i} for i in df.Country.unique()
                    ],placeholder='Filter by Country_code',persistence = True, persistence_type = 'session')]), md= 2),
        dbc.Col(
            html.Div([
                
                dcc.Dropdown(id='Month_dropdown',  options=[
                        {'label': i, 'value': i} for i in df.Month.unique()
                    ],placeholder='Filter by Date',persistence = True, persistence_type = 'session')]),md = 2),
        
        dbc.Col(
            html.Div([
                
                dcc.Dropdown(id='Date_dropdown',  options=[
                        {'label': i, 'value': i} for i in df.Date_reported.unique()
                    ],placeholder='Filter by Date',persistence = True, persistence_type = 'session')]),md = 2),
        dbc.Col(
            html.Div([
                html.Button('Clear', id='clear-button', n_clicks=0)])
            )
                
               

    ]),
    dbc.Row([
        
        dbc.Col(
            html.Div(children = [html.H4("New Cases", style = {'font-weight':'bold','text-align':'center',
                        'font-size':16, 'color':'black'}),html.Div(id = "newcases", style = {'font-weight':'bold','text-align':'center',
                        'font-size':25, 'color':'black','text-align':'center'})],style = { 'background-color': '#fae6af'}), width = {"offset":1}, md =2),
        dbc.Col(
            html.Div(children = [html.H4("New Deaths", style = {'font-weight':'bold','text-align':'center',
                        'font-size':16, 'color':'black'}),html.Div(id = "newdeaths", style = {'font-weight':'bold','text-align':'center',
                        'font-size':25, 'color':'black','text-align':'center'})],style = { 'background-color': '#b2cbed'}), md =2),
        dbc.Col(
            html.Div(children = [html.H4("No. Cases", style = {'font-weight':'bold','text-align':'center',
                        'font-size':16, 'color':'black'}),html.Div(id="nocases", style = {'font-weight':'bold','text-align':'center',
                        'font-size':25, 'color':'black','text-align':'center'})],style = { 'background-color': '#d7f5bc'}), md =2),
        dbc.Col(
            html.Div(children = [html.H4("No. Deaths", style = {'font-weight':'bold','text-align':'center',
                        'font-size':16, 'color':'black'}),html.Div(id = "nodeaths", style = {'font-weight':'bold','text-align':'center',
                        'font-size':25, 'color':'black','text-align':'center'})],style = { 'background-color': '#fadcf4'}), md =2)
    ]),
  
        
    ##### dropdowns 
    
    ### Stacked Bar Chart
    dcc.Loading(id = "loading1", children =[html.Div(
    dcc.Graph(id = "barchart1"))]),
    ### Pie Chart
    dbc.Row([
        dbc.Col(
            html.Div([
                
                dcc.Graph(id = "barchart2")]),md = 4),
        dbc.Col(
            html.Div([
                
                dcc.Graph(id = "piechart")]),md = 4),
        dbc.Col(
            html.Div([
                
                dcc.Graph(id = "boxplot")]),md = 4),
        ])
])
