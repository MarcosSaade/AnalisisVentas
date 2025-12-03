"""
Dashboard de Análisis de Ventas
Aplicación web con múltiples visualizaciones en pestañas
Ejecutar: python src/dashboard_app.py
Ver en: http://localhost:8050
"""

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# =============================================================================
# CARGA DE DATOS
# =============================================================================

# Ventas limpias
df = pd.read_csv('data_clean/ventas_clean.csv')
df['Fecha'] = pd.to_datetime(df['Fecha'])
df = df.sort_values('Fecha')
df['Semana'] = ((df['Fecha'] - df['Fecha'].min()).dt.days // 7) + 1

# Predicciones
data_predicha = pd.read_csv('data_clean/data_con_predicciones.csv')
data_predicha['Fecha'] = pd.to_datetime(data_predicha['Fecha'])
data_predicha['Semana'] = ((data_predicha['Fecha'] - data_predicha['Fecha'].min()).dt.days // 7) + 1

# Predicciones por productos (si existe)
try:
    productos_pred = pd.read_csv('data_clean/data_con_predicciones_productos.csv')
    productos_pred['Fecha'] = pd.to_datetime(productos_pred['Fecha'])
    productos_pred['Semana'] = ((productos_pred['Fecha'] - productos_pred['Fecha'].min()).dt.days // 7) + 1
    TIENE_PRODUCTOS = True
except FileNotFoundError:
    productos_pred = pd.DataFrame()
    TIENE_PRODUCTOS = False

# Predicciones 2025 (si existe)
try:
    data_2025 = pd.read_csv('data_clean/data_2025_predicciones.csv')
    data_2025['Fecha'] = pd.to_datetime(data_2025['Fecha'])
    data_2025['Semana'] = ((data_2025['Fecha'] - data_2025['Fecha'].min()).dt.days // 7) + 1
    TIENE_2025 = True
except FileNotFoundError:
    data_2025 = pd.DataFrame()
    TIENE_2025 = False

# =============================================================================
# CREAR APLICACIÓN
# =============================================================================

app = Dash(__name__)
app.title = "Dashboard de Ventas"

# =============================================================================
# LAYOUTS DE CADA TAB (definidos antes para que los callbacks funcionen)
# =============================================================================

# Tab 1: Ventas por Categoría
tab_ventas = html.Div([
    html.H3("📈 Cantidad por Categoría a lo largo del tiempo", style={'color': '#2c3e50'}),
    html.Div([
        html.Div([
            html.Label("Región:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
                value=df['Region'].unique().tolist(),
                multi=True
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
        html.Div([
            html.Label("Categoría:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='categoria-dropdown',
                options=[{'label': c, 'value': c} for c in sorted(df['Categoria'].unique())],
                value=df['Categoria'].unique().tolist(),
                multi=True
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={'marginBottom': '20px'}),
    dcc.Graph(id='cantidad-graph')
], style={'padding': '20px'})

# Tab 2: Real vs Predicho
tab_vs = html.Div([
    html.H3("🔮 Cantidad Real vs Cantidad Predicha", style={'color': '#2c3e50'}),
    html.Div([
        html.Div([
            html.Label("Región:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-dropdown-vs',
                options=[{'label': r, 'value': r} for r in sorted(data_predicha['Region'].unique())],
                value=data_predicha['Region'].unique().tolist(),
                multi=True
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
        html.Div([
            html.Label("Categoría:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='categoria-dropdown-vs',
                options=[{'label': c, 'value': c} for c in sorted(data_predicha['Categoria'].unique())],
                value=data_predicha['Categoria'].unique().tolist(),
                multi=True
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={'marginBottom': '20px'}),
    dcc.Graph(id='cantidad-vs-graph')
], style={'padding': '20px'})

# Tab 3: Productos Predichos
if TIENE_PRODUCTOS:
    tab_productos = html.Div([
        html.H3("📦 Cantidad Predicha por Producto", style={'color': '#2c3e50'}),
        html.Div([
            html.Label("Región:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-dropdown-prod',
                options=[{'label': r, 'value': r} for r in sorted(productos_pred['Region'].unique())],
                value=productos_pred['Region'].unique().tolist(),
                multi=True
            ),
        ], style={'width': '48%', 'marginBottom': '20px'}),
        dcc.Graph(id='productos-graph')
    ], style={'padding': '20px'})
else:
    tab_productos = html.Div([
        html.H3("📦 Productos Predichos", style={'color': '#2c3e50'}),
        html.P("⚠️ No se encontró el archivo data_con_predicciones_productos.csv", 
               style={'color': 'red', 'fontSize': '18px'}),
        # Componentes ocultos para evitar errores de callback
        dcc.Dropdown(id='region-dropdown-prod', style={'display': 'none'}),
        dcc.Graph(id='productos-graph', style={'display': 'none'})
    ], style={'padding': '20px'})

# Tab 4: Predicciones 2025
if TIENE_2025:
    tab_2025 = html.Div([
        html.H3("📅 Predicciones 2025 por Categoría", style={'color': '#2c3e50'}),
        html.Div([
            html.Div([
                html.Label("Región:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='region-dropdown-2025',
                    options=[{'label': r, 'value': r} for r in sorted(data_2025['Region'].unique())],
                    value=data_2025['Region'].unique().tolist(),
                    multi=True
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
            html.Div([
                html.Label("Categoría:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='categoria-dropdown-2025',
                    options=[{'label': c, 'value': c} for c in sorted(data_2025['Categoria'].unique())],
                    value=data_2025['Categoria'].unique().tolist(),
                    multi=True
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        ], style={'marginBottom': '20px'}),
        dcc.Graph(id='cantidad-predicha-2025-graph')
    ], style={'padding': '20px'})
else:
    tab_2025 = html.Div([
        html.H3("📅 Predicciones 2025", style={'color': '#2c3e50'}),
        html.P("⚠️ No se encontró el archivo data_2025_predicciones.csv", 
               style={'color': 'red', 'fontSize': '18px'}),
        # Componentes ocultos para evitar errores de callback
        dcc.Dropdown(id='region-dropdown-2025', style={'display': 'none'}),
        dcc.Dropdown(id='categoria-dropdown-2025', style={'display': 'none'}),
        dcc.Graph(id='cantidad-predicha-2025-graph', style={'display': 'none'})
    ], style={'padding': '20px'})

# =============================================================================
# LAYOUT PRINCIPAL CON TABS
# =============================================================================

app.layout = html.Div([
    html.H1("📊 Dashboard de Análisis de Ventas", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px', 
                   'borderBottom': '3px solid #3498db', 'paddingBottom': '15px'}),
    
    dcc.Tabs([
        dcc.Tab(label='📈 Ventas por Categoría', children=[tab_ventas],
                style={'padding': '10px', 'fontWeight': 'bold'}, 
                selected_style={'padding': '10px', 'fontWeight': 'bold', 'backgroundColor': '#e8f4f8'}),
        dcc.Tab(label='🔮 Real vs Predicho', children=[tab_vs],
                style={'padding': '10px', 'fontWeight': 'bold'}, 
                selected_style={'padding': '10px', 'fontWeight': 'bold', 'backgroundColor': '#e8f4f8'}),
        dcc.Tab(label='📦 Productos Predichos', children=[tab_productos],
                style={'padding': '10px', 'fontWeight': 'bold'}, 
                selected_style={'padding': '10px', 'fontWeight': 'bold', 'backgroundColor': '#e8f4f8'}),
        dcc.Tab(label='📅 Predicciones 2025', children=[tab_2025],
                style={'padding': '10px', 'fontWeight': 'bold'}, 
                selected_style={'padding': '10px', 'fontWeight': 'bold', 'backgroundColor': '#e8f4f8'}),
    ]),
    
], style={'padding': '30px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f8f9fa'})

# =============================================================================
# CALLBACKS
# =============================================================================

# Callback Tab 1: Ventas por Categoría
@app.callback(
    Output('cantidad-graph', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('categoria-dropdown', 'value')]
)
def update_ventas_graph(selected_regions, selected_categories):
    if not selected_regions or not selected_categories:
        return px.bar(title='Selecciona al menos una región y categoría')
    
    filtered = df[df['Region'].isin(selected_regions) & df['Categoria'].isin(selected_categories)]
    grouped = filtered.groupby(['Semana', 'Categoria'])['Cantidad'].sum().unstack().reset_index()
    grouped = grouped.sort_values('Semana')
    
    fig = px.bar(grouped, x='Semana', y=grouped.columns[1:],
                 title='Cantidad por Categoría por Semana',
                 labels={'value': 'Cantidad', 'Semana': 'Semana', 'variable': 'Categoría'})
    
    fig.update_layout(height=550, xaxis_tickangle=-45, legend_title_text='Categoría',
                      plot_bgcolor='white', paper_bgcolor='white')
    return fig


# Callback Tab 2: Real vs Predicho
@app.callback(
    Output('cantidad-vs-graph', 'figure'),
    [Input('region-dropdown-vs', 'value'),
     Input('categoria-dropdown-vs', 'value')]
)
def update_vs_graph(selected_regions, selected_categories):
    if not selected_regions or not selected_categories:
        return px.line(title='Selecciona al menos una región y categoría')
    
    filtered = data_predicha[
        data_predicha['Region'].isin(selected_regions) & 
        data_predicha['Categoria'].isin(selected_categories)
    ]
    grouped = filtered.groupby('Semana')[['Cantidad_Semanal', 'Cantidad_Predicha']].sum().reset_index()
    grouped = grouped.sort_values('Semana')
    
    fig = px.line(grouped, x='Semana', y=['Cantidad_Semanal', 'Cantidad_Predicha'],
                  title='Cantidad Real vs Predicha por Semana',
                  labels={'value': 'Cantidad', 'Semana': 'Semana', 'variable': 'Tipo'},
                  markers=True)
    
    # Renombrar las leyendas
    fig.for_each_trace(lambda t: t.update(name='Real' if t.name == 'Cantidad_Semanal' else 'Predicha'))
    
    fig.update_layout(height=550, legend_title_text='',
                      plot_bgcolor='white', paper_bgcolor='white')
    return fig


# Callback Tab 3: Productos
@app.callback(
    Output('productos-graph', 'figure'),
    Input('region-dropdown-prod', 'value')
)
def update_productos_graph(selected_regions):
    if not TIENE_PRODUCTOS or productos_pred.empty:
        return px.bar(title='No hay datos de productos disponibles')
    
    if not selected_regions:
        return px.bar(title='Selecciona al menos una región')
    
    filtered = productos_pred[productos_pred['Region'].isin(selected_regions)]
    
    # Agrupar por semana y producto
    if 'ID_Producto' in filtered.columns:
        grouped = filtered.groupby(['Semana', 'ID_Producto'])['Cantidad_Semanal'].mean().reset_index()
        grouped['ID_Producto'] = grouped['ID_Producto'].astype(str)
        fig = px.bar(grouped, x='Semana', y='Cantidad_Semanal', color='ID_Producto',
                     title='Cantidad Predicha Promedio por Producto',
                     labels={'Cantidad_Semanal': 'Cantidad Promedio', 'ID_Producto': 'Producto'})
        fig.update_layout(barmode='stack')
    else:
        grouped = filtered.groupby('Semana')['Cantidad_Semanal'].mean().reset_index()
        fig = px.bar(grouped, x='Semana', y='Cantidad_Semanal',
                     title='Cantidad Predicha Promedio por Semana')
    
    fig.update_layout(height=550, xaxis_tickangle=-45,
                      plot_bgcolor='white', paper_bgcolor='white')
    return fig


# Callback Tab 4: Predicciones 2025
@app.callback(
    Output('cantidad-predicha-2025-graph', 'figure'),
    [Input('region-dropdown-2025', 'value'),
     Input('categoria-dropdown-2025', 'value')]
)
def update_2025_graph(selected_regions, selected_categories):
    if not TIENE_2025 or data_2025.empty:
        return px.bar(title='No hay datos de 2025 disponibles')
    
    if not selected_regions:
        selected_regions = data_2025['Region'].unique().tolist()
    if not selected_categories:
        selected_categories = data_2025['Categoria'].unique().tolist()

    filtered = data_2025[
        data_2025['Region'].isin(selected_regions) &
        data_2025['Categoria'].isin(selected_categories)
    ].dropna(subset=['Cantidad_Predicha']).copy()

    if filtered.empty:
        return px.bar(title='No hay datos para las selecciones')

    grouped = filtered.groupby(['Semana', 'Categoria'])['Cantidad_Predicha'].mean().unstack().reset_index().sort_values('Semana')

    if grouped.empty:
        return px.bar(title='No hay datos para las selecciones')

    # Obtener nombres de columnas como lista (excluyendo 'Semana')
    y_cols = [col for col in grouped.columns if col != 'Semana']
    
    fig = px.bar(grouped, x='Semana', y=y_cols,
                 title='Cantidad Predicha Promedio por Categoría (2025)',
                 labels={'value': 'Cantidad Predicha Promedio', 'Semana': 'Semana', 'variable': 'Categoría'})

    tick_start = int(grouped['Semana'].min())
    tick_end = int(grouped['Semana'].max())
    tick_step = 2 if (tick_end - tick_start) >= 2 else 1
    tickvals = list(range(tick_start, tick_end + 1, tick_step))
    
    fig.update_layout(height=550, xaxis_tickangle=-45, legend_title_text='Categoría',
                      plot_bgcolor='white', paper_bgcolor='white',
                      xaxis=dict(tickmode='array', tickvals=tickvals, ticktext=[str(v+4) for v in tickvals]))

    return fig

# =============================================================================
# EJECUTAR SERVIDOR
# =============================================================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Dashboard de Ventas iniciado!")
    print("📍 Abre tu navegador en: http://localhost:8051")
    print("⏹️  Presiona Ctrl+C para detener")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=8051)
