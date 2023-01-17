from lib.functions import Weekly_calendar, draw_graph
from dash import Dash, html, dcc, Output, Input, State
import datetime as dt
import dash_bootstrap_components as dbc

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

start_date = dt.date(1990,2,19)

SIDEBAR_STYLE = {
    "position" : "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem"
}

CONTENT_STYLE = {
    "margin-left" : "2rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem"
}


calendar = Weekly_calendar(start_date)
fig = draw_graph(calendar.calendar,start_date)

app = Dash(external_stylesheets=[dbc.themes.DARKLY,dbc_css])

birthdate_picker = html.Div(
            [
                html.Div(
                    "Birthdate",
                    style={"display":"inline", "margin-right" : "10px", "font-size": "19px","font-family": "var(--bs-body-font-family)"}
                ),
                dcc.DatePickerSingle(
                    date = start_date,
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
            html.H1("100 year calendar",style={"display":"inline"}),
            birthdate_picker
        ],
        style= {"position" : "relative"},
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
    app.run_server(debug=True)