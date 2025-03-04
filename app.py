import dash_table
import plotly.express as px
from datetime import datetime
import pandas as pd
from dash import dcc, html, Dash , Input, Output, State
import dash_bootstrap_components as dbc
from pandas_datareader import wb

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY]) # changed theme to dark

indicators = {
    "NV.AGR.TOTL.ZS": "Agriculture, forestry, and fishing, value added (% of GDP)",
    "NY.GDP.MKTP.CD": "GDP (current US$)"
}

countries = wb.get_countries()
countries["capitalCity"].replace({"": None}, inplace=True)
countries.dropna(subset=["capitalCity"], inplace=True)
countries = countries[["name", "iso3c"]]
countries = countries.rename(columns={"name": "country"})

south_america_iso3 = [
    "ARG", "BOL", "BRA", "CHL", "COL", "ECU", "GUY",
    "PRY", "PER", "SUR", "URY", "VEN"
]

def update_wb_data():
    df = wb.download(
        indicator=(list(indicators)),
        country=south_america_iso3,
        start=1981,
        end=2023
    )
    df = df.reset_index()
    df.year = df.year.astype(int)
    df = pd.merge(df, countries, on="country")
    df = df.rename(columns=indicators)
    return df

df = update_wb_data()
df = df[df["iso3c"].isin(south_america_iso3)]

fig = px.choropleth(
    df,
    locations="iso3c", # country codes
    color="Agriculture, forestry, and fishing, value added (% of GDP)",
    hover_name="country", # display country names when hovering over them
    scope="south america",
    projection="natural earth",) # some type of map projection that i might delete


app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                html.H1(
                    "Socioeconomic Development in South America: Agriculture, forestry, and fishing & GDP Trends ",
                    style={"textAlign": "center"},
                ),
                html.H3(
                    f"Data last fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    style={"textAlign": "center", "color": "#888"},
                ),
                dcc.Graph(id="my-choropleth", figure=fig),
            ],
            width=12,
        )
    ),

    # Second Row - Select Data Set and Year Range
    dbc.Row([
        dbc.Col([
            dbc.Label("Select Data Set:", className="fw-bold", style={"textDecoration": "underline", "fontSize": 20}),
            dcc.Dropdown(
                id="my-dropdown",
                options=[{"label": i, "value": i} for i in indicators.values()],
                value=list(indicators.values())[0],
            )
            ], width=4),
        dbc.Col([
            dbc.Label(
                "Select Years:",
                className="fw-bold",
                style={"textDecoration": "underline", "fontSize": 20},
            ),
            dcc.RangeSlider(
                    id="years-range",
                    min=1981,
                    max=2023,
                    step=5,
                    value=[1981, 2023],
                    marks={year: str(year) for year in range(1981, 2024, 5)},
                ),
            ], width=6),
            dbc.Col(
                dbc.Button(
                    id="my-button",
                    children="Submit",  # prop represents the text displayed on the button
                    n_clicks=0,
                    color="primary",  # prop sets the color of the button background.
                    className="mb-2",
                ),
                width=6,
                className="d-flex justify-content-end",
            ),
            ], justify="end"),

            # 3rd Row - Country Data Over Time
        dbc.Row([
                dbc.Col([
                    html.H3("Country Data Over Time"),
                    dcc.Graph(id="my-country-over-time", figure=fig),
                ], width=12),
            ]),

        # # 4th Row - Select Country and Year for Country Data
        # dbc.Row([
        #         dbc.Col([
        #             dbc.Label("Select Country:", className="fw-bold", style={"textDecoration": "underline", "fontSize": 20}),
        #             dcc.Dropdown(
        #                 id="country-dropdown",
        #                 options=[{"label": c, "value": c} for c in df["country"].unique()],
        #                 value=df["country"].unique()[0],
        #             )
        #         ], width=4),
        #         dbc.Col(
        #             dbc.Button(
        #                 id="my-country-button",
        #                 children="Submit",  # prop represents the text displayed on the button
        #                 n_clicks=0,
        #                 color="primary",  # prop sets the color of the button background.
        #                 className="mb-2",
        #             ),
        #             width=6,
        #             className="d-flex justify-content-end",
        #         ),
        #     ], justify="end"),
    dbc.Row([
        dbc.Col([
            dbc.Label("Select Country 1:", className="fw-bold", style={"textDecoration": "underline", "fontSize": 20}),
            dcc.Dropdown(
                id="country-1-dropdown",
                options=[{"label": c, "value": c} for c in df["country"].unique()],
                value="Guyana" # default country (min)
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Select Country 2:", className="fw-bold", style={"textDecoration": "underline", "fontSize": 20}),
            dcc.Dropdown(
                id="country-2-dropdown",
                options=[{"label": c, "value": c} for c in df["country"].unique()],
                value="Bolivia" # default country (max)
            ),
        ], width=3),
    ]),
    # row for 2 bar charts
    dbc.Row([
        dbc.Col([
            html.H3("Agriculture, forestry, and fishing, value added (% of GDP) - Country 1"),
            dcc.Graph(id="country-1-bar"),
        ], width=6),
        dbc.Col([
            html.H3("Agriculture, forestry, and fishing, value added (% of GDP) - Country 2"),
            dcc.Graph(id="country-2-bar"),
        ], width=6),
    ])
])

@app.callback(
    [Output("my-choropleth", "figure"),
    Output("my-country-over-time", "figure"),
     Output("country-1-bar", "figure"),
     Output("country-2-bar", "figure"),],
    [Input("my-dropdown", "value"),
    Input("my-button", "n_clicks"),
     Input("country-1-dropdown", "value"),
     Input("country-2-dropdown", "value")],
    [State("years-range", "value")],
)
def update_choropleth(indct_chosen, n_clicks, country1, country2, years_chosen):

    if not isinstance(years_chosen, (list, tuple)) or len(years_chosen) != 2:
        years_chosen = [1981, 2023]

    dff = update_wb_data()
    dff = dff[dff["iso3c"].isin(south_america_iso3)]
    dff = dff[dff.year.between(years_chosen[0], years_chosen[1])]

    if dff.empty:
        return px.choropleth(), px.line(), [], px.bar(), px.bar()

    choropleth_fig = px.choropleth(
        data_frame=dff,
        locations="iso3c",
        color=indct_chosen,
        scope="south america",
        hover_data={"iso3c": False, "country": True},
    )
    choropleth_fig.update_layout(
        geo={"projection": {"type": "natural earth"}},
        margin=dict(l=0, r=0, t=0, b=0),
    )

    country_time_figure = px.line(
        dff,
        x="year",
        y=[indicators["NV.AGR.TOTL.ZS"], indicators["NY.GDP.MKTP.CD"]],
        color="country",
        title="Country Data Over Time")

    # bar graphs
    country1_data = dff[dff["country"] == country1]
    country2_data = dff[dff["country"] == country2]

    country1_bar = px.bar(
        country1_data,
        x="year",
        y="Agriculture, forestry, and fishing, value added (% of GDP)",
        title=f"{country1} - Agriculture Value Added (% of GDP)",
        labels={"year": "Year", "Agriculture, forestry, and fishing, value added (% of GDP)": "% of GDP"},
    )

    country2_bar = px.bar(
        country2_data,
        x="year",
        y="Agriculture, forestry, and fishing, value added (% of GDP)",
        title=f"{country2} - Agriculture Value Added (% of GDP)",
        labels={"year": "Year", "Agriculture, forestry, and fishing, value added (% of GDP)": "% of GDP"},
    )

    # ["NV.AGR.TOTL.ZS", "NY.GDP.MKTP.CD"]
    return choropleth_fig, country_time_figure, country1_bar, country2_bar

if __name__ == "__main__":
    app.run_server(debug=True)