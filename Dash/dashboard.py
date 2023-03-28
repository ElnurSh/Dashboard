from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_excel('brand.xlsx').sort_values('area_num', ascending=True)

dashboard = dbc.Container([
    dbc.Row(
        [
            dbc.Col([html.H1(id='row_one-col_one', children=len(df.index),

                             style={"height": "100px",
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center"}),

                     html.H6(id='row_one-col_one_1', children='ВСЕГО',
                             style={"text-align": "center"})], width=2,
                    style={"box-shadow": "0 0 10px 2px #888888",
                           'borderRadius': '5px',
                           "background-color": "#161A1D",
                           }),
            dbc.Col([html.H1(id='row_one-col_two', children=len(df.index),
                             style={"height": "100px",
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center"}),
                     html.H6(id='row_one-col_two_1', children='Коэффициент технической готовности',
                             style={"text-align": "center"})], width=2,

                    style={"box-shadow": "0 0 10px 2px #888888",
                           'borderRadius': '5px',
                           "background-color": "#161A1D",
                           "margin-left": "20px"
                           }),
            dbc.Col([html.H1(id='row_one-col_three', children=len(df.index),
                             style={"height": "100px",
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center"}),
                     html.H6(id='row_one-col_three_1', children='Коэффициент выезда из парка',
                             style={"text-align": "center"})], width=2,

                    style={"box-shadow": "0 0 10px 2px #888888",
                           'borderRadius': '5px',
                           "background-color": "#161A1D",
                           "margin-left": "20px"}),
            dbc.Col([
                html.Label('Выбрать участок'),
                dcc.Dropdown(id='dropdown',
                             options=df.area.unique().tolist(),
                             value=df.area.unique().tolist(),
                             multi=True,
                             style={"margin-bottom": "30px"}),
                html.Label('Выбрать диапазон объема двигателя'),
                dcc.RangeSlider(

                    1300, 3700,
                    step=None,
                    marks={i: {'label': str(i),
                               'style': {'writing-mode': 'vertical-lr', 'font-size': '12px'}
                               } for i in df.engine_volume.unique().tolist()},
                    allowCross=False,
                    updatemode='drag',
                    value=[df.engine_volume.min(), df.engine_volume.max()],
                    id='my-slider')], style={"background-color": "#161A1D",
                                             "box-shadow": "0 0 10px 2px #888888",
                                             "margin-left": "20px",
                                             'height': '170px'}),
            ], style={"margin-left": "20px",
                      "margin-top": "40px",
                      "margin-right": "20px", }),
    dbc.Row(
        [
            dbc.Col(html.Div(dcc.Graph(id="graph1"), style={"box-shadow": "0 0 10px 2px #888888"}), width=4),
            dbc.Col(
                html.Div(dcc.Graph(id="graph2"), style={"box-shadow": "0 0 10px 2px #888888", "margin-right": "15px"}),
                width=8)], style={"margin-top": "40px",
                                  "margin-bottom": "40px",
                                  "margin-left": "10px",
                                  'font-family': 'Segoe UI Arial sans-serif'},
    )
],
    fluid=True,
)
