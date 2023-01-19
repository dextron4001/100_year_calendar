from lib.functions import Weekly_calendar, draw_graph
from dash import Dash, html, dcc, Output, Input, State
import datetime as dt
import dash_bootstrap_components as dbc

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

start_date = dt.date(1990,1,1)

SIDEBAR_STYLE = {
    "position" : "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem"
}

CONTENT_STYLE = {
    "padding": "1rem 1rem"
}


calendar = Weekly_calendar(start_date)
fig = draw_graph(calendar.calendar,start_date)

app = Dash(external_stylesheets=[dbc.themes.DARKLY,dbc_css])
server = app.server

birthdate_picker = html.Div(
            [
                html.Div(
                    "Birthdate",
                    style={"display":"inline", "margin-right" : "10px", "font-size": "19px","font-family": "var(--bs-body-font-family)"}
                ),
                dcc.DatePickerSingle(
                    date = start_date,
                    display_format='DD/MMM/YY',
                    max_date_allowed=calendar.end_date,
                    #month_format='Do/MMM/YY',
                    id = "birthdate_input",
                    style={"display":"inline"}
                )
            ],
            style={
                "float":"right",
                "margin" : "5px"
                }
        )

top_bar = html.Div(
        [
            html.H1("100 year calendar",style={"display":"inline","margin":"5px","padding":"5px"}),
            birthdate_picker
        ],
        style= {"position" : "relative", "height" : "5%"},
        className = "bg-secondary"
    )

content = html.Div(
    [
        html.Div("",id='output-text'),
        dcc.Graph(id="graph",figure=fig)
    ],
    style = CONTENT_STYLE,
    className = 'bg-dark'
)

app.layout = html.Div([top_bar,content],className="dbc")

@app.callback(
    Output("graph", "figure"), 
    Input("birthdate_input", "date")
)
def update_bar_chart(start_date):
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    calendar = Weekly_calendar(start_date)
    fig = draw_graph(calendar.calendar,start_date)
    return fig

if __name__ == '__main__':
    app.run_server()