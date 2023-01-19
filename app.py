from lib.functions import Weekly_calendar, draw_graph
from dash import Dash, html, dcc, Output, Input , State
import pandas as pd

import datetime as dt

import dash_bootstrap_components as dbc

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
start_date = dt.date(1990,1,1)

calendar = Weekly_calendar(start_date)
fig = draw_graph(calendar.calendar,start_date)

life_expectancy_data = pd.read_csv('data/life-expectancy-at-birth-total-years.csv')
print(life_expectancy_data.columns)
life_expectancy_options = life_expectancy_data['Entity'].unique().tolist()

app = Dash(external_stylesheets=[dbc.themes.SKETCHY,dbc_css])
server = app.server

app.layout = html.Div(
    [
        html.Div("logo",id="logo"),
        html.Div(html.H1("100 Year Calendar",style={"float":"right"}),id="header"),
        html.Div(dcc.Graph(id="graph",figure=fig),id="content"),
        html.Div(
            html.Div(
            [
                html.Div(
                    "Birthdate",
                    style={"display":"inline", "margin-right" : "10px", "padding-top": "10px","font-size": "19px","font-family": "var(--bs-body-font-family)"}
                ),
                dcc.DatePickerSingle(
                    date = start_date,
                    display_format='DD/MMM/YY',
                    max_date_allowed=calendar.end_date,
                    #month_format='Do/MMM/YY',
                    id = "birthdate_input",
                    style={"display":"inline"}
                ),
                html.Div(
                    "Location",
                    style={"display":"inline", "margin-right" : "10px", "padding-top": "10px", "font-size": "19px","font-family": "var(--bs-body-font-family)"}
                ),
                dcc.Dropdown(life_expectancy_options, id="location-dropdown"),
                html.Div("Add link to poster",style={"float":"bottom"})
            ],
            style={
                "float":"right",
                "margin" : "5px"
                }
            )
            ,id="side"
        ),
        html.Div(html.P("Copyright Dexter Robinson 2023 ",style={"float":"right","margin":"2px"}),id="footer")
    ],
    className="app-grid"
)

@app.callback(
    Output("graph", "figure"), 
    Input("birthdate_input", "date"),
    Input("location-dropdown","value")
)
def update_bar_chart(start_date,location):
    life_expectancy = 100
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    year = start_date.year
    if location != None:
        filtered_data = life_expectancy_data[life_expectancy_data['Entity']==location]
        filtered_data = filtered_data.iloc[(filtered_data['Year']-year).abs().argsort()[:1]]
        life_expectancy = filtered_data['Life expectancy at birth, total (years)'].iloc[0]
        print(life_expectancy)

    calendar = Weekly_calendar(start_date,life_expectancy)
    fig = draw_graph(calendar.calendar,start_date)
    return fig

if __name__ == '__main__':
    app.run_server()

