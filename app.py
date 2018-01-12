
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
from plotly.graph_objs import *
import plotly.plotly as py
import pandas as pd
import numpy as np
import calendar
import plotly
import os
from pandas.tseries.offsets import MonthEnd
import base64

#--------------------------- APP AND SERVER CONFIG

app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div(style = {'font-family': 'Helvetica', 'background-color': '#ffffff', 'overflow': 'hidden', 'background-color': '#275968'}, children =[
    html.Div(style = {'font-family': 'Helvetica', 'font-size': '15','max-width': '100%','margin': 'auto', 'padding-left': '25px', 'padding-top': '20px','background-color': '#275968'}, children=[
        html.H1(style = {'font-family': 'Helvetica', 'font-size': '33','color': '#ffffff'},children='Escoja el tipo de información que desea ver:')
    ]),
    html.Div(style = {'height':'100vh','margin': 'auto','text-align':'middle','background-color': '#275968','padding-left': '25px', 'padding-top': '25px','font-family': 'Helvetica', 'font-size': '13','width': '50%', 'color': '#ffffff', 'margin': 'auto', 'float':'left','box-shadow': '4px 5px 9px -3px rgba(102,102,102,1)'}, children =[
        html.H2(style = {'font-family': 'Helvetica', 'font-size': '28','color': '#ffffff','margin': 'auto'}, children='Dashboards comerciales:'),
        html.Br(),
        html.Img(src='https://cdn4.iconfinder.com/data/icons/ikooni-outline-seo-web/128/seo-51-512.png', style={'height':"50", 'width':"50", 'margin': 'auto', 'display':'block'}),
        html.A(html.Button('Ir a Dashboard Localidad+Director', className='btn btn-primary btn-block', style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '16', 'width': '50%', 'height': '10vh','background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
           href='/page-1'),
        html.Br(),
        html.Img(src='https://cdn4.iconfinder.com/data/icons/ikooni-outline-seo-web/128/seo-51-512.png', style={'height':"50", 'width':"50", 'margin': 'auto', 'display':'block'}),
        html.A(html.Button('Ir a Dashboard Director+Informador', className='btn btn-primary btn-block', style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '16', 'width': '50%','height': '10vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
               href='/page-2'),
        html.Br(),
        html.Img(src='https://cdn4.iconfinder.com/data/icons/ikooni-outline-seo-web/128/seo-51-512.png', style={'height':"50", 'width':"50", 'margin': 'auto', 'display':'block'}),
        html.A(html.Button('Ir a Dashboard Director+Asesor', className='btn btn-primary btn-block', style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '16', 'width': '50%', 'height': '10vh','background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
               href='/page-3'),

    ]),
    html.Div(style = {'height':'100vh','margin': 'auto','text-align':'middle','background-color': '#275968','padding-left': '25px', 'padding-top': '25px','font-family': 'Helvetica', 'font-size': '13','width': '50%', 'color': '#ffffff',  'margin': 'auto', 'overflow': 'hidden'}, children =[
        html.H2(style = {'font-family': 'Helvetica', 'font-size': '28','color': '#ffffff','margin': 'auto'}, children='Rankings:'),
        html.Br(),
        html.Img(src='https://cdn2.iconfinder.com/data/icons/large-svg-icons-part-3/512/table_excel_row_document_teach-512.png', style={'height':"50", 'width':"50", 'margin': 'auto', 'display':'block'}),
        html.A(html.Button('Ir a Ranking Localidad', className='btn btn-primary btn-block', style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '16', 'width': '50%', 'height': '10vh','background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
           href='/page-4'),
        html.Br(),
        html.Img(src='https://cdn2.iconfinder.com/data/icons/large-svg-icons-part-3/512/table_excel_row_document_teach-512.png', style={'height':"50", 'width':"50", 'margin': 'auto', 'display':'block'}),
        html.A(html.Button('Ir a Ranking Director', className='btn btn-primary btn-block', style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '16', 'width': '50%','height': '10vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
               href='/page-5')
    ])
])


#--------------------------- DATABASES IMPORTS AND ADJUSTMENTS

base = pd.read_csv('https://raw.githubusercontent.com/Bancaseguros/DashboardCumplimiento/master/INFORME_DV_DIARIO.csv', delimiter = '|', encoding='latin-1')
del base['CODIGO_DIRECTOR_VENTAS']
base = base.drop_duplicates()

base['FECHA'] = pd.to_datetime(base['FECHA'], format='%d/%m/%Y', errors='coerce')
base['FECHA2'] = pd.to_datetime(base['FECHA'], format="%Y%m") + MonthEnd(0)
base['PRODUCTO']=base['PRODUCTO'].astype(str)
base['PRODUCTO'][base['PRODUCTO']=='98']='MULTIRIESGO NEGOCIO'
base['PRODUCTO'][base['PRODUCTO']=='721']='DAVIDA'
base['PRODUCTO'][base['PRODUCTO']=='793']='VIDA GRUPO NEGOCIO'
base['PRODUCTO'][base['PRODUCTO']=='115']='HOGAR BANCARIO'
base['PRODUCTO'][base['PRODUCTO']=='500']='DESEMPLEO'

base['DIRECTOR_VENTAS']=base['DIRECTOR_VENTAS'].str.upper()
base['LOCALIDAD']=base['LOCALIDAD'].str.upper()
base['ZONA_DAVIVIENDA']=base['ZONA_DAVIVIENDA'].str.upper()
base['GERENCIA_BOLIVAR']=base['GERENCIA_BOLIVAR'].str.upper()

base = base.sort_values(['FECHA', 'PRODUCTO', 'DIRECTOR_VENTAS'], ascending = [True, True, True])
                        
options_sgro = base['PRODUCTO'].unique()

baseMes = pd.read_csv('https://raw.githubusercontent.com/Bancaseguros/DashboardCumplimiento/master/INFORME_DV_MENSUAL.csv', delimiter = '|', encoding='latin-1')

baseMes['PRODUCTO']=baseMes['PRODUCTO'].astype(str)
baseMes['PRODUCTO'][baseMes['PRODUCTO']=='98']='MULTIRIESGO NEGOCIO'
baseMes['PRODUCTO'][baseMes['PRODUCTO']=='721']='DAVIDA'
baseMes['PRODUCTO'][baseMes['PRODUCTO']=='793']='VIDA GRUPO NEGOCIO'
baseMes['PRODUCTO'][baseMes['PRODUCTO']=='115']='HOGAR BANCARIO'
baseMes['PRODUCTO'][baseMes['PRODUCTO']=='500']='DESEMPLEO'

baseMes['DIRECTOR_VENTAS']=baseMes['DIRECTOR_VENTAS'].str.upper()
baseMes['LOCALIDAD']=baseMes['LOCALIDAD'].str.upper()
baseMes['ZONA_DAVIVIENDA']=baseMes['ZONA_DAVIVIENDA'].str.upper()
baseMes['GERENCIA_BOLIVAR']=baseMes['GERENCIA_BOLIVAR'].str.upper()


#--------------------------- APP LAYOUT (HTML + DCC)

page_1_layout = html.Div(style = {'font-family': 'Helvetica', 'height': '100%', 'background-color': '#ffffff', 'margin': '-8px', 'overflow': 'hidden'}, children =[
    html.Div(style = {'width': '30%', 'height': '700px', 'background-color': '#275968', 'margin': '0px', 'float': 'left', 'box-shadow': '4px 5px 9px -3px rgba(102,102,102,1)'}, children =[
        html.Div(style = {'max-width': '100%','margin': 'auto', 'padding-left': '25px', 'padding-top': '15px', 'padding-bottom': '0px'}, children=[
            html.H1(style = {'font-family': 'Helvetica', 'font-size': '28', 'color': '#ffffff'},children='Dashboard Localidad+Director')
        ]),
        html.Div(style = {'padding-left': '15px', 'padding-right': '15px', 'padding-top': '5px', 'font-size': '12'}, children = [
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '15'}, children = 'Seleccione tipo seguro:'),
            dcc.Dropdown(
                id ='sgro-drop',
                options = [{'label': i, 'value': i} for i in options_sgro],
                clearable = False
                ),
            html.Br(),
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '15'}, children = 'Seleccione gerencia:'),
            dcc.Dropdown(
                id ='ger-drop',
                clearable = False
                ),
            html.Br(),
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '15'}, children = 'Seleccione localidad:'),
            dcc.Dropdown(
                id ='loc-drop',
                clearable = False
                ),
            html.Br(),
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '15'}, children = 'Seleccione director:'),
            dcc.Dropdown(
                id ='dir-drop',
                clearable = False
                )
            ]),
        html.Br(),
        html.A(html.Button('Ir a Dashboard Director+Informador', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'height': '4vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-2'),
        html.A(html.Button('Ir a Dashboard Director+Asesor', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'height': '4vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-3'),
        html.Br(),
        html.A(html.Button('Ir a Ranking Localidad', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'height': '4vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-4'),
        html.A(html.Button('Ir a Ranking Director', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'height': '4vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-5'),
        html.A(html.Button('Ir al Inicio', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'height': '4vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/')
        ]),
    html.Div(style = {'width': '70%', 'height': '100%', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '30px', 'padding-bottom': '5px'}, children =[
        html.Div(style = {'width': '100%', 'height': '320px', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '30px'}, children = [
            html.Div(style = {'width': '50%', 'height': '100%', 'margin': '0px', 'float': 'left', 'padding-left':'10px'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Cumplimiento acumulado (%)'),
                dcc.Graph(id ='graph-1', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ]),
            html.Div(style = {'width': '50%', 'height': '100%', 'margin': '0px', 'float': 'left'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Cumplimiento DÃ­a (%)'),
                dcc.Graph(id ='graph-2', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ])
        ]),
        html.Div(style = {'width': '100%', 'height': '320px', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '20px'}, children = [
            html.Div(style = {'width': '100%', 'height': '100%', 'margin': '0px', 'float': 'left'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Cumplimiento mensual (%)'),
                dcc.Graph(id ='graph-3', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ])
        ])
    ])
])

#---------------------------------------------------------

#--------------------------- DEPENDENT DROPDOWNS CALLBACKS

@app.callback(
    dash.dependencies.Output('ger-drop', 'options'),
    [dash.dependencies.Input('sgro-drop', 'value')])
def set_cities_options(selected_sgro):
    filtro = base[base['PRODUCTO'] == selected_sgro]
    return [{'label': i, 'value': i} for i in filtro['GERENCIA_BOLIVAR'].unique()]

@app.callback(
    dash.dependencies.Output('loc-drop', 'options'),
    [dash.dependencies.Input('sgro-drop', 'value'),
     dash.dependencies.Input('ger-drop', 'value')])
def set_cities_options(selected_sgro, selected_ger):
    filtro = base[(base['PRODUCTO'] == selected_sgro)&(base['GERENCIA_BOLIVAR'] == selected_ger)]
    return [{'label': i, 'value': i} for i in filtro['LOCALIDAD'].unique()]
    
@app.callback(
    dash.dependencies.Output('dir-drop', 'options'),
    [dash.dependencies.Input('sgro-drop', 'value'),
     dash.dependencies.Input('ger-drop', 'value'),
     dash.dependencies.Input('loc-drop', 'value')])
def set_cities_options(selected_sgro, selected_ger, selected_loc):
    filtro = base[(base['PRODUCTO'] == selected_sgro)&(base['GERENCIA_BOLIVAR'] == selected_ger)&(base['LOCALIDAD'] == selected_loc)]
    return [{'label': i, 'value': i} for i in filtro['DIRECTOR_VENTAS'].unique()]


#---------------------------------------------------------

#--------------------------- GRAPH 1 "CUMPLIMIENTO DIARIO ACUMULADO"

@app.callback(
    dash.dependencies.Output('graph-1', 'figure'),
    [dash.dependencies.Input('sgro-drop', 'value'),
    dash.dependencies.Input('ger-drop', 'value'),
    dash.dependencies.Input('loc-drop', 'value'),
    dash.dependencies.Input('dir-drop', 'value')])
def update_figure(selected_sgro, selected_ger, selected_loc, selected_dir):

   
    base_filtro = base
    base_filtro1 = base_filtro[(base_filtro['PRODUCTO'] == selected_sgro)&(base_filtro['GERENCIA_BOLIVAR'] == selected_ger)&(base_filtro['LOCALIDAD'] == selected_loc)]
    base_filtro2 = base_filtro1[base_filtro['DIRECTOR_VENTAS'] == selected_dir]

    base_filtro2.reset_index()

    base_filtro1_todos=base_filtro1[base_filtro1['DIRECTOR_VENTAS']=='(TODOS)']


    base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtro1_todos['CUMPLIMIENTO_ACUMULADO']
    base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=round(base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']*100,1)
    base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO'].astype(str)
    base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']+'%'

    base_filtro2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=round(base_filtro2['CUMPLIMIENTO_ACUMULADO']*100,1)
    base_filtro2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtro2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO'].astype(str)
    base_filtro2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtro2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']+'%'

    base_filtro2['ETIQUETAS_OBJETIVO']=round((base_filtro2['FECHA'].dt.day/base_filtro2['FECHA2'].dt.day)*100,1)
    base_filtro2['ETIQUETAS_OBJETIVO']=base_filtro2['ETIQUETAS_OBJETIVO'].astype(str)
    base_filtro2['ETIQUETAS_OBJETIVO']=base_filtro2['ETIQUETAS_OBJETIVO']+'%'

    trace1 = Scatter(
    x = base_filtro2['FECHA'],
    y = base_filtro2['CUMPLIMIENTO_ACUMULADO']*100,
    text = base_filtro2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO'],
    name = 'Director',
    marker = {'color': '#3381ff'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    trace2 = Scatter(
    x = base_filtro2['FECHA'],
    y = (base_filtro2['FECHA'].dt.day/base_filtro2['FECHA2'].dt.day)*100,
    text = base_filtro2['ETIQUETAS_OBJETIVO'],
    name = 'Objetivo',
    marker = {'color': '#ff5733'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    trace3 = Scatter(
    x = base_filtro2['FECHA'],
    y = base_filtro1['CUMPLIMIENTO_ACUMULADO'][base_filtro1['DIRECTOR_VENTAS']=='(TODOS)']*100,
    text = base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO'],
    name = 'Total',
    marker = {'color': '#23c052'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(autorange=True, title = '', showgrid = False, showline = False, showticklabels = True),
    margin = {'l': 30, 'b': 200, 't': 0, 'r': 20},
    showlegend = True
    )

    data = Data([trace1, trace2, trace3])


    return Figure(data=data, layout=layout)

#--------------------------- GRAPH 2 "CUMPLIMIENTO DIARIO"

@app.callback(
    dash.dependencies.Output('graph-2', 'figure'),
    [dash.dependencies.Input('sgro-drop', 'value'),
    dash.dependencies.Input('ger-drop', 'value'),
    dash.dependencies.Input('loc-drop', 'value'),
    dash.dependencies.Input('dir-drop', 'value')])
def update_figure(selected_sgro, selected_ger, selected_loc, selected_dir):

   
    base_filtro = base
    base_filtro1 = base_filtro[(base_filtro['PRODUCTO'] == selected_sgro)&(base_filtro['GERENCIA_BOLIVAR'] == selected_ger)&(base_filtro['LOCALIDAD'] == selected_loc)]
    base_filtro2 = base_filtro1[base_filtro1['DIRECTOR_VENTAS'] == selected_dir]

    base_filtro1_todos=base_filtro1[base_filtro1['DIRECTOR_VENTAS']=='(TODOS)']

    base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtro1_todos['CUMPLIMIENTO_DIA']
    base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']=round(base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']*100,1)
    base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_DIA'].astype(str)
    base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']+'%'

    base_filtro2['ETIQUETAS_CUMPLIMIENTO_DIA']=round(base_filtro2['CUMPLIMIENTO_DIA']*100,1)
    base_filtro2['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtro2['ETIQUETAS_CUMPLIMIENTO_DIA'].astype(str)
    base_filtro2['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtro2['ETIQUETAS_CUMPLIMIENTO_DIA']+'%'

    base_filtro2['ETIQUETAS_OBJETIVO']=np.repeat(5.0,len(base_filtro2['FECHA']))
    base_filtro2['ETIQUETAS_OBJETIVO']=base_filtro2['ETIQUETAS_OBJETIVO'].astype(str)
    base_filtro2['ETIQUETAS_OBJETIVO']=base_filtro2['ETIQUETAS_OBJETIVO']+'%'

    trace1 = Scatter(
    x = base_filtro2['FECHA'],
    y = base_filtro2['CUMPLIMIENTO_DIA']*100,
    text = base_filtro2['ETIQUETAS_CUMPLIMIENTO_DIA'],
    name = 'Director',
    marker = {'color': '#3381ff'},
    mode = "lines",
    hoverinfo="x+text+name"
    )

    trace2 = Scatter(
    x = base_filtro2['FECHA'],
    y = np.repeat(0.05,len(base_filtro2['FECHA']))*100,
    text = base_filtro2['ETIQUETAS_OBJETIVO'],
    name = 'Objetivo',
    marker = {'color': '#ff5733'},
    mode = "lines",
    hoverinfo="x+text+name"
    )

    trace3 = Scatter(
    x = base_filtro2['FECHA'],
    y = base_filtro1['CUMPLIMIENTO_DIA'][base_filtro1['DIRECTOR_VENTAS']=='(TODOS)']*100,
    text = base_filtro1_todos['ETIQUETAS_CUMPLIMIENTO_DIA'],
    name = 'Total',
    marker = {'color': '#23c052'},
    mode = "lines",
    hoverinfo="x+text+name"
    )

    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(autorange=True, title = '', showgrid = False, showline = False, showticklabels = True),
    margin = {'l': 30, 'b': 200, 't': 0, 'r': 20},
    showlegend = True
    )

    data = Data([trace1, trace2, trace3])


    return Figure(data=data, layout=layout)

#--------------------------- GRAPH 3 "CUMPLIMIENTO MES"

@app.callback(
    dash.dependencies.Output('graph-3', 'figure'),
    [dash.dependencies.Input('sgro-drop', 'value'),
    dash.dependencies.Input('loc-drop', 'value'),
    dash.dependencies.Input('dir-drop', 'value')])
def update_figure(selected_sgro, selected_loc, selected_dir):

    base_filtro = baseMes
    base_filtro1 = base_filtro[(base_filtro['PRODUCTO'] == selected_sgro)&(base_filtro['LOCALIDAD'] == selected_loc)]
    base_filtro2 = base_filtro1[base_filtro1['DIRECTOR_VENTAS'] == selected_dir]
    base_filtro2['FECHA'] = pd.to_datetime(base_filtro2['FECHA'], format='%d/%m/%Y', errors='coerce')
    base_filtro2['MES'] = base_filtro2['FECHA'].dt.month
    base_filtro2['MES'] = base_filtro2['MES'].apply(lambda x:calendar.month_abbr[x])
    base_filtro2['CUMPLIMIENTO_TOTAL2']=base_filtro2['CUMPLIMIENTO_TOTAL']*100
    base_filtro2['CUMPLIMIENTO_TOTAL2']=base_filtro2['CUMPLIMIENTO_TOTAL2'].astype(int)
    base_filtro2['CUMPLIMIENTO_TOTAL2']=base_filtro2['CUMPLIMIENTO_TOTAL2'].astype(str)
    base_filtro2['CUMPLIMIENTO_TOTAL2'] = base_filtro2['CUMPLIMIENTO_TOTAL2']+'%'

    if base_filtro2['CUMPLIMIENTO_TOTAL2'].empty == True:
        min_trace3=0
        max_trace3=1
    else:
        min_cumplimiento_total=min(base_filtro2['CUMPLIMIENTO_TOTAL'])
        max_cumplimiento_total=max(base_filtro2['CUMPLIMIENTO_TOTAL'])
        min_trace3=float(min_cumplimiento_total)-float(0.1)
        max_trace3=float(max_cumplimiento_total)+float(0.3)

    trace1 = Scatter(
    x = base_filtro2['MES'],
    y = base_filtro2['CUMPLIMIENTO_TOTAL'],
    text = base_filtro2['CUMPLIMIENTO_TOTAL2'],
    textposition='top',
    textfont=dict(
        family='Helvetica',
        size=14,
        color='#1D5BBF'
    ),
    name = 'Director',
    marker = {'color': '#3381ff'},
    mode = "lines+text",
    hoverinfo="text"
    )


    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(
        range=[min_trace3, max_trace3],
        title = '', showgrid = False, showline = False, showticklabels = False),
    margin = {'l': 20, 'b': 200, 't': 0, 'r': 20},
    showlegend = False
    )

    data = Data([trace1])


    return Figure(data=data, layout=layout)

#-------------------------------------------PAGE 2

#--------------------------- DATABASES IMPORTS AND ADJUSTMENTS

base2 = pd.read_csv('https://raw.githubusercontent.com/Bancaseguros/DashboardCumplimiento/master/INFORME_INFORMADOR_DIARIO.csv', delimiter = '|', encoding='latin-1')
del base2['CODIGO_DIRECTOR_VENTAS']
base2=base2.drop_duplicates()
base2=base2.sort_values(['FECHA', 'DIRECTOR_VENTAS', 'NOMBRE_INFORMADOR_VENTAS'], ascending=[True, True, True])

base2['DIRECTOR_VENTAS']=base2['DIRECTOR_VENTAS'].str.upper()
base2['NOMBRE_INFORMADOR_VENTAS']=base2['NOMBRE_INFORMADOR_VENTAS'].str.upper()

base2['FECHA'] = pd.to_datetime(base2['FECHA'], format='%d/%m/%Y', errors='coerce')
base2['FECHA2'] = pd.to_datetime(base2['FECHA'], format="%Y%m") + MonthEnd(0)

options_dir2 = base2['DIRECTOR_VENTAS'].unique()
options_inf = base2['NOMBRE_INFORMADOR_VENTAS'].unique()

baseMes2 = pd.read_csv('https://raw.githubusercontent.com/Bancaseguros/DashboardCumplimiento/master/INFORME_INFORMADOR_MENSUAL.csv', delimiter = '|', encoding='latin-1')

baseMes2['DIRECTOR_VENTAS']=baseMes2['DIRECTOR_VENTAS'].str.upper()
baseMes2['NOMBRE_INFORMADOR_VENTAS']=baseMes2['NOMBRE_INFORMADOR_VENTAS'].str.upper()

#---------------------------------------------------------PAGE 2

#--------------------------- APP LAYOUT (HTML + DCC)

page_2_layout = html.Div(style = {'font-family': 'Helvetica', 'height': '100%', 'background-color': '#ffffff', 'margin': '-8px', 'overflow': 'hidden'}, children =[
    html.Div(style = {'width': '30%', 'height': '100vh', 'background-color': '#275968', 'margin': '0px', 'float': 'left', 'box-shadow': '4px 5px 9px -3px rgba(102,102,102,1)'}, children =[
        html.Div(style = {'max-width': '100%','margin': 'auto', 'padding-left': '25px', 'padding-top': '20px'}, children=[
            html.H1(style = {'font-family': 'Helvetica', 'font-size': '28', 'color': '#ffffff'},children='Dashboard Director+Informador')
        ]),
        html.Div(style = {'padding-left': '15px', 'padding-right': '15px', 'padding-top': '20px', 'font-size': '13'}, children = [
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '16'}, children = 'Seleccione director:'),
            dcc.Dropdown(
                id ='dir2-drop',
                options = [{'label': i, 'value': i} for i in options_dir2],
                ),
            html.Br(),
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '16'}, children = 'Seleccione informador:'),
            dcc.Dropdown(
                id ='inf-drop',
                options = [{'label': i, 'value': i} for i in options_inf]
                )
            ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.A(html.Button('Ir a Dashboard Director+Asesor', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-3'),
        html.A(html.Button('Ir a Dashboard Localidad+Director', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D','border-color':'#A8CECE', 'margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-1'),
        html.Br(),
        html.A(html.Button('Ir a Ranking Localidad', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D','border-color':'#A8CECE', 'margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-4'),
        html.A(html.Button('Ir a Ranking Director', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D','border-color':'#A8CECE', 'margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-5'),
        html.Br(),
        html.A(html.Button('Ir al Inicio', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D','border-color':'#A8CECE', 'margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/')
        ]),
    html.Div(style = {'width': '70%', 'height': '100%', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '30px', 'padding-bottom': '5px'}, children =[
        html.Div(style = {'width': '100%', 'height': '320px', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '30px'}, children = [
            html.Div(style = {'width': '50%', 'height': '100%', 'margin': '0px', 'float': 'left'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Recaudo primas Acumulado ($)'),
                dcc.Graph(id ='graph-1b', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ]),
            html.Div(style = {'width': '50%', 'height': '100%', 'margin': '0px', 'float': 'left'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Recaudo primas DÃ­a ($)'),
                dcc.Graph(id ='graph-2b', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ])
        ]),
        html.Div(style = {'width': '100%', 'height': '320px', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '20px'}, children = [
            html.Div(style = {'width': '100%', 'height': '100%', 'margin': '0px', 'float': 'left'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Recaudo primas mensual ($M)'),
                dcc.Graph(id ='graph-3b', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ])
        ])
    ])
])

#---------------------------------------------------------

#--------------------------- DEPENDENT DROPDOWNS CALLBACKS

@app.callback(
    dash.dependencies.Output('inf-drop', 'options'),
    [dash.dependencies.Input('dir2-drop', 'value')])
def set_inform_options(selected_dir2):
    filtrob = base2[base2['DIRECTOR_VENTAS'] == selected_dir2]
    return [{'label': i, 'value': i} for i in filtrob['NOMBRE_INFORMADOR_VENTAS'].unique()]

@app.callback(
    dash.dependencies.Output('inf-drop', 'value'),
    [dash.dependencies.Input('dir2-drop', 'options')])
def set_inform_value(available_options):
    return available_options[0]['value']


#---------------------------------------------------------

#--------------------------- GRAPH 1 "CUMPLIMIENTO DIARIO ACUMULADO"

@app.callback(
    dash.dependencies.Output('graph-1b', 'figure'),
    [dash.dependencies.Input('dir2-drop', 'value'),
    dash.dependencies.Input('inf-drop', 'value')])
def update_figure(selected_dir2, selected_inf):


    base_filtrob = base2
    base_filtrob1 = base_filtrob[base_filtrob['DIRECTOR_VENTAS'] == selected_dir2]
    base_filtrob2 = base_filtrob1[base_filtrob1['NOMBRE_INFORMADOR_VENTAS'] == selected_inf]

    base_filtrob2.reset_index()

    base_filtrob1_todos=base_filtrob1[base_filtrob1['NOMBRE_INFORMADOR_VENTAS']=='(TODOS)']

    base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtrob1_todos['CUMPLIMIENTO_ACUMULADO']
    base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=round(base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']*100,1)
    base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO'].astype(str)
    base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']+'%'

    base_filtrob2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=round(base_filtrob2['CUMPLIMIENTO_ACUMULADO']*100,1)
    base_filtrob2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtrob2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO'].astype(str)
    base_filtrob2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']=base_filtrob2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO']+'%'

    base_filtrob2['ETIQUETAS_OBJETIVO']=round((base_filtrob2['FECHA'].dt.day/base_filtrob2['FECHA2'].dt.day)*100,1)
    base_filtrob2['ETIQUETAS_OBJETIVO']=base_filtrob2['ETIQUETAS_OBJETIVO'].astype(str)
    base_filtrob2['ETIQUETAS_OBJETIVO']=base_filtrob2['ETIQUETAS_OBJETIVO']+'%'


    trace1 = Scatter(
    x = base_filtrob2['FECHA'],
    y = base_filtrob2['CUMPLIMIENTO_ACUMULADO']*100,
    text = base_filtrob2['ETIQUETAS_CUMPLIMIENTO_ACUMULADO'],
    name = 'Informador',
    marker = {'color': '#3381ff'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    trace2 = Scatter(
    x = base_filtrob2['FECHA'],
    y = (base_filtrob2['FECHA'].dt.day/base_filtrob2['FECHA2'].dt.day)*100,
    text = base_filtrob2['ETIQUETAS_OBJETIVO'],
    name = 'Objetivo',
    marker = {'color': '#ff5733'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    trace3 = Scatter(
    x = base_filtrob2['FECHA'],
    y = base_filtrob1['CUMPLIMIENTO_ACUMULADO'][base_filtrob1['NOMBRE_INFORMADOR_VENTAS']=='(TODOS)']*100,
    text = base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_ACUMULADO'],
    name = 'Total',
    marker = {'color': '#23c052'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(autorange=True, title = '', showgrid = False, showline = False, showticklabels = True),
    margin = {'l': 30, 'b': 200, 't': 0, 'r': 20},
    showlegend = True
    )

    data = Data([trace1, trace2, trace3])


    return Figure(data=data, layout=layout)

#--------------------------- GRAPH 2 "CUMPLIMIENTO DIARIO"

@app.callback(
    dash.dependencies.Output('graph-2b', 'figure'),
    [dash.dependencies.Input('dir2-drop', 'value'),
    dash.dependencies.Input('inf-drop', 'value')])
def update_figure(selected_dir2, selected_inf):

    base_filtrob = base2
    base_filtrob1 = base_filtrob[base_filtrob['DIRECTOR_VENTAS'] == selected_dir2]
    base_filtrob2 = base_filtrob1[base_filtrob1['NOMBRE_INFORMADOR_VENTAS'] == selected_inf]

    base_filtrob1_todos=base_filtrob1[base_filtrob1['NOMBRE_INFORMADOR_VENTAS']=='(TODOS)']

    base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtrob1_todos['CUMPLIMIENTO_DIA']
    base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']=round(base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']*100,1)
    base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_DIA'].astype(str)
    base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_DIA']+'%'

    base_filtrob2['ETIQUETAS_CUMPLIMIENTO_DIA']=round(base_filtrob2['CUMPLIMIENTO_DIA']*100,1)
    base_filtrob2['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtrob2['ETIQUETAS_CUMPLIMIENTO_DIA'].astype(str)
    base_filtrob2['ETIQUETAS_CUMPLIMIENTO_DIA']=base_filtrob2['ETIQUETAS_CUMPLIMIENTO_DIA']+'%'

    base_filtrob2['ETIQUETAS_OBJETIVO']=np.repeat(5.0,len(base_filtrob2['FECHA']))
    base_filtrob2['ETIQUETAS_OBJETIVO']=base_filtrob2['ETIQUETAS_OBJETIVO'].astype(str)
    base_filtrob2['ETIQUETAS_OBJETIVO']=base_filtrob2['ETIQUETAS_OBJETIVO']+'%'

    trace1 = Scatter(
    x = base_filtrob2['FECHA'],
    y = base_filtrob2['CUMPLIMIENTO_DIA']*100,
    text = base_filtrob2['ETIQUETAS_CUMPLIMIENTO_DIA'],
    name = 'Informador',
    marker = {'color': '#3381ff'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    trace2 = Scatter(
    x = base_filtrob2['FECHA'],
    y = np.repeat(0.05,len(base_filtrob2['FECHA']))*100,
    text = base_filtrob2['ETIQUETAS_OBJETIVO'],
    name = 'Objetivo',
    marker = {'color': '#ff5733'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    trace3 = Scatter(
    x = base_filtrob2['FECHA'],
    y = base_filtrob1['CUMPLIMIENTO_DIA'][base_filtrob1['NOMBRE_INFORMADOR_VENTAS']=='(TODOS)']*100,
    text = base_filtrob1_todos['ETIQUETAS_CUMPLIMIENTO_DIA'],
    name = 'Total',
    marker = {'color': '#23c052'},
    mode = "lines",
    hoverinfo="x+name+text"
    )

    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(autorange=True, title = '', showgrid = False, showline = False, showticklabels = True),
    margin = {'l': 20, 'b': 200, 't': 0, 'r': 20},
    showlegend = True
    )

    data = Data([trace1, trace2, trace3])


    return Figure(data=data, layout=layout)

#--------------------------- GRAPH 3 "RECAUDO MES"

@app.callback(
    dash.dependencies.Output('graph-3b', 'figure'),
    [dash.dependencies.Input('dir2-drop', 'value'),
    dash.dependencies.Input('inf-drop', 'value')])
def update_figure(selected_dir2, selected_inf):

    base_filtroc = baseMes2
    base_filtroc1 = base_filtroc[base_filtroc['DIRECTOR_VENTAS'] == selected_dir2]
    base_filtroc2 = base_filtroc1[base_filtroc1['NOMBRE_INFORMADOR_VENTAS'] == selected_inf]

    base_filtroc2['FECHA'] = pd.to_datetime(base_filtroc2['FECHA'],format='%d/%m/%Y', errors='coerce')
    base_filtroc2['MES'] = base_filtroc2['FECHA'].dt.month
    base_filtroc2['MES'] = base_filtroc2['MES'].apply(lambda x:calendar.month_abbr[x])
    base_filtroc2['ETIQUETAS_CUMPLIMIENTO']=base_filtroc2['CUMPLIMIENTO_ACUMULADO']*100
    base_filtroc2['ETIQUETAS_CUMPLIMIENTO']=base_filtroc2['ETIQUETAS_CUMPLIMIENTO'].astype(int)
    base_filtroc2['ETIQUETAS_CUMPLIMIENTO']=base_filtroc2['ETIQUETAS_CUMPLIMIENTO'].astype(str)
    base_filtroc2['ETIQUETAS_CUMPLIMIENTO']=base_filtroc2['ETIQUETAS_CUMPLIMIENTO']+'%'

    if base_filtroc2['CUMPLIMIENTO_ACUMULADO'].empty == True:
        min_trace3=0
        max_trace3=1
    else:
        min_cumplimiento_total=min(base_filtroc2['CUMPLIMIENTO_ACUMULADO'])
        max_cumplimiento_total=max(base_filtroc2['CUMPLIMIENTO_ACUMULADO'])
        min_trace3=float(min_cumplimiento_total)-float(0.1)
        max_trace3=float(max_cumplimiento_total)+float(0.3)

    trace1 = Scatter(
    x = base_filtroc2['MES'],
    y = base_filtroc2['CUMPLIMIENTO_ACUMULADO'],
    text = base_filtroc2['ETIQUETAS_CUMPLIMIENTO'],
    name = 'Informador',
    marker = {'color': '#3381ff'},
    mode = "lines+text",
    textposition='top',
    textfont=dict(
        family='Helvetica',
        size=14,
        color='#1D5BBF'
    ),
    hoverinfo="text"
    )


    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(range=[min_trace3, max_trace3],
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False),
    margin = {'l': 20, 'b': 200, 't': 0, 'r': 20},
    showlegend = False
    )

    data = Data([trace1])


    return Figure(data=data, layout=layout)


#-------------------------------------------PAGE 3
#--------------------------- DATABASES IMPORTS AND ADJUSTMENTS

base3 = pd.read_csv('https://raw.githubusercontent.com/Bancaseguros/DashboardCumplimiento/master/INFORME_ASESOR_DIARIO.csv', delimiter = '|', encoding='latin-1', low_memory=False)
del base3['CODIGO_DIRECTOR_VENTAS']
base3=base3.drop_duplicates()
base3=base3.sort_values(['FECHA', 'DIRECTOR_VENTAS', 'NOMBRE_ASESOR_VENTAS'], ascending=[True, True, True])
base3['FECHA'] = pd.to_datetime(base3['FECHA'], format='%d/%m/%Y', errors='coerce')

base3['DIRECTOR_VENTAS']=base3['DIRECTOR_VENTAS'].str.upper()
base3['NOMBRE_ASESOR_VENTAS']=base3['NOMBRE_ASESOR_VENTAS'].str.upper()

options_dir3 = base3['DIRECTOR_VENTAS'].unique()
options_ase = base3['NOMBRE_ASESOR_VENTAS'].unique()

baseMes3 = pd.read_csv('https://raw.githubusercontent.com/Bancaseguros/DashboardCumplimiento/master/INFORME_ASESOR_MENSUAL.csv', delimiter = '|', encoding='latin-1', low_memory=False)

baseMes3['DIRECTOR_VENTAS']=baseMes3['DIRECTOR_VENTAS'].str.upper()
baseMes3['NOMBRE_ASESOR_VENTAS']=baseMes3['NOMBRE_ASESOR_VENTAS'].str.upper()

#---------------------------------------------------------PAGE 3

#--------------------------- APP LAYOUT (HTML + DCC)

page_3_layout = html.Div(style = {'font-family': 'Helvetica','height': '100%', 'background-color': '#ffffff', 'margin': '-8px', 'overflow': 'hidden'}, children =[
    html.Div(style = {'width': '30%', 'height': '100vh', 'background-color': '#275968', 'margin': '0px', 'float': 'left', 'box-shadow': '4px 5px 9px -3px rgba(102,102,102,1)'}, children =[
        html.Div(style = {'max-width': '100%','margin': 'auto', 'padding-left': '25px', 'padding-top': '20px'}, children=[
            html.H1(style = {'font-family': 'Helvetica', 'font-size': '28', 'color': '#ffffff'},children='Dashboard Director+Asesor')
        ]),
        html.Div(style = {'padding-left': '15px', 'padding-right': '15px', 'padding-top': '20px', 'font-size': '13'}, children = [
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '16'}, children = 'Seleccione director:'),
            dcc.Dropdown(
                id ='dir3-drop',
                options = [{'label': i, 'value': i} for i in options_dir3],
                ),
            html.Br(),
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '16'}, children = 'Seleccione asesor:'),
            dcc.Dropdown(
                id ='ase-drop'
                )
            ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.A(html.Button('Ir a Dashboard Localidad+Director', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-1'),
        html.A(html.Button('Ir a Dashboard Director+Informador', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-2'),
            html.Br(),
        html.A(html.Button('Ir a Ranking Localidad', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-4'),
        html.A(html.Button('Ir a Ranking Director', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-5'),
        html.Br(),
        html.A(html.Button('Ir al Inicio', className='btn btn-primary btn-block',style = {'font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'height': '6vh', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/')
        ]),
    html.Div(style = {'width': '70%', 'height': '100%', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '30px', 'padding-bottom': '5px'}, children =[
        html.Div(style = {'width': '100%', 'height': '320px', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '30px'}, children = [
            html.Div(style = {'width': '50%', 'height': '100%', 'margin': '0px', 'float': 'left'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Recaudo primas acumulado ($)'),
                dcc.Graph(id ='graph-1c', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ]),
            html.Div(style = {'width': '50%', 'height': '100%', 'margin': '0px', 'float': 'left'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Recaudo primas DÃ­a ($)'),
                dcc.Graph(id ='graph-2c', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ])
        ]),
        html.Div(style = {'width': '100%', 'height': '320px', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '20px'}, children = [
            html.Div(style = {'width': '100%', 'height': '100%', 'margin': '0px', 'float': 'left'}, children = [
                html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Recaudo primas mensual ($M)'),
                dcc.Graph(id ='graph-3c', animate = False, style = {'height': '350px', 'width': '95%', 'margin': 'auto'}, config = {'displayModeBar': False})
            ])
        ])
    ])
])

#---------------------------------------------------------

#--------------------------- DEPENDENT DROPDOWNS CALLBACKS

@app.callback(
    dash.dependencies.Output('ase-drop', 'options'),
    [dash.dependencies.Input('dir3-drop', 'value')])
def set_asesor_options(selected_dir3):
    filtroc = base3[base3['DIRECTOR_VENTAS'] == selected_dir3]
    return [{'label': i, 'value': i} for i in filtroc['NOMBRE_ASESOR_VENTAS'].unique()]

@app.callback(
    dash.dependencies.Output('ase-drop', 'value'),
    [dash.dependencies.Input('dir3-drop', 'options')])
def set_asesor_value(available_options):
    return available_options[0]['value']

#---------------------------------------------------------

#--------------------------- GRAPH 1 "CUMPLIMIENTO DIARIO ACUMULADO"

@app.callback(
    dash.dependencies.Output('graph-1c', 'figure'),
    [dash.dependencies.Input('dir3-drop', 'value'),
    dash.dependencies.Input('ase-drop', 'value')])
def update_figure(selected_dir3, selected_ase):


    base_filtroc = base3
    base_filtroc1 = base_filtroc[base_filtroc['DIRECTOR_VENTAS'] == selected_dir3]
    base_filtroc2 = base_filtroc1[base_filtroc1['NOMBRE_ASESOR_VENTAS'] == selected_ase]


    trace1 = Scatter(
    x = base_filtroc2['FECHA'],
    y = round(base_filtroc2['RECAUDO_ACUMULADO'],1),
    text = 'Asesor',
    name = 'Asesor',
    marker = {'color': '#3381ff'},
    mode = "lines",
    hoverinfo="x+y"
    )

    trace2 = Scatter(
    x = base_filtroc2['FECHA'],
    y = base_filtroc1['RECAUDO_ACUMULADO'][base_filtroc1['NOMBRE_ASESOR_VENTAS']=='(TODOS)'],
    text = 'Total',
    name = 'Total',
    marker = {'color': '#23c052'},
    mode = "lines",
    hoverinfo="x+y"
    )

    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(autorange=True, title = '', showgrid = False, showline = False, showticklabels = True),
    margin = {'l': 20, 'b': 200, 't': 0, 'r': 20},
    showlegend = True
    )

    data = Data([trace1, trace2])


    return Figure(data=data, layout=layout)

#--------------------------- GRAPH 2 "CUMPLIMIENTO DIARIO"

@app.callback(
    dash.dependencies.Output('graph-2c', 'figure'),
    [dash.dependencies.Input('dir3-drop', 'value'),
    dash.dependencies.Input('ase-drop', 'value')])
def update_figure(selected_dir3, selected_ase):


    base_filtroc = base3
    base_filtroc1 = base_filtroc[base_filtroc['DIRECTOR_VENTAS'] == selected_dir3]
    base_filtroc2 = base_filtroc1[base_filtroc1['NOMBRE_ASESOR_VENTAS'] == selected_ase]


    trace1 = Scatter(
    x = base_filtroc2['FECHA'],
    y = round(base_filtroc2['RECAUDO_DIA'],1),
    text = 'Asesor',
    name = 'Asesor',
    marker = {'color': '#3381ff'},
    mode = "lines",
    hoverinfo="x+y"
    )

    trace2 = Scatter(
    x = base_filtroc2['FECHA'],
    y = base_filtroc1['RECAUDO_DIA'][base_filtroc1['NOMBRE_ASESOR_VENTAS']=='(TODOS)'],
    text = 'Total',
    name = 'Total',
    marker = {'color': '#23c052'},
    mode = "lines",
    hoverinfo="x+y"
    )

    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(autorange=True, title = '', showgrid = False, showline = False, showticklabels = True),
    margin = {'l': 20, 'b': 200, 't': 0, 'r': 20},
    showlegend = True
    )

    data = Data([trace1, trace2])


    return Figure(data=data, layout=layout)

#--------------------------- GRAPH 3 "RECAUDO MES"

@app.callback(
    dash.dependencies.Output('graph-3c', 'figure'),
    [dash.dependencies.Input('dir3-drop', 'value'),
    dash.dependencies.Input('ase-drop', 'value')])
def update_figure(selected_dir3, selected_ase):


    base_filtroc = baseMes3
    base_filtroc1 = base_filtroc[base_filtroc['DIRECTOR_VENTAS'] == selected_dir3]
    base_filtroc2 = base_filtroc1[base_filtroc1['NOMBRE_ASESOR_VENTAS'] == selected_ase]

    base_filtroc2['FECHA'] = pd.to_datetime(base_filtroc2['FECHA'])
    base_filtroc2['MES'] = base_filtroc2['FECHA'].dt.month
    base_filtroc2['MES'] = base_filtroc2['MES'].apply(lambda x:calendar.month_abbr[x])
    base_filtroc2['ETIQUETAS_RECAUDO']=round(base_filtroc2['RECAUDO']/1000000,1)
    base_filtroc2['ETIQUETAS_RECAUDO']=base_filtroc2['ETIQUETAS_RECAUDO'].astype(str)
    base_filtroc2['ETIQUETAS_RECAUDO']='$'+base_filtroc2['ETIQUETAS_RECAUDO']+'M'

    if base_filtroc2['RECAUDO'].empty == True:
        min_trace3=0
        max_trace3=1
    else:
        min_cumplimiento_total=min(base_filtroc2['RECAUDO'])
        max_cumplimiento_total=max(base_filtroc2['RECAUDO'])
        min_trace3=float(min_cumplimiento_total)-1000000
        max_trace3=float(max_cumplimiento_total)+2000000

    trace1 = Scatter(
    x = base_filtroc2['MES'],
    y = base_filtroc2['RECAUDO'],
    text = base_filtroc2['ETIQUETAS_RECAUDO'],
    name = 'Asesor',
    marker = {'color': '#3381ff'},
    mode = "lines+text",
    textposition='top',
    textfont=dict(
        family='Helvetica',
        size=14,
        color='#1D5BBF'
    ),
    hoverinfo="text"
    )


    layout = Layout(
    title = '',
    titlefont = {'family': 'Helvetica', 'size': '16', 'color': '#7f7f7f'},
    xaxis = dict(title = '', showgrid = False),
    yaxis = dict(range=[min_trace3, max_trace3],
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False),
    margin = {'l': 20, 'b': 200, 't': 0, 'r': 20},
    showlegend = False
    )

    data = Data([trace1])


    return Figure(data=data, layout=layout)

#---------------------------------------------------------PAGE 4

baseMes['FECHA'] = pd.to_datetime(baseMes['FECHA'], format='%d/%m/%Y', errors='coerce')
fechaMax=baseMes['FECHA'].max()
baseMes['PRODUCTO2']='  '+baseMes['PRODUCTO']
baseFiltro=baseMes[['FECHA', 'LOCALIDAD','PRODUCTO2', 'CUMPLIMIENTO_TOTAL']][(baseMes['FECHA']==fechaMax)&(baseMes['PRODUCTO2']=='  DAVIDA')&(baseMes['DIRECTOR_VENTAS']=='(TODOS)')].sort_values('CUMPLIMIENTO_TOTAL', ascending=False)
baseFiltro.reset_index(inplace=True)
baseFiltro['POSICION'] = baseFiltro.index
baseFiltro['POSICION']=baseFiltro['POSICION']+1
baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series([round(val, 2) for val in baseFiltro['CUMPLIMIENTO_TOTAL']])
baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series(["{0:.0f}%".format(val * 100) for val in baseFiltro['CUMPLIMIENTO TOTAL']])
baseFiltro['LOCALIDAD']=baseFiltro['LOCALIDAD'].str.replace("A.C.E.","")
baseFiltro=baseFiltro[['POSICION', 'LOCALIDAD', 'CUMPLIMIENTO TOTAL']]
#basePeor=baseFiltro
#baseMejor=baseFiltro.head(n=10)
#basePeor=basePeor.tail(n=10)
#basePeor=basePeor.sort_values('POSICION',ascending=False)

options_sgro2 = baseMes['PRODUCTO2'].unique()

Tabla1=ff.create_table(baseFiltro)
for i in range(len(Tabla1.layout.annotations)):
        Tabla1.layout.annotations[i].font.size=11

#Tabla1=ff.create_table(baseMejor)

#Tabla2=ff.create_table(basePeor)

page_4_layout = html.Div(style = {'font-family': 'Helvetica','height': '100%','background-color': '#ffffff', 'margin': '-8px', 'overflow': 'hidden'}, children =[
    html.Div(style = {'width': '20%', 'height':'1000px', 'color': '#ffffff', 'background-color': '#275968', 'margin': '0px', 'float': 'left', 'box-shadow': '4px 5px 9px -3px rgba(102,102,102,1)'}, children =[
        html.Div(style = {'max-width': '100%','margin': 'auto', 'padding-left': '25px', 'padding-top': '20px'}, children=[
            html.H1(style = {'font-family': 'Helvetica', 'font-size': '28', 'color': '#ffffff'},children='Ranking Localidades')
        ]),
        html.Div(style = {'padding-left': '20px', 'padding-top': '20px', 'font-size': '12'}, children = [
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '16'}, children = 'Seleccione tipo seguro:'),
            dcc.RadioItems(
                id ='sgro-drop', className='w3-radio',
                options = [{'label': i, 'value': i} for i in options_sgro2],
                value='  DAVIDA',
                labelStyle={'display': 'block', 'font-size': '12'}
            ),
        ]),
        html.Br(),
        html.A(html.Button('Ir a Dashboard Localidad+Director', className='btn btn-primary',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-1'),
        html.A(html.Button('Ir a Dashboard Director+Informador', className='btn btn-primary btn-block',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-2'),
        html.A(html.Button('Ir a Dashboard Director+Asesor', className='btn btn-primary btn-block',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-3'),
        html.Br(),
        html.A(html.Button('Ir a Ranking Director', className='btn btn-primary btn-block',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-5'),
        html.Br(),
        html.A(html.Button('Ir al Inicio', className='btn btn-primary btn-block',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/')
    ]),
    html.Div(style = {'width': '80%', 'height': '100%', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '35px', 'padding-bottom': '5px', 'font-family': 'Helvetica', 'font-size': '13'}, children =[
        html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Ranking Localidades por %Cumplimiento'),
        html.Div(style = {'padding-bottom': '5px', 'font-family': 'Helvetica', 'font-size': '13'}, children =[
            dcc.Graph(id ='table-1', figure=Tabla1, style = {'width': '95%', 'margin': 'auto', 'display':'block', 'font-family': 'Helvetica', 'font-size': '13'}),
        ])
        #,html.Br(),
        #html.Br(),
        #html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Top 10 Peores Localidades por %Cumplimiento'),
        #dcc.Graph(id ='table-2', figure=Tabla2, style = {'width': '95%', 'margin': 'auto', 'display':'block', 'font-family': 'Helvetica', 'font-size': '13'})
    ])
])

@app.callback(
    dash.dependencies.Output('table-1', 'figure'),
    [dash.dependencies.Input('sgro-drop', 'value')])
def update_figure(selected_sgro):

    baseMes['FECHA'] = pd.to_datetime(baseMes['FECHA'], format='%d/%m/%Y', errors='coerce')
    fechaMax=baseMes['FECHA'].max()
    baseFiltro=baseMes[['FECHA', 'LOCALIDAD', 'PRODUCTO2', 'CUMPLIMIENTO_TOTAL']][(baseMes['FECHA']==fechaMax)&(baseMes['PRODUCTO2']==selected_sgro)&(baseMes['DIRECTOR_VENTAS']=='(TODOS)')].sort_values('CUMPLIMIENTO_TOTAL', ascending=False)
    baseFiltro.reset_index(inplace=True)
    baseFiltro['POSICION'] = baseFiltro.index
    baseFiltro['POSICION']=baseFiltro['POSICION']+1
    baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series([round(val, 2) for val in baseFiltro['CUMPLIMIENTO_TOTAL']])
    baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series(["{0:.0f}%".format(val * 100) for val in baseFiltro['CUMPLIMIENTO TOTAL']])
    baseFiltro['LOCALIDAD']=baseFiltro['LOCALIDAD'].str.replace("A.C.E.","")
    baseFiltro=baseFiltro[['POSICION', 'LOCALIDAD', 'CUMPLIMIENTO TOTAL']]
    #basePeor=baseFiltro
    #baseMejor=baseFiltro.head(n=10)
    #basePeor=basePeor.tail(n=10)
    #basePeor=basePeor.sort_values('POSICION',ascending=False)

    Tabla1=ff.create_table(baseFiltro)
    #Tabla1=ff.create_table(baseMejor)
    for i in range(len(Tabla1.layout.annotations)):
        Tabla1.layout.annotations[i].font.size=11

    return Tabla1

'''
@app.callback(
    dash.dependencies.Output('table-2', 'figure'),
    [dash.dependencies.Input('sgro-drop', 'value')])
def update_figure(selected_sgro):

    baseMes['FECHA'] = pd.to_datetime(baseMes['FECHA'], format='%d/%m/%Y', errors='coerce')
    fechaMax=baseMes['FECHA'].max()
    baseFiltro=baseMes[['FECHA', 'LOCALIDAD', 'PRODUCTO2', 'CUMPLIMIENTO_TOTAL']][(baseMes['FECHA']==fechaMax)&(baseMes['PRODUCTO2']==selected_sgro)&(baseMes['DIRECTOR_VENTAS']=='(Todos)')].sort_values('CUMPLIMIENTO_TOTAL', ascending=False)
    baseFiltro.reset_index(inplace=True)
    baseFiltro['POSICION'] = baseFiltro.index
    baseFiltro['POSICION']=baseFiltro['POSICION']+1
    baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series([round(val, 2) for val in baseFiltro['CUMPLIMIENTO_TOTAL']])
    baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series(["{0:.0f}%".format(val * 100) for val in baseFiltro['CUMPLIMIENTO TOTAL']])
    baseFiltro=baseFiltro[['POSICION', 'LOCALIDAD', 'CUMPLIMIENTO TOTAL']]
    basePeor=baseFiltro
    baseMejor=baseFiltro.head(n=10)
    basePeor=basePeor.tail(n=10)
    basePeor=basePeor.sort_values('POSICION',ascending=False)

    Tabla2=ff.create_table(basePeor)

    return Tabla2
'''
#---------------------------------------------------------PAGE 5
baseMes['FECHA'] = pd.to_datetime(baseMes['FECHA'], format='%d/%m/%Y', errors='coerce')
fechaMax=baseMes['FECHA'].max()
baseMes['PRODUCTO2']='  '+baseMes['PRODUCTO']
baseFiltro=baseMes[['FECHA', 'DIRECTOR_VENTAS', 'LOCALIDAD', 'PRODUCTO2', 'CUMPLIMIENTO_TOTAL']][(baseMes['FECHA']==fechaMax)&(baseMes['PRODUCTO2']=='  DAVIDA')&(baseMes['DIRECTOR_VENTAS']!='(TODOS)')].sort_values('CUMPLIMIENTO_TOTAL', ascending=False)
baseFiltro.reset_index(inplace=True)
baseFiltro['POSICION'] = baseFiltro.index
baseFiltro['POSICION']=baseFiltro['POSICION']+1
baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series([round(val, 2) for val in baseFiltro['CUMPLIMIENTO_TOTAL']])
baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series(["{0:.0f}%".format(val * 100) for val in baseFiltro['CUMPLIMIENTO TOTAL']])
baseFiltro['LOCALIDAD']=baseFiltro['LOCALIDAD'].str.replace("A.C.E.","")
baseFiltro=baseFiltro[['POSICION', 'DIRECTOR_VENTAS', 'LOCALIDAD', 'CUMPLIMIENTO TOTAL']]
#basePeor=baseFiltro
#baseMejor=baseFiltro.head(n=10)
#basePeor=basePeor.tail(n=10)
#basePeor=basePeor.sort_values('POSICION',ascending=False)

options_sgro2 = baseMes['PRODUCTO2'].unique()

Tabla1b=ff.create_table(baseFiltro)

for i in range(len(Tabla1b.layout.annotations)):
        Tabla1b.layout.annotations[i].font.size=8
#Tabla1=ff.create_table(baseMejor)

#Tabla2=ff.create_table(basePeor)

page_5_layout = html.Div(style = {'font-family': 'Helvetica','height': '100%','background-color': '#ffffff', 'margin': '-8px', 'overflow': 'hidden'}, children =[
    html.Div(style = {'width': '20%', 'height':'1000px', 'overflow': 'hidden', 'color': '#ffffff', 'background-color': '#275968', 'margin': '0px', 'float': 'left', 'box-shadow': '4px 5px 9px -3px rgba(102,102,102,1)'}, children =[
        html.Div(style = {'max-width': '100%','margin': 'auto', 'padding-left': '25px', 'padding-top': '20px'}, children=[
            html.H1(style = {'font-family': 'Helvetica', 'font-size': '28', 'color': '#ffffff'},children='Ranking Directores')
        ]),
        html.Div(style = {'padding-left': '20px', 'padding-top': '20px', 'font-size': '12'}, children = [
            html.P(style = {'color': '#ffffff', 'font-family': 'Helvetica', 'font-size': '16'}, children = 'Seleccione tipo seguro:'),
            dcc.RadioItems(
                id ='sgro-drop', className='w3-radio',
                options = [{'label': i, 'value': i} for i in options_sgro2],
                value='  DAVIDA',
                labelStyle={'display': 'block', 'font-size': '12'}
            ),
        ]),
        html.Br(),
        html.A(html.Button('Ir a Dashboard Localidad+Director', className='btn btn-primary',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-1'),
        html.A(html.Button('Ir a Dashboard Director+Informador', className='btn btn-primary btn-block',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-2'),
        html.A(html.Button('Ir a Dashboard Director+Asesor', className='btn btn-primary btn-block',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-3'),
        html.Br(),
        html.A(html.Button('Ir a Ranking Localidad', className='btn btn-primary',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-4'),
        html.Br(),
        html.A(html.Button('Ir al Inicio', className='btn btn-primary btn-block',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '12', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/')
    ]),
    html.Div(style = {'width': '80%', 'height': '100%', 'margin': '0px', 'overflow': 'scroll', 'padding-top': '35px', 'padding-bottom': '5px', 'font-family': 'Helvetica', 'font-size': '13'}, children =[
        html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Ranking Directores por %Cumplimiento'),
        html.Div(style = {'padding-bottom': '5px', 'font-family': 'Helvetica', 'font-size': '13'}, children =[
            dcc.Graph(id ='table-1b', figure=Tabla1b, style = {'width': '95%', 'margin': 'auto', 'display':'block', 'font-family': 'Helvetica', 'font-size': '13'}),
        ])
        #,html.Br(),
        #html.Br(),
        #html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Top 10 Peores Localidades por %Cumplimiento'),
        #dcc.Graph(id ='table-2', figure=Tabla2, style = {'width': '95%', 'margin': 'auto', 'display':'block', 'font-family': 'Helvetica', 'font-size': '13'})
    ])
])

@app.callback(
    dash.dependencies.Output('table-1b', 'figure'),
    [dash.dependencies.Input('sgro-drop', 'value')])
def update_figure(selected_sgro):

    baseMes['FECHA'] = pd.to_datetime(baseMes['FECHA'], format='%d/%m/%Y', errors='coerce')
    fechaMax=baseMes['FECHA'].max()
    baseFiltro=baseMes[['FECHA', 'DIRECTOR_VENTAS', 'LOCALIDAD', 'PRODUCTO2', 'CUMPLIMIENTO_TOTAL']][(baseMes['FECHA']==fechaMax)&(baseMes['PRODUCTO2']==selected_sgro)&(baseMes['DIRECTOR_VENTAS']!='(TODOS)')].sort_values('CUMPLIMIENTO_TOTAL', ascending=False)
    baseFiltro.reset_index(inplace=True)
    baseFiltro['POSICION'] = baseFiltro.index
    baseFiltro['POSICION']=baseFiltro['POSICION']+1
    baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series([round(val, 2) for val in baseFiltro['CUMPLIMIENTO_TOTAL']])
    baseFiltro['CUMPLIMIENTO TOTAL'] = pd.Series(["{0:.0f}%".format(val * 100) for val in baseFiltro['CUMPLIMIENTO TOTAL']])
    baseFiltro['LOCALIDAD']=baseFiltro['LOCALIDAD'].str.replace("A.C.E.","")
    baseFiltro=baseFiltro[['POSICION', 'DIRECTOR_VENTAS', 'LOCALIDAD', 'CUMPLIMIENTO TOTAL']]
    #basePeor=baseFiltro
    #baseMejor=baseFiltro.head(n=10)
    #basePeor=basePeor.tail(n=10)
    #basePeor=basePeor.sort_values('POSICION',ascending=False)

    Tabla1b=ff.create_table(baseFiltro)
    #Tabla1=ff.create_table(baseMejor)
    for i in range(len(Tabla1b.layout.annotations)):
        Tabla1b.layout.annotations[i].font.size=8

    return Tabla1b

'''
baseMes3['FECHA'] = pd.to_datetime(baseMes3['FECHA'])
baseMes3['FECHA'] = baseMes3['FECHA'].dt.strftime('%d/%m/%Y')
fechaMax=baseMes3['FECHA'].max()
baseFiltro=baseMes3[['FECHA', 'DIRECTOR_VENTAS', 'RECAUDO']][(baseMes3['FECHA']==fechaMax)&(baseMes3['NOMBRE_ASESOR_VENTAS']=='(Todos)')].sort_values('RECAUDO', ascending=False)
baseFiltro.reset_index(inplace=True)
baseFiltro['POSICION'] = baseFiltro.index
baseFiltro['POSICION']=baseFiltro['POSICION']+1
baseFiltro['RECAUDO']=baseFiltro.apply(lambda x: "{:,}".format(x['RECAUDO']), axis=1)
baseFiltro['DIRECTOR VENTAS']=baseFiltro['DIRECTOR_VENTAS']
baseFiltro=baseFiltro[['POSICION', 'DIRECTOR VENTAS', 'RECAUDO']]
basePeor=baseFiltro
baseMejor=baseFiltro.head(n=10)
basePeor=basePeor.tail(n=10)
basePeor=basePeor.sort_values('POSICION',ascending=False)

Tabla1=ff.create_table(baseMejor)

Tabla2=ff.create_table(basePeor)

page_5_layout = html.Div(style = {'font-family': 'Helvetica','height': '100%','background-color': '#ffffff', 'margin': '-8px', 'overflow': 'hidden'}, children =[
    html.Div(style = {'width': '20%', 'height':'1000px', 'background-color': '#275968', 'margin': '0px', 'float': 'left', 'box-shadow': '4px 5px 9px -3px rgba(102,102,102,1)'}, children =[
        html.Div(style = {'max-width': '100%','margin': 'auto', 'padding-left': '25px', 'padding-top': '20px'}, children=[
            html.H1(style = {'font-family': 'Helvetica', 'font-size': '28', 'color': '#ffffff'},children='Ranking Directores')
        ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.A(html.Button('Ir a Dashboard Localidad+Director', className='btn btn-primary',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-1'),
        html.A(html.Button('Ir a Dashboard Director+Informador', className='btn btn-primary',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-2'),
        html.A(html.Button('Ir a Dashboard Director+Asesor', className='btn btn-primary',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-3'),
        html.Br(),
        html.A(html.Button('Ir a Ranking Localidad', className='btn btn-primary',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/page-4'),
        html.Br(),
        html.A(html.Button('Ir al Inicio', className='btn btn-primary',style = {'white-space': 'initial','overflow': 'visible','font-family': 'Helvetica', 'font-size': '14', 'width': '80%', 'background-color': '#068D8D', 'border-color':'#A8CECE','margin': 'auto', 'display':'block', 'box-shadow': '2px 2px 1px #A8CECE'}),
            href='/')
    ]),
    html.Div(style = {'width': '80%', 'height': '100%', 'margin': '0px', 'overflow': 'hidden', 'padding-top': '35px', 'padding-bottom': '5px'}, children =[
        html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Top 10 Mejores Directores por Recaudo Primas'),
        html.Div(style = {'padding-bottom': '5px', 'font-family': 'Helvetica', 'font-size': '13'}, children =[
            dcc.Graph(id ='table-1', figure=Tabla1,style = {'width': '95%', 'background-color': '#93c178', 'margin': 'auto', 'display':'block', 'font-family': 'Helvetica', 'font-size': '13'}),

        ]),
        html.Br(),
        html.Br(),
        html.P(style = {'color': '#7f7f7f', 'font-family': 'Helvetica', 'font-size': '17', 'text-align': 'center'}, children = 'Top 10 Peores Directores por Recaudo Primas'),
        dcc.Graph(id ='table-2', figure=Tabla2,style = {'width': '95%', 'background-color': '#93c178', 'margin': 'auto', 'display':'block'})
    ])
])
'''

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/page-5':
        return page_5_layout
    else:
        return index_page

#--------------------------- CSS STYLING FILE - URL DELETES UNDO-REDO BUTTON
app.css.append_css({
   'external_url': (
       'https://rawgit.com/lwileczek/Dash/master/undo_redo5.css'
   )
})
app.css.append_css({
   'external_url': (
       'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css'
   )
})

if __name__ == '__main__':
    app.run_server(debug=False, port=5000)
