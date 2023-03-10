import datetime as dt
import numpy as np
import pandas as pd
import plotly.express as px
import math
from dash_bootstrap_templates import load_figure_template

load_figure_template("sketchy")

def get_status(row,current_date,life_expectancy=100):
    e_date = row['week_end']
    s_date = row['week_start']
    year_real = row['year_real']
    status = "future"
    if s_date <= current_date:
        status = "current"
    if e_date < current_date:
        status = "past"
    if year_real > life_expectancy:
        status = "dead"
    
    return status

class Weekly_calendar:
    def get_end_date(self) -> dt.datetime:
        try:
            return self.start_date.replace(year=self.start_date.year + 100)
        except ValueError:
            return self.start_date.replace(year=self.start_date.year + 100, day=28)

    def define_calendar(self) -> pd.DataFrame:
        df = pd.DataFrame({"date": pd.date_range(self.start_date, self.end_date)})
        df['start_date'] = pd.to_datetime(self.start_date)
        df['week'] = df.apply(lambda x: math.floor((x['date']-x['start_date']).days/7.02403846154) ,axis=1)
        df['year_no'] = df.apply(lambda x: math.floor(x['week']/52) ,axis=1)
        df['year_real'] = df.apply(lambda x: x['week']/52 ,axis=1)
        df['week_no'] = df.apply(lambda x: math.floor(x['week'] - x['year_no']*52) ,axis=1)
        df2 = df.groupby(['year_no', 'week_no']).agg(week_start=('date', np.min),week_end=('date', np.max),year_real=('year_real',np.max)).reset_index()
        df2['status'] = df2.apply(lambda x: get_status(x,self.current_date,self.life_expectancy),axis=1)
        return df2

    def __init__(self,start_date,life_expectancy=100) -> None:
        self.start_date = start_date
        self.life_expectancy = life_expectancy
        self.current_date = dt.date.today()
        self.end_date = self.get_end_date()
        self.calendar = self.define_calendar()
        
def draw_graph(df,start_date):
    fig = px.scatter(df, 
        x = df['week_no'],
        y = df['year_no'],
        color = df["status"],
        color_discrete_map={"past": 'red',"future":"white","current":"green","dead":"black"},
        height = 850,
        template = "sketchy",
        labels=dict(week_no="Week", year_no="Year", status="Status"),
        #discrete_sequence=['black','red','yellow']#,
        #title = f"{start_date}"
        )
    fig.update_layout( 
        xaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 1 , range = [-0.5,51.5]),
        yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 5 , range = [-0.5,100.5])
    )
    fig.update_traces(marker_size=7,marker_line=dict(width=0.5,color="DarkSlateGrey"),selector=dict(mode='markers'))
    return fig