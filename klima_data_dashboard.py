import dash
import dash_bootstrap_components as dbc
from dash import html
from millify import millify
from subgrounds.dash_wrappers import Graph
from subgrounds.plotly_wrappers import Figure, Scatter
from subgrounds.plotly_wrappers import Figure, Pie
import pandas as pd
from klima_data_query import sg, carbon_bct_1d, carbon_mco_1d, carbon_ubo_1d, carbon_nbo_1d, carbon_nct_1d, carbon_bct_250d, carbon_mco_250d, carbon_ubo_250d, carbon_nbo_250d, carbon_nct_250d, klima_supply_1d, klima_supply_250d, treasury_assets, carbon_custodied_250d, carbon_custodied_1d



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label('KlimaDAO Treasury Backed Carbon',
                      style={'font-style': 'normal',
                             'font-weight': '600',
                             'font-size': '64px',
                             'line-height': '64px',
                             'color': '#252525',
                             }, xs=18, sm=18 , md=18),
        ]),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('Klima price', className='text-center',
                        style={'text-align': 'center',
                        'color': '#FFFFFF',
                        'font-size': '24px',
                        'font-weight': '800'}
                    ),
                    html.H1('$ '+
                        millify(
                        sg.query([klima_supply_1d.klimaPrice]),
                        precision = 2),
                        style={'text-align': 'center',
                        'color': '#FFFFFF',
                        'font-size': '24px',
                        'font-weight': '800'},
                    )
                ]),
            ], style={'height': '100%', 'width': '60%', 
            'backgroundColor':'#74c476',
            'color':'#FFFFFF',
            'border':0, 
            #'border': '2px rgb(255, 255, 255) solid',
            'text-align':'right'}),
        ], width={"size": 2, "offset": -1}),#xs=12, sm=12, md=12, lg=3, xl=3),
    ], style={'padding': '20px'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('BTC Carbon [t]', className='text-center', 
                    style={'font-size':'28px'}),
                    
                    html.H1(''+
                        millify(
                            sg.query([carbon_bct_1d.carbonBalance]),
                            precision = 2),
                        style={'text-align': 'center',
                            'font-size': '24px'},
                    ),
                ]),
            ]),
        ],style={"width":"24rem", "size": 1, "order": "last", "offset": 1} ,xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('MCO Carbon [t]', className='text-center',
                    style={'font-size':'28px'}),
                    html.H1(''+
                        millify(
                            sg.query([carbon_mco_1d.carbonBalance]),
                            precision = 2),
                        style={'text-align': 'center',
                            'font-size': '24px'}
                    )
                ]),
            ]),
        ],style={"width":"24rem", "size": 1, "order": "last", "offset": 1}, xs=12, sm=12, md=12, lg=3, xl=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('UBO Carbon [t]', className='text-center',
                    style={'font-size':'28px'}),
                    html.H1(''+
                        millify(
                            sg.query([carbon_ubo_1d.carbonBalance]),
                            precision = 2),
                        style={'text-align': 'center',
                            'font-size': '24px'}
                    ),
                ]),
            ]),
        ], style={"width":"24rem", "size": 1, "order": "last", "offset": 1, 'align':'center', 'justify':'center'}, xs=12, sm=12, md=12, lg=3, xl=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('NBO Carbon [t]', className='text-center',
                    style={'font-size':'28px'}),
                    html.H1(''+
                        millify(
                            sg.query([carbon_nbo_1d.carbonBalance]),
                            precision = 2),
                        style={'text-align': 'center',
                            'font-size': '24px'}
                    )
                ]),
            ]),
        ], style={"width":"24rem", "size": 1, "order": "last", "offset": 1}, xs=12, sm=12, md=12, lg=3, xl=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('NCT Carbon [t]', className='text-center',
                    style={'font-size':'28px'}),
                    html.H1(''+
                        millify(
                            sg.query([carbon_nct_1d.carbonBalance]),
                            precision = 2),
                        style={'text-align': 'center',
                        'font-size': '24px'}
                    )
                ]),
            ]),
        ], style={"width":"24rem", "size": 1, "order": "last", "offset": 1}, xs=12, sm=12, md=12, lg=3, xl=3),

    ], style={'padding': '30px'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Carbon in Treasury [t]'),
                        ]),
                        dbc.Col([
                            millify(
                                sum(sg.query([
                                    carbon_bct_1d.carbonBalance,
                                    carbon_mco_1d.carbonBalance,
                                    carbon_ubo_1d.carbonBalance,
                                    carbon_nbo_1d.carbonBalance,
                                    carbon_nct_1d.carbonBalance])),
                                precision=2)
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='BCT Carbon',
                                x=carbon_bct_250d.datetime,
                                y=carbon_bct_250d.carbonBalance,
                                stackgroup='one'
                            ),
                            Scatter(
                                name='MCO Carbon',
                                x=carbon_mco_250d.datetime,
                                y=carbon_mco_250d.carbonBalance,
                                stackgroup='one'
                            ),
                            Scatter(
                                name='UBO Carbon',
                                x=carbon_ubo_250d.datetime,
                                y=carbon_ubo_250d.carbonBalance,
                                stackgroup='one'
                            ),
                            Scatter(
                                name='NBO Carbon',
                                x=carbon_nbo_250d.datetime,
                                y=carbon_nbo_250d.carbonBalance,
                                stackgroup='one'
                            ),
                            Scatter(
                                name='NCT Carbon',
                                x=carbon_nct_250d.datetime,
                                y=carbon_nct_250d.carbonBalance,
                                stackgroup='one'
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white',
                                      'title': 'klima carbon in treasury'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#2A2A2A',
                            'plot_bgcolor': '#2A2A2A',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#2A2A2A')
        ], xs=12, sm=12, md=12, lg=6, xl=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Klima Market Cap [$]'),
                        ]),
                        dbc.Col([
                            millify(
                                sg.query([klima_supply_1d.klimaCirculatingSupply]) * sg.query([klima_supply_1d.klimaPrice]),
                                precision=2)
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='Klima Market Cap',
                                x=klima_supply_250d.datetime,
                                y=klima_supply_250d.marketCap,
                                stackgroup='one'
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white',
                                      'title': 'klima Market Cap'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#2A2A2A',
                            'plot_bgcolor': '#2A2A2A',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#2A2A2A')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
    ], style={'padding': '10px'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Carbon allocation [%]'),
                        ])
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Pie(
                                name='BCT Carbon',
                                labels=treasury_assets.symbol,
                                values=treasury_assets.carbonBalance
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white',
                                      'title': 'klima carbon in treasury'},
                            'font':{'color':'white'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#2A2A2A',
                            'plot_bgcolor': '#2A2A2A',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#2A2A2A')
        ], xs=12, sm=12, md=12, lg=6, xl=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Backing per carbon custodied [$/t]'),
                        ]),
                        dbc.Col([
                            millify(
                                sg.query([carbon_custodied_1d.backing]),
                                precision=2)
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='Klima Market Cap',
                                x = carbon_custodied_250d.datetime,
                                y= carbon_custodied_250d.backing,
                                stackgroup='one'
                            ),
                        ],
                        layout={
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white',
                                      'title': 'klima Market Cap'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': '#2A2A2A',
                            'plot_bgcolor': '#2A2A2A',
                        }
                    ))
                ]),
            ], style={'height': '100%'}, color='#2A2A2A')
        ], xs=12, sm=12, md=12, lg=6, xl=6),
    ], style={'padding': '10px'}),

], style={'backgroundColor': '#74c476'}, fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)

