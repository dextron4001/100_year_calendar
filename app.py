from dash import Dash, html, dcc, Output, Input, State
import datetime as dt
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import math


start_date = dt.date(1990,2,19)
current_date = np.datetime64(dt.date.today())

SIDEBAR_STYLE = {
    "position" : "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem"
}

CONTENT_STYLE = {
    "margin-left" : "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}

def get_end_date(start_date):
    try:
        return start_date.replace(year=start_date.year + 100)
    except ValueError:
        # 👇️ preseve calendar day (if Feb 29th doesn't exist, set to 28th)
        return start_date.replace(year=start_date.year + 100, day=28)

end_date = get_end_date(start_date)

def get_status(row,current_date):
    e_date = row['week_end']
    s_date = row['week_start']
    status = "future"
    if s_date < current_date:
        status = "current"
        if e_date < current_date:
            status = "past"
    return status


def create_calendar(start_date,end_date,current_date):
    df = pd.DataFrame({"date": pd.date_range(start_date, end_date)})
    df['start_date'] = pd.to_datetime(start_date)
    df['week'] = df.apply(lambda x: math.floor((x['date']-x['start_date']).days/7.02403846154) ,axis=1)
    df['year_no'] = df.apply(lambda x: math.floor(x['week']/52) ,axis=1)
    df['week_no'] = df.apply(lambda x: math.floor(x['week'] - x['year_no']*52) ,axis=1)
    #df.to_csv('test1.csv')
    df2 = df.groupby(['year_no', 'week_no']).agg(week_start=('date', np.min),week_end=('date', np.max)).reset_index()
    df2['status'] = df2.apply(lambda x: get_status(x,current_date),axis=1)
    df2 = df2[df2['year_no']>=0] 
    df2 = df2[df2['year_no']<100]
    df2.to_csv('test.csv')
    return df2

df = create_calendar(start_date,end_date,current_date)

def draw_graph(df,start_date):
    fig = px.scatter(df, 
                x = df['week_no'],
                y = df['year_no'],
                color = df["status"],
                color_discrete_map={"True": 'red' },
                height = 900,
                template = 'plotly_dark',
                labels=dict(week_no="Week", year_no="Year", status="Status"),
                color_discrete_sequence=['black','red','yellow'],
                title = f"{start_date}"
                )
    fig.update_layout( 
        xaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 1 , range = [-0.5,51.5]),
        yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 5 , range = [-0.5,100.5])
    )
    fig.update_traces(marker_size=7,marker_line=dict(width=1),selector=dict(mode='markers'))
    return fig

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(external_stylesheets=[dbc.themes.DARKLY, dbc_css])

birthdate_picker = html.Div([
    html.Button("Birthdate",className="btn btn-dark"), # need to fix height and rounding on right hand side
    dcc.DatePickerSingle(date=start_date, id = "birthdate_input" ,className="mb-2") 
],
className="dbc"
)

submit_button = html.Div([
    html.Button("submit",id="submit-button",className="btn btn-primary align-right",n_clicks=0)
],
className="dbc"
)

sidebar = html.Div(
    [
        html.H1("Sidebar"),
        birthdate_picker,
        submit_button
    ],
    style = SIDEBAR_STYLE,
    className = 'bg-secondary'
)

content = html.Div(
    [
        html.Div("",id='output-text'),
        dcc.Graph(id="graph")
    ],
    style = CONTENT_STYLE,
    className = 'bg-dark'
)

app.layout = html.Div([sidebar,content])

@app.callback(
    Output("graph", "figure"), 
    Input("submit-button", "n_clicks"),
    State("birthdate_input", "date")
)
def update_bar_chart(n_clicks,start_date):
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = get_end_date(start_date)
    df = create_calendar(start_date,end_date,current_date)
    fig = draw_graph(df,start_date)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)