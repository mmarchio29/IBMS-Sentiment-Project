import pandas as pd
import numpy as np

import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Data
file_path = r'./assets/QuestromSA_final.csv'
df = pd.read_csv(file_path)

# Convert the date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Define positive and negative sentiments
positive_sentiments = ['Happiness', 'Love', 'Surprise']
negative_sentiments = ['Anger', 'Disgust', 'Fear', 'Sadness']

# Positive/Negative scores 
df['Positive'] = df[positive_sentiments].sum(axis=1)
df['Negative'] = df[negative_sentiments].sum(axis=1)

# Clean up whitespace and handle missing values
df['Source Type'] = df['Source Type'].str.strip().dropna()
df['Publication Title'] = df['Publication Title'].str.strip().dropna()
df['Keyword'] = df['Keyword'].str.strip().dropna()

# Ensure numeric columns are indeed numeric
numeric_columns = positive_sentiments + negative_sentiments + ['Positive', 'Negative']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Sentiment Analysis Dashboard", className="text-center my-4", style={'font-family': 'Arial', 'color': '#2E4053'}), width=11),
        ], justify="center"),
        dbc.Row([
            dbc.Col(html.A(html.Img(src=r'./assets/infoicon.svg', height='30px'), href='#', id='info-icon'), width=1, className="text-right")
        ]),

        dbc.Tooltip(
            [
                html.P("How to use this dashboard:", className="mb-2"),
                html.Ol([
                    html.Li("Select the source type, publisher, keyword, emotions, and aggregation value using the dropdown menus."),
                    html.Li("Adjust the year range slider to filter data based on the selected year range."),
                    html.Li("The graphs will update automatically based on your selections."),
                    html.Li("Scroll down to see additional visualizations.")
                ], style={'text-align': 'left'})
            ],
            target="info-icon",
            placement="right"
        ),

        dbc.Row([
            dbc.Col([
                html.Label("Source Type:", style={'font-family': 'Arial', 'color': '#2E4053'}),
                dcc.Dropdown(
                    id='source-type-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': st, 'value': st} for st in df['Source Type'].unique() if pd.notna(st)],
                    value='All',
                    clearable=False,
                    multi=True
                ),
            ], width=6, md=3, className="text-center"),

            dbc.Col([
                html.Label("Publisher:", style={'font-family': 'Arial', 'color': '#2E4053'}),
                dcc.Dropdown(
                    id='publisher-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': publisher, 'value': publisher} for publisher in df['Publication Title'].unique() if pd.notna(publisher)],
                    value='All',
                    clearable=False,
                    multi=True
                ),
            ], width=6, md=3, className="text-center"),

            dbc.Col([
                html.Label("Keyword:", style={'font-family': 'Arial', 'color': '#2E4053'}),
                dcc.Dropdown(
                    id='keyword-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': keyword, 'value': keyword} for keyword in df['Keyword'].unique() if pd.notna(keyword)],
                    value='All',
                    clearable=False,
                    multi=True
                ),
            ], width=6, md=3, className="text-center"),
        ], className="mb-4 justify-content-center"),

        dbc.Row([
            dbc.Col([
                html.Label("Emotions:", style={'font-family': 'Arial', 'color': '#2E4053'}),
                dcc.Dropdown(
                    id='emotions-dropdown',
                    options=[
                        {'label': 'Positive', 'value': 'Positive'},
                        {'label': 'Negative', 'value': 'Negative'},
                        {'label': 'Anger', 'value': 'Anger'},
                        {'label': 'Disgust', 'value': 'Disgust'},
                        {'label': 'Fear', 'value': 'Fear'},
                        {'label': 'Sadness', 'value': 'Sadness'},
                        {'label': 'Happiness', 'value': 'Happiness'},
                        {'label': 'Love', 'value': 'Love'},
                        {'label': 'Surprise', 'value': 'Surprise'},
                        {'label': 'Neutral', 'value': 'Neutral'},
                        {'label': 'Other', 'value': 'Other'}
                    ],
                    value=['Positive', 'Negative'],
                    multi=True
                ),
            ], width=6, md=3, className="text-center"),

            dbc.Col([
                html.Label("Aggregation Value:", style={'font-family': 'Arial', 'color': '#2E4053'}),
                dcc.Dropdown(
                    id='aggregation-dropdown',
                    options=[
                        {'label': 'Average Sentiment', 'value': 'mean'},
                        {'label': 'Median Sentiment', 'value': 'median'},
                        {'label': 'Max Sentiment', 'value': 'max'},
                        {'label': 'Min Sentiment', 'value': 'min'},
                        {'label': '5-Year Rolling Average', 'value': 'rolling_mean'}
                    ],
                    value='mean',
                    clearable=False
                ),
            ], width=6, md=3, className="text-center"),
        ], className="mb-4 justify-content-center"),

        dbc.Row([
            dbc.Col([
                html.Label("Year Range:", style={'font-family': 'Arial', 'color': '#2E4053'}),
                dcc.RangeSlider(
                    id='year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=[df['Year'].min(), df['Year'].max()],
                    marks={str(year): str(year) for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1) if int(year) % 5 == 0},
                    step=1
                ),
            ], width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='sentiment-line-graph', style={'height': '45vh'})
            ], width=12),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='capitalism-scatter-graph', style={'height': '45vh'})
            ], width=4),
            dbc.Col([
                dcc.Graph(id='communism-scatter-graph', style={'height': '45vh'})
            ], width=4),
            dbc.Col([
                dcc.Graph(id='keyword-dist-graph', style={'height': '45vh'})
            ], width=4),
        ], className="mb-4"),
    ], fluid=True, style={'background-color': '#EAEDED', 'padding': '40px', 'border-radius': '10px', 'margin-top': '20px', 'width': '100vw'})
])

@app.callback(
    [Output('sentiment-line-graph', 'figure'),
     Output('capitalism-scatter-graph', 'figure'),
     Output('communism-scatter-graph', 'figure'),
     Output('keyword-dist-graph', 'figure')],
    [Input('source-type-dropdown', 'value'),
     Input('publisher-dropdown', 'value'),
     Input('keyword-dropdown', 'value'),
     Input('emotions-dropdown', 'value'),
     Input('aggregation-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_source, selected_publisher, selected_keyword, selected_emotions, aggregation_value, selected_years):
    filtered_df = df.copy()
    if selected_source != 'All':
        filtered_df = filtered_df[filtered_df['Source Type'].isin(selected_source)]
    if selected_publisher != 'All':
        filtered_df = filtered_df[filtered_df['Publication Title'].isin(selected_publisher)]
    if selected_keyword != 'All':
        filtered_df = filtered_df[filtered_df['Keyword'].isin(selected_keyword)]

    filtered_df = filtered_df[(filtered_df['Year'] >= selected_years[0]) & (filtered_df['Year'] <= selected_years[1])]

    # Handle empty DataFrame scenario
    if filtered_df.empty:
        return (px.line(title="No data available for the selected filters."),
                px.scatter(title="No data available for the selected filters."),
                px.scatter(title="No data available for the selected filters."),
                px.bar(title="No data available for the selected filters."))

    # Line Graph
    numeric_columns = selected_emotions
    if not set(numeric_columns).issubset(filtered_df.columns):
        return (px.line(title="Please select at least one emotion."),
                px.scatter(title="Please select at least one emotion."),
                px.scatter(title="Please select at least one emotion."),
                px.bar(title="Please select at least one emotion."))
    
    filtered_df_numeric = filtered_df[['Date', 'Year', 'Keyword'] + numeric_columns].set_index('Date')
    if aggregation_value == 'rolling_mean':
        filtered_df_numeric = filtered_df_numeric.groupby(['Year', 'Keyword']).mean().rolling(window=5, min_periods=1).mean().reset_index()
    else:
        filtered_df_numeric = filtered_df_numeric.groupby(['Year', 'Keyword']).agg(aggregation_value).reset_index()

    if filtered_df_numeric.empty:
        line_fig = px.line(title="No data available for the selected filters.")
    else:
        line_fig = px.line(
            filtered_df_numeric,
            x='Year',
            y=numeric_columns,
            color='Keyword',
            line_group='Keyword',
            facet_col='variable',
            labels={'Year': 'Year', 'value': 'Sentiment Score', 'variable': 'Sentiment'},
            title=f'Sentiment Trends from {selected_years[0]} to {selected_years[1]}'
        )
        line_fig.update_layout(
            font_family="Arial", font_size=12, font_color="#2E4053", title_font_family="Arial", title_font_color="#2E4053",
            legend_title_font_color="#2E4053", template="plotly"
        )

    # Scatter Plot for Capitalism
    capitalism_df = filtered_df[filtered_df['Keyword'] == 'Capitalism']
    scatter_fig1 = px.scatter(
        capitalism_df.sort_values('Year'), x='Negative', y='Positive',
        animation_frame='Year',
        color='Keyword',
        labels={'Positive': 'Positive Sentiment', 'Negative': 'Negative Sentiment'},
        title='Sentiment Distribution Over Time (Capitalism)'
    )
    scatter_fig1.update_layout(
        font_family="Arial", font_size=12, font_color="#2E4053", title_font_family="Arial", title_font_color="#2E4053",
        legend_title_font_color="#2E4053", template="plotly",
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1])
    )

    # Scatter Plot for Communism
    communism_df = filtered_df[filtered_df['Keyword'] == 'Communism']
    scatter_fig2 = px.scatter(
        communism_df.sort_values('Year'), x='Negative', y='Positive',
        animation_frame='Year',
        color='Keyword',
        labels={'Positive': 'Positive Sentiment', 'Negative': 'Negative Sentiment'},
        title='Sentiment Distribution Over Time (Communism)'
    )
    scatter_fig2.update_layout(
        font_family="Arial", font_size=12, font_color="#2E4053", title_font_family="Arial", title_font_color="#2E4053",
        legend_title_font_color="#2E4053", template="plotly",
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1])
    )

    # Keyword Distribution Over Time
    keyword_dist = filtered_df.groupby(['Year', 'Keyword']).size().reset_index(name='Count')
    bar_fig = px.bar(
        keyword_dist,
        x='Year',
        y='Count',
        color='Keyword',
        labels={'Count': 'Count of Observations'},
        title='Keyword Distribution Over Time'
    )
    bar_fig.update_layout(
        font_family="Arial", font_size=12, font_color="#2E4053", title_font_family="Arial", title_font_color="#2E4053",
        legend_title_font_color="#2E4053", template="plotly",
        barmode='stack',
        margin=dict(l=0, r=0, t=30, b=0)
    )

    return line_fig, scatter_fig1, scatter_fig2, bar_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  # Change the port number as needed