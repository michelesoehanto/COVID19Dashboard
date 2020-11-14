import dash
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objs as go
import time

#different tabs
#from tabs import tab_0
#from tabs import tab1
#from tabs import tab_2
#from tabs import tab_3

## data frame
df = pd.read_csv("WHO-COVID-19-global-data.csv",low_memory= False)
dfcolor = pd.read_csv("color-country.csv", engine="python", sep=',', dtype={'Country':'string', 'Color':'string'})

## external scripts and external stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css']
external_scripts = ['https://code.jquery.com/jquery-3.5.1.js',
'https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js']

app = dash.Dash(__name__, external_scripts = external_scripts,
                external_stylesheets=external_stylesheets,suppress_callback_exceptions = True)
server = app.server

COLORS = [
    {
        'background': '#fef0d9',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#fdcc8a',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#fc8d59',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#d7301f',
        'text': 'white'
    },
]

listColor = [
    '#8B0000',
    '#A52A2A',
    '#B22222',
    '#DC143C',
    '#FF0000',
    '#FF6347',
    '#FF7F50',
    '#CD5C5C',
    '#F08080',
    '#E9967A',
    '#FA8072',
    '#FFA07A',
    '#FF4500',
    '#FF8C00',
    '#FFA500',
    '#FFD700',
    '#B8860B',
    '#DAA520',
    '#EEE8AA',
    '#BDB76B',
    '#F0E68C',
    '#808000',
    '#FFFF00',
    '#9ACD32',
    '#556B2F'
]




    

tab_style = {
    
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'backgroundColor': 'white',
    'color': '#119DFF',
    'padding': '6px'
}

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
                    ],value = "WPRO",placeholder='Filter by Region')]), width = {"offset":1},md =2),
        dbc.Col(
            html.Div([

               dcc.Dropdown(id='Country_dropdown', options=[
                        {'label': i, 'value': i} for i in df.Country.unique()
                    ],value = "Singapore", placeholder='Filter by Country')]), md= 2),
        dbc.Col(
            html.Div([
                
                dcc.Dropdown(id='Month_dropdown',  options=[
                        {'label': i, 'value': i} for i in df.Month.unique()
                    ],placeholder='Filter by Month')]),md = 2),
        
        dbc.Col(
            html.Div([
                
                dcc.Dropdown(id='Date_dropdown',  options=[
                        {'label': i, 'value': i} for i in df.Date_reported.unique()
                    ],placeholder='Filter by Date')]),md = 2),
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


app.layout = html.Div([
    html.Div(first_layout)
    
    ]
)

@app.callback(dash.dependencies.Output('WHO_dropdown','value'),
              [dash.dependencies.Input('clear-button', 'n_clicks')]
              )
def clearWho(clicks):
    if clicks == 0:
        return 'WPRO'
    if clicks !=0:
        return None
    
    
@app.callback(dash.dependencies.Output('Country_dropdown','value'),
              [dash.dependencies.Input('clear-button', 'n_clicks')]
              )
def clearWho(clicks):
    if clicks == 0:
        return 'Singapore'
    if clicks !=0:
        return None
    

@app.callback(dash.dependencies.Output('Month_dropdown','value'),
              [dash.dependencies.Input('clear-button', 'n_clicks')]
              )
def clearWho(clicks):
    if clicks !=0:
        return None

@app.callback(dash.dependencies.Output('Date_dropdown','value'),
              [dash.dependencies.Input('clear-button', 'n_clicks')]
              )
def clearWho(clicks):
    if clicks !=0:
        return None
    
# UPDATE COUNTRIES ACCORDING TO WHO REGION
@app.callback(dash.dependencies.Output('Country_dropdown','options'),
              [dash.dependencies.Input('WHO_dropdown', 'value')])

def updateDropdown(who):
    dataframe = df
    if who is None:
        return [{'label': i, 'value': i} for i in dataframe.Country.unique()]
   
    dataframe = dataframe.loc[dataframe['WHO_region']==who]
    return [{'label': i, 'value': i} for i in dataframe.Country.unique()]

@app.callback(dash.dependencies.Output('Date_dropdown','options'),
              [dash.dependencies.Input('Month_dropdown', 'value')])

def updateDropdown(month):
    dataframe = df
    if month is None:
        return [{'label': i, 'value': i} for i in dataframe.Date_reported.unique()]
    dataframe = dataframe.loc[dataframe['Month']==month]
    return [{'label': i, 'value': i} for i in dataframe.Date_reported.unique()]

@app.callback(dash.dependencies.Output('Month_dropdown','options'),
              [dash.dependencies.Input('Country_dropdown', 'value')])

def updateDropdown(country):
    dataframe = df
    if country is None:
        return [{'label': i, 'value': i} for i in dataframe.Month.unique()]
    dataframe = dataframe.loc[dataframe['Country']==country]
    nonzero = dataframe.loc[dataframe['Cumulative_cases'] > 0]
    

    return [{'label': i, 'value': i} for i in nonzero.Month.unique()]

@app.callback(Output("newcases", "children"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )
def updateNewCases(month, date, country, who):
    dataframe = df
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    
    val = dataframe['New_cases'].sum()
    return str(val)

@app.callback(Output("newdeaths", "children"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )
def updateNewCases(month, date, country, who):
    dataframe = df
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    
    val = dataframe['New_deaths'].sum()
    return str(val)

@app.callback(Output("nocases", "children"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )
def updateNewCases(month, date, country, who):
    dataframe = df
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    else:
        if month is not None:
            dataframe= dataframe.tail(1)
        else:
            lastdate = '5 Nov 2020'
            if who == "EURO":
                lastdate = '4 Nov 2020'
            dataframe = dataframe.loc[dataframe['Date_reported'] == lastdate]

    val = dataframe['Cumulative_cases'].sum()
    
    return str(val)

@app.callback(Output("nodeaths", "children"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )
def updateNoDeaths(month, date, country, who):
    dataframe = df
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    else:
        if month is not None:
            dataframe= dataframe.tail(1)
        else:
            lastdate = '5 Nov 2020'
            if who == "EURO":
                lastdate = '4 Nov 2020'
            dataframe = dataframe.loc[dataframe['Date_reported'] == lastdate]
    
    val = dataframe['Cumulative_deaths'].sum()
    return str(val)





    


## UPDATE STACKED BAR CHART    
@app.callback(Output("barchart1", "figure"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )

def updateGraph(month,date,country,who):
    time.sleep(1)
    dataframecolor = dfcolor
    count = 0
   
    
   
    dataframe = df
    layout = go.Layout(
                      
                       
                       xaxis = {
                           "title": "Date",
                    
                           },
                           
                       yaxis = {
                "title": "Daily Counts"},
                       title= 'Daily Case Count',
                       barmode="stack",
              
              showlegend=True)
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    data = []

    
    for i in dataframe.Country.unique():
        countrycase = dataframe.loc[dataframe['Country']== i]['Cumulative_cases']
        date = dataframe.loc[dataframe['Country']== i]['Date_reported']
        color = dataframecolor.loc[dataframecolor['Country']==i]['Color']
        try:
            color = color.values[0]
        except IndexError as e:
            color = listColor[count]
            count+=1
        trace_close = go.Bar(x = date, y= countrycase, name = i, marker={'color': color})
        
        data.append(trace_close)

    return {
        "data": data,
        "layout": layout
        
        }

@app.callback(Output("barchart2", "figure"),
              
              [Input("Month_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )

def updateGraph(month,country,who):
    dataframecolor = dfcolor
    count = 0
    color = 0
   
    dataframe = df
    layout = go.Layout(
                      
                       
                       xaxis = {
                           "title": "Date",
                    
                           },
                           
                       yaxis = {
                "title": "Daily Counts"},
                       title='Top 3 Countries By Death Toll',
        
              
              showlegend=True)
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
    
    
    data = []
    d = dataframe.groupby('Country').agg({'New_deaths':'sum'}).sort_values('New_deaths').tail(3).index.values
    for i in d:
        frame = dataframe.loc[dataframe['Country'] == i]['New_deaths'].sum()
        
            
        color = dataframecolor.loc[dataframecolor['Country']==i]['Color']
        try:
            color = color.values[0]
        except IndexError as e:
            color = listColor[count]
            count+=1
        trace_close = go.Bar(x = [i], y= [frame], name = i, marker={'color': color})
        data.append(trace_close)
        
    return {
        "data": data,
        "layout": layout
        
        }


  
@app.callback(Output("piechart", "figure"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )

def updatePie(month, date, country, who):
    dataframe = df
    layout = go.Layout(
                      
                       
                       xaxis = {
                           "title": "Date",
                    
                           },
                           
                       yaxis = {
                "title": "Daily Counts"},
                       title= 'Fatality Rate',
              
              showlegend=True)
   
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
        listOfCumulativeCases = dataframe['Cumulative_cases']
        listOfCumulativeDeaths = dataframe['Cumulative_deaths']
        
    elif month is not None:
    
        listOfCumulative = dataframe.loc[dataframe['Month'] == month]['Cumulative_cases'].tail(1)
        listOfCumulativeDeaths = dataframe.loc[dataframe['Month'] == month]['Cumulative_deaths'].tail(1)
    else:
        
        lastdate = '4 Nov 2020'
       
        listOfCumulativeCases = dataframe.loc[dataframe['Date_reported'] == lastdate]['Cumulative_cases']
        
        listOfCumulativeDeaths = dataframe.loc[dataframe['Date_reported'] == lastdate]['Cumulative_deaths']
        
    sumOfCumulativeCases = listOfCumulativeCases.sum()    
    sumOfCumulativeDeaths = listOfCumulativeDeaths.sum()

    

    data = [
        {
            'labels': ['Total Deaths','Total Cases'],
            'values':[sumOfCumulativeDeaths, sumOfCumulativeCases],
            'type': 'pie'
        }
    ]
    
    
    return {
        "data": data,
        "layout": layout
        }

@app.callback(Output("boxplot", "figure"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )

def updateBoxPlot(month,date,country,who):
    dataframe = df
    layout = go.Layout(
                      
                       
                       xaxis = {
                           "title": "Date",
                    
                           },
                           
                       yaxis = {
                "title":"Daily Counts"},
                       title= 'Distribution of New Cases and New Deaths',
              
              showlegend=True)
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    
    trace1 = go.Box(y = dataframe.New_cases, name = "New cases", marker = dict(color = 'blue'),line = dict(color = 'rgb(7,40,89)'))
    trace2 = go.Box(y = dataframe.New_deaths, name = "New Deaths", marker = dict(color = 'red'),line = dict(color = 'rgb(7,40,89)'))
    data = [trace1,trace2]
   
   
    
    
    return {
        "data": data,
        "layout": layout
        
        }





if __name__ == '__main__':
    app.run_server()



