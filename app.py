import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from flask import Flask
from dash.dependencies import Input, Output, State
import numpy as np

# Inicializa o Flask
server = Flask(__name__)

# Inicializa o Dash com tema personalizado
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Cores personalizadas
CORES = {
    'fundo': '#F8F9FA',
    'card': '#FFFFFF',
    'texto': '#2C3E50',
    'primaria': '#3498DB',
    'secundaria': '#E74C3C',
    'terciaria': '#2ECC71',
    'destaque': '#F1C40F'
}

# Função para criar gráfico vazio em caso de erro
def create_empty_fig(title="Erro ao carregar dados"):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        template='plotly_white',
        plot_bgcolor=CORES['card'],
        paper_bgcolor=CORES['card']
    )
    return fig

# Lê o arquivo Excel
try:
    df = pd.read_excel(r'C:\Users\Gabri\Documents\default_prone_model\src\model\results\df_origin_prod_com_probabilidades.xlsx')
    # Garante que as colunas necessárias existem e são numéricas
    if 'PROBABILIDADES' in df.columns:
        df['PROBABILIDADES'] = pd.to_numeric(df['PROBABILIDADES'], errors='coerce')
    if 'ESTADO_CLIENTE' in df.columns:
        df['ESTADO_CLIENTE'] = df['ESTADO_CLIENTE'].fillna('Não Informado')
    if 'VALOR_FINANCIAMENTO' in df.columns:
        df['VALOR_FINANCIAMENTO'] = pd.to_numeric(df['VALOR_FINANCIAMENTO'], errors='coerce')
    if 'QT_DIAS_PRIM_PC_ATRASO' in df.columns:
        df['QT_DIAS_PRIM_PC_ATRASO'] = pd.to_numeric(df['QT_DIAS_PRIM_PC_ATRASO'], errors='coerce')
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    df = pd.DataFrame()

# Layout do dashboard
app.layout = dbc.Container([
    # Cabeçalho
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Dashboard de Análise de Inadimplência", 
                       className="text-center my-4",
                       style={'color': CORES['texto'], 'fontWeight': 'bold'}),
                html.Hr(style={'borderColor': CORES['primaria'], 'borderWidth': '2px'})
            ], style={'backgroundColor': CORES['card'], 'padding': '20px', 'borderRadius': '10px'})
        ])
    ], className="mb-4"),
    
    # Cards de Métricas
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Probabilidade Média", className="text-center mb-3"),
                    html.H2(id='big-number', className="text-center text-primary mb-0",
                           style={'fontSize': '2.5rem', 'fontWeight': 'bold'})
                ])
            ], style={'backgroundColor': CORES['card'], 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Valor Total em Risco", className="text-center mb-3"),
                    html.H2(id='valor-total', className="text-center text-danger mb-0",
                           style={'fontSize': '2.5rem', 'fontWeight': 'bold'})
                ])
            ], style={'backgroundColor': CORES['card'], 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Média de Dias em Atraso", className="text-center mb-3"),
                    html.H2(id='dias-atraso', className="text-center text-success mb-0",
                           style={'fontSize': '2.5rem', 'fontWeight': 'bold'})
                ])
            ], style={'backgroundColor': CORES['card'], 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ], width=4)
    ], className="mb-4"),
    
    # Gráfico Principal
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Análise por Estado", className="mb-0",
                           style={'color': CORES['texto'], 'fontWeight': 'bold'})
                ], style={'backgroundColor': CORES['card'], 'borderBottom': f'2px solid {CORES["primaria"]}'}),
                dbc.CardBody([
                    dcc.Graph(id='grafico-estados')
                ])
            ], style={'backgroundColor': CORES['card'], 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ])
    ], className="mb-4"),
    
    # Tabela de Contratos
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Top Contratos com Maior Risco", className="mb-0",
                           style={'color': CORES['texto'], 'fontWeight': 'bold'})
                ], style={'backgroundColor': CORES['card'], 'borderBottom': f'2px solid {CORES["primaria"]}'}),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='tabela-contratos',
                        columns=[
                            {'name': 'Número do Contrato', 'id': 'NUMERO_CONTRATO'},
                            {'name': 'Probabilidade', 'id': 'PROBABILIDADES'},
                            {'name': 'Valor Financiamento', 'id': 'VALOR_FINANCIAMENTO'},
                            {'name': 'Dias de Atraso', 'id': 'QT_DIAS_PRIM_PC_ATRASO'}
                        ],
                        data=[],
                        sort_action='native',
                        sort_mode='single',
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '12px',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'backgroundColor': CORES['card'],
                            'color': CORES['texto'],
                            'border': f'1px solid {CORES["fundo"]}'
                        },
                        style_header={
                            'backgroundColor': CORES['primaria'],
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            'padding': '12px'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': CORES['fundo']
                            }
                        ]
                    )
                ])
            ], style={'backgroundColor': CORES['card'], 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
        ])
    ])
], fluid=True, style={'backgroundColor': CORES['fundo'], 'padding': '20px'})

# Callback para atualizar os gráficos e a tabela
@app.callback(
    [Output('grafico-estados', 'figure'),
     Output('big-number', 'children'),
     Output('valor-total', 'children'),
     Output('dias-atraso', 'children'),
     Output('tabela-contratos', 'data')],
    [Input('grafico-estados', 'id')]
)
def update_graphs(_):
    try:
        if df.empty:
            return create_empty_fig(), "Erro", "Erro", "Erro", []

        # Prepara dados para o gráfico por Estado
        df_estados = df.groupby('ESTADO_CLIENTE').agg({
            'PROBABILIDADES': 'mean',
            'VALOR_FINANCIAMENTO': 'mean',
            'QT_DIAS_PRIM_PC_ATRASO': 'mean'
        }).reset_index()
        
        df_estados = df_estados.sort_values('PROBABILIDADES', ascending=False)
        
        # Cria o gráfico de barras
        fig = go.Figure()
        
        # Adiciona barras para probabilidade
        fig.add_trace(go.Bar(
            x=df_estados['ESTADO_CLIENTE'],
            y=df_estados['PROBABILIDADES'],
            name='Probabilidade',
            marker_color=CORES['primaria']
        ))
        
        # Adiciona linha para valor médio
        fig.add_trace(go.Scatter(
            x=df_estados['ESTADO_CLIENTE'],
            y=df_estados['VALOR_FINANCIAMENTO'] / df_estados['VALOR_FINANCIAMENTO'].max(),
            name='Valor Médio (normalizado)',
            yaxis='y2',
            line=dict(color=CORES['secundaria'], width=3)
        ))
        
        # Adiciona linha para dias de atraso
        fig.add_trace(go.Scatter(
            x=df_estados['ESTADO_CLIENTE'],
            y=df_estados['QT_DIAS_PRIM_PC_ATRASO'] / df_estados['QT_DIAS_PRIM_PC_ATRASO'].max(),
            name='Dias de Atraso (normalizado)',
            yaxis='y2',
            line=dict(color=CORES['terciaria'], width=3)
        ))
        
        # Atualiza o layout
        fig.update_layout(
            title={
                'text': 'Análise por Estado',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': CORES['texto']}
            },
            xaxis_title='Estado',
            yaxis_title='Probabilidade de Inadimplência',
            yaxis2=dict(
                title='Valores Normalizados',
                overlaying='y',
                side='right',
                showgrid=False
            ),
            template='plotly_white',
            plot_bgcolor=CORES['card'],
            paper_bgcolor=CORES['card'],
            font=dict(family="Arial", size=12, color=CORES['texto']),
            margin=dict(t=80, l=10, r=10, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor=CORES['card']
            ),
            showlegend=True
        )
        
        # Calcula métricas
        prob_media = f"{df['PROBABILIDADES'].mean():.2%}"
        valor_total = f"R$ {df['VALOR_FINANCIAMENTO'].sum():,.2f}"
        dias_media = f"{df['QT_DIAS_PRIM_PC_ATRASO'].mean():.1f} dias"
        
        # Prepara dados para a tabela
        tabela_data = df[['NUMERO_CONTRATO', 'PROBABILIDADES', 'VALOR_FINANCIAMENTO', 'QT_DIAS_PRIM_PC_ATRASO']].copy()
        tabela_data['PROBABILIDADES'] = tabela_data['PROBABILIDADES'].apply(lambda x: f"{x:.2%}")
        tabela_data['VALOR_FINANCIAMENTO'] = tabela_data['VALOR_FINANCIAMENTO'].apply(lambda x: f"R$ {x:,.2f}")
        tabela_data = tabela_data.sort_values('PROBABILIDADES', ascending=False).head(10).to_dict('records')
        
        return fig, prob_media, valor_total, dias_media, tabela_data
    
    except Exception as e:
        print(f"Erro ao gerar gráficos: {e}")
        return create_empty_fig(), "Erro", "Erro", "Erro", []

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
