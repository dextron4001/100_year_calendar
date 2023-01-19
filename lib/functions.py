import datetime as dt
import numpy as np
import pandas as pd
import plotly.express as px
import math

def get_status(row,current_date):
    e_date = row['week_end']
    s_date = row['week_start']
    status = "future"
    if s_date <= current_date:
        status = "current"
    if e_date < current_date:
        status = "past"
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
        df['week_no'] = df.apply(lambda x: math.floor(x['week'] - x['year_no']*52) ,axis=1)
        df2 = df.groupby(['year_no', 'week_no']).agg(week_start=('date', np.min),week_end=('date', np.max)).reset_index()
        df2['status'] = df2.apply(lambda x: get_status(x,self.current_date),axis=1)
        return df2

    def __init__(self,start_date) -> None:
        self.start_date = start_date
        self.current_date = dt.date.today()
        self.end_date = self.get_end_date()
        self.calendar = self.define_calendar()
        
def draw_graph(df,start_date):
    fig = px.scatter(df, 
        x = df['week_no'],
        y = df['year_no'],
        color = df["status"],
        color_discrete_map={"True": 'red' },
        height = 850,
        template = 'plotly_dark',
        labels=dict(week_no="Week", year_no="Year", status="Status"),
        color_discrete_sequence=['black','red','yellow']#,
        #title = f"{start_date}"
        )
    fig.update_layout( 
        xaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 1 , range = [-0.5,51.5]),
        yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 5 , range = [-0.5,100.5])
    )
    fig.update_traces(marker_size=7,marker_line=dict(width=1),selector=dict(mode='markers'))
    return fig

C = Weekly_calendar(dt.date(1990,2,19))

print(C.__dict__)