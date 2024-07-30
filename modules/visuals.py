import plotly.graph_objects as go
from datetime import datetime
import pandas

LOWER_SAMPLE_BOUNDS: float = 0.0
UPPER_LOWER_BOUNDS: float = 1.0

def map_figure(df: pandas.DataFrame, date: datetime,sample_ratio: float=None, export_location: str=None) -> None:
    scl : tuple = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
        [0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
        [0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]

    df : pandas.DataFrame = df.loc[df["DATE"] == str(date)].sample(frac=float((sample_ratio if float(sample_ratio) > 0.0 or float(sample_ratio) <= 1.0 else 1.0)))
    fig = go.Figure(data=go.Scattergeo(
        locationmode="ISO-3",
        lon=df['LONGITUDE'],
        lat=df['LATITUDE'],
        mode="markers",
        text=df["TEMP"],
        marker=dict(
            color = df['TEMP'],
            colorscale = scl,
            opacity = 0.7,
            size = 3,
            cmax = df["TEMP"].max(),
            colorbar_title=f"Average Temperatures<br>{date.strftime('%b %d, %Y')}"
        )
    ))

    fig.update_layout(
        geo = dict(
            showsubunits = True,
            showcountries = True,
            resolution = 110,
        ),
        title = "Global Surface Summary of the Day"
    )

    fig.write_image(export_location, format="jpg")