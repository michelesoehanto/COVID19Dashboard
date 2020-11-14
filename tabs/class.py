@app.callback(Output("places", "children"),
              
              [
               Input("WHO_dropdown", "value")]
              )
def updateNewCases(who):
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    month = dataframe.groupby('Country')['Cumulative_cases'].sort_values('Cumulative_cases')
    return month.tail(1).Country

@app.callback(Output("nocases", "children"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )
def updateNewCases(month, date, country, who):
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    val = dataframe['Cumulative_cases'].tail(1)
    return str(val)

@app.callback(Output("nodeaths", "children"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )
def updateNewCases(month, date, country, who):
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
    if country is not None:
        dataframe = dataframe.loc[dataframe['Country'] == country]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    val = dataframe['Cumulative_deaths'].tail(1)
    return str(val)


#####TOP 3 charts
@app.callback(Output("barchart2", "figure"),
              
              [Input("Month_dropdown", "value"),
               Input("Date_dropdown", "value"),
               Input("Country_dropdown", "value"),
               Input("WHO_dropdown", "value")]
              )

def updateGraph(month,date,country,who):
    dataframecolor = dfcolor
    count = 0
    
   
    dataframe = df
    layout = go.Layout(
                      
                       
                       xaxis = {
                           "title": "Date",
                    
                           },
                           
                       yaxis = {
                "title": "Daily Counts"},
        
              
              showlegend=True)
    if who is not None:
        dataframe = dataframe.loc[dataframe['WHO_region'] == who]
        
    if month is not None:
        dataframe = dataframe.loc[dataframe['Month'] == month]
        
    if date is not None:
        dataframe = dataframe.loc[dataframe['Date_reported'] == date]
    data = []
    d = dataframe.groupby('Country').agg({'New_deaths':'sum'}).sort_values('New_deaths').tail(3)['Country']
    for i in range(3):
        frame = dataframe.loc[dataframe['Country'] == d[i]]['New_deaths'].sum()
        data.append(frame)
        
    return {
        "data": data,
        "layout": layout
        
        }
