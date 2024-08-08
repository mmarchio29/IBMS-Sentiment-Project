import pandas as pd
import numpy as np

import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

file_path = r'C:\\Users\\mamar\\Questrom Sentiment Project\\DATA\\QuestromSA_final.csv'
df = pd.read_csv(file_path)

# Ensure the Date column is in datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
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

# Ensure numeric columns 
numeric_columns = positive_sentiments + negative_sentiments + ['Positive', 'Negative']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div([

    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Economic Sentiment Report", className="text-center my-4", style={'font-family': 'Arial', 'color': '#2E4053'}), width=11),
        ], justify="center"),

        dcc.Dropdown(
            id='keyword-dropdown',
            options=[{'label': k, 'value': k} for k in df['Keyword'].unique()],
            value='Capitalism'
        ),
    
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='sentiment-graph', style={'height': '35vh'})
            ], width=7),
            dbc.Col([
                dcc.Graph(id='sentiment-pie', style={'height': '35vh'})
            ], width=5),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='sentiment-by-source', style={'height': '35vh'})
            ], width=4),
            dbc.Col([
                dcc.Graph(id='emotions-bar', style={'height': '35vh'})
            ], width=4),
            dbc.Col([
                html.Div(id='data-volume-summary', style={'height': '35vh'})
            ], width=4),
        ], className="mb-4"),
    ], fluid=True, style={'background-color': '#EAEDED', 'padding': '40px', 'border-radius': '10px', 'margin-top': '20px', 'width': '100vw'})
])

@app.callback(
    [Output('sentiment-graph', 'figure'),
     Output('sentiment-pie', 'figure'),
     Output('emotions-bar', 'figure'),
     Output('sentiment-by-source', 'figure'),
     Output('data-volume-summary', 'children')],
     [Input('keyword-dropdown', 'value')]
)
def update_graphs(keyword):

    filtered_df = df[df['Keyword'] == keyword].copy()
    numeric_cols = filtered_df.select_dtypes(include='number').columns
    yearly_sentiment = filtered_df.resample('YE', on='Date')[numeric_cols].mean()

    # LINE GRAPH
    sentimental_trend_fig = px.line(yearly_sentiment, y='Positive', title='Positive Sentiment Trend Over Time')
    sentimental_trend_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # PIE CHART
    positive_sentiments = filtered_df[['Positive']].mean()
    negative_sentiments = filtered_df[['Negative']].mean()

    sentiment_values = [positive_sentiments, negative_sentiments]
    sentiment_labels = ['Positive', 'Negative']
    sentiment_colors = ['#ff9999','#66b3ff']

    overall_sentiment_fig = px.pie(
        values=sentiment_values,
        names=sentiment_labels,
        title='Overall Sentiment',
        color_discrete_sequence=sentiment_colors
    )
    overall_sentiment_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # EMOTIONS BAR GRAPH
    emotions = filtered_df[['Happiness', 'Love', 'Surprise', 'Sadness', 'Anger', 'Disgust', 'Fear']].mean()
    overall_emotions_fig = px.bar(emotions, title='Overall Emotions')
    overall_emotions_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # SOURCE BAR GRAPH
    sentiment_by_source_fig = px.bar(df, x='Source Type', y='Happiness', title='Sentiment by Source')
    sentiment_by_source_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # DATA VOLUME SUMMARY 
    filtered_df['Period'] = pd.cut(
        filtered_df['Date'].dt.year,
        bins=[-float('inf'), 1960, 1980, 2010, float('inf')],
        labels=['Before 1960', '1960-1980', '1980-2010', '2010-Present']
    )

    period_counts = filtered_df['Period'].value_counts().reindex(['Before 1960', '1960-1980', '1990-2010', '2010-Present'], fill_value=0)
    data_volume_summary = html.Div([
        html.Div(f"Before 1960: {period_counts['Before 1960']} records", className='data-volume'),
        html.Div(f"1960-1980: {period_counts['1960-1980']} records", className='data-volume'),
        html.Div(f"1990-2010: {period_counts['1990-2010']} records", className='data-volume'),
        html.Div(f"2010-Present: {period_counts['2010-Present']} records", className='data-volume')
    ])

    return sentimental_trend_fig, overall_sentiment_fig, overall_emotions_fig, sentiment_by_source_fig, data_volume_summary

# Run
if __name__ == '__main__':
    app.run_server(debug=True)