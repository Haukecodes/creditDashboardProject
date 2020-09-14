import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from datetime import date

app = dash.Dash(__name__)

axisLogo = base64.b64encode(open(r'C:\Users\Connor.Rhodes\Desktop\axisLogo.png', 'rb').read())

#import spreadsheet into dataframe
df = pd.read_csv(r'C:\Users\Connor.Rhodes\Desktop\dashTestData.csv', index_col=0)

#Put CEDENT names into dictionary
def cedentDictionary(values):
    options = []
    repeats = []

    for elements in values:
        if elements in repeats:
            continue

        options.append({'label': str(elements), 'value': str(elements)})
        repeats.append(elements)

    return options

#Create graph from selected dataframe - function takes a dataframe and creates a graph from it. Dataframe parameter based on user-selection in dropdown menu
def showTable(data):
    table = df[selection]

#storing values of CEDENTS:
cedentList = df.columns.values.tolist()

print(cedentList, sep='\n')


app.layout = html.Div([

    html.Div([

        html.Div(

            children=[

                html.Div(html.Img(src='data:image/png;base64,{}'.format(axisLogo.decode())),
                         style={'textAlign': 'center'}),

                html.Div(

                    id='sidebar',

                    children=[

                        html.H4(
                            'Filters',
                            style={'margin-top': '75px', 'color': 'white'}
                        ),

                        html.Label('CEDENT NAME', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='cedentList',
                            options=cedentDictionary(cedentList),
                            value=[],
                            multi=True
                        ),


                        html.Div(html.Label('Date Range', style={'color': 'white'})),
                        dcc.DatePickerRange(
                            id='dateRange',
                            start_date='1990-01-01',
                            end_date=str(date.today()),
                            style={'margin-bottom': '50px'}
                        ),


                        html.Div(html.Button('Run Query', id='runQuery', n_clicks=0)),
                    ]
                )
            ], className='two columns'),

        html.Div([

            # Tabs for the plots and raw data
            dcc.Tabs([

                # Plots and Tables Tab
                dcc.Tab(label='Plots and Tables', children=[

                    html.Div(style={'margin-top': '10px'}),

                    dcc.Loading(children=[

                        html.Div(id='defaultGraphs', style={'display': 'none'}),

                        html.Div([

                            html.Div([

                                dcc.Graph(id='testGraph')

                            ], className='six columns'),

                            html.Div([

                                #dcc.Graph(id='donutCAT')

                            ], className='six columns')

                        ], className='row', style={'margin-bottom': '25px'}),

                        html.Div([

                            html.Div([

                                #dcc.Graph(id='donutLOB'),

                            ], className='six columns'),

                            html.Div([

                                #dcc.Graph(id='graph')

                            ], className='six columns')

                        ], className='row', style={'margin-bottom': '25px'}),

                        html.Div([

                            html.Div(
                                id='stateTable',
                                className='six columns'),

                            html.Div(
                                id='aggTable',
                                className='six columns')

                        ], className='row')
                    ])
                ]),

                # Raw Data Tab
                dcc.Tab(label='Raw Data', children=[

                    html.Div(style={'margin-top': '10px'}),

                    dcc.Loading(children=[

                        html.Div(id='table')

                    ])
                ])
            ],

                colors={
                    'border': 'white',
                    'primary': '#04ade8',
                    'background': '#cfcece'
                },

                style={'width': '25%'}
            )

        ], className='ten columns')

    ], className='row')
])


#callbacks triggered by the run query button - creates plots from user selection:
@app.callback(dash.dependencies.Output('testGraph', 'figure'),
              [dash.dependencies.Input('runQuery', 'clicks')],
              [dash.dependencies.Input('cedentList', 'value')],
              [dash.dependencies.State('dateRange', 'start_date'),
              dash.dependencies.State('dateRange', 'end_date')])
def makeTable(clicks, value, start_date, end_date):
    if clicks != 0:
        #make table using selected value from dropdown
        selectedColumnDF = df.loc[:, value]
        listTest = selectedColumnDF.values.tolist()
        print(listTest)



if __name__ == '__main__':
    app.run_server(debug=False)
