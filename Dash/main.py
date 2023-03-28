from dash import Dash, html, dcc, State, Output, Input, no_update
import dash_bootstrap_components as dbc
import plotly.express as pex
import sqlite3
from dashboard import dashboard, df

db = sqlite3.connect('my_db.db', check_same_thread=False)
cursor = db.cursor()

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Transport Department"
app.config.suppress_callback_exceptions = True

# Define your login layout
login_layout = html.Div(className='login', id='login', children=[html.Div(className='head', children=[
     html.H1('Transport Department', className='company')]),
     html.P('SOCAR', className='msg'),
     html.Div(className='form', children=[
         dcc.Input(type='text', placeholder='username', className='text', id='username'),
         html.Br(),
         dcc.Input(type='password', placeholder='••••••••••••••', className='password', id='password'),
         html.Br(),
         html.Button('Login', n_clicks=0, className='btn-login', id='do-login'),
         html.Br(), html.Br(),
         html.Div(id='output', className='callback-answer')
         ])
 ])

# Define your dashboard layout
dashboard_layout = dashboard

# Define your app layout with dcc.Location and the login layout as the default content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=login_layout),

])


# Define a callback that listens to changes in the URL and updates the page content accordingly
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              )
def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard_layout
    else:
        return login_layout


# Define a callback for the login button that updates the URL
@app.callback(Output('url', 'pathname'),
              Output('output', 'children'),
              Input('do-login', 'n_clicks'),
              State('username', 'value'),
              State('password', 'value'))
def login(n_clicks, username, password):
    if n_clicks:
        # your login logic here
        if not username and not password:
            return no_update, 'fill login and password'
        if username and not password:
            return no_update, 'fill password'
        if not username and password:
            return no_update, 'fill username'
        if username and password:
            for user, pwd in cursor.execute('SELECT * FROM logins'):
                if user == username and pwd == password:
                    return '/dashboard', no_update
                else:
                    return no_update, 'incorrect username or password'
    else:
        return '/', no_update


@app.callback(Output('row_one-col_one', 'children'),
              Output('row_one-col_two', 'children'),
              Output('row_one-col_three', 'children'),
              Output('graph1', 'figure'),
              Output('graph2', 'figure'),
              Input('dropdown', 'value'),
              Input('my-slider', 'value'))
def update_dashboard(drop_value, slider_value):
    row_one_col_one = len(df[(df.engine_volume.between(slider_value[0], slider_value[1])) &
                             (df.area.isin(drop_value))])
    if row_one_col_one == 0:
        row_one_col_two = 0
    else:
        row_one_col_two = format(len(df[(df.engine_volume.between(slider_value[0],
                                                                  slider_value[1])) & (df.area.isin(drop_value)) &
                                 (~df.note.isin(['repair', 'VM-2']))]) /
                                 len(df[(df.engine_volume.between(slider_value[0],
                                                                  slider_value[1])) &
                                        (df.area.isin(drop_value))]), '.2f')
    if row_one_col_one == 0:
        row_one_col_three = 0
    else:
        row_one_col_three = format(len(df[(df.engine_volume.between(slider_value[0],
                                                                    slider_value[1])) & (df.area.isin(drop_value)) & (~df.organization.isin(['простой_автомобиля']))]) /
        len(df[(df.engine_volume.between(slider_value[0], slider_value[1])) & (df.area.isin(drop_value))]), '.2f')
    fig1 = pex.pie(df[(df.engine_volume.between(slider_value[0], slider_value[1])) & (df.area.isin(drop_value))],
                   names='organization', color='organization',
                   category_orders={'organization': ["azerigas", "downstream", "itcd", "простой_автомобиля", ]},
                   title='Парк автомобилей', hole=.3).update_layout(
                   paper_bgcolor='rgba(22, 26, 29, 255)',
                   title_font_color='yellow',
                   title_x=0.44,
                   font_color="white")
    fig2 = pex.bar(df[(df.engine_volume.between(slider_value[0], slider_value[1])) & (df.area.isin(drop_value))],
                   x="area", y="note_num",
                   color='note', barmode="group",
                   category_orders={'area': ["1№ area", "2№ area", "3№ area", "4№ area", ]}).update_layout(
                   paper_bgcolor='rgba(22, 26, 29, 255)',
                   plot_bgcolor='rgba(22, 26, 29, 255)',
                   font_color="white",
                   title={'text': 'Простой автомобилей', 'x': 0.5, 'font_color': 'yellow'},
                   xaxis_title={'text': 'Участок', 'font': {'color': 'red'}},
                   yaxis_title={'text': 'Количество', 'font': {'color': 'red'}},
                   legend={'title': {'text': ""}, 'font': {'color': 'white'}})

    return row_one_col_one, row_one_col_two, row_one_col_three, fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
