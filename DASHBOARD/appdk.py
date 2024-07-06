import pandas as pd
import numpy as np

import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Data
file_path = r'./assets/final_merged_output.xlsx'
df = pd.read_excel(file_path)

# Convert the 'Date_x' column to datetime format
df['Date_x'] = pd.to_datetime(df['Date_x'])
df['Year'] = df['Date_x'].dt.year

# Define positive and negative sentiments
positive_sentiments = ['Happiness', 'Love', 'Surprise']
negative_sentiments = ['Anger', 'Disgust', 'Fear', 'Sadness']

# Positive/Negative scores 
df['Positive'] = df[positive_sentiments].sum(axis=1)
df['Negative'] = df[negative_sentiments].sum(axis=1)

# Add 'keyword' column
df['keyword'] = 'Capitalism'

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Sentiment Analysis Dashboard", className="text-center my-4", style={'font-family': 'Arial', 'color': '#2E4053'}), width=11),
            dbc.Col(html.A(html.Img(src='./assets/infoicon.svg', height='30px'), href='#', id='info-icon'), width=1, className="text-right")
        ], justify="center"),

        dbc.Tooltip(
            [
                html.P("How to use this dashboard:", className="mb-2"),
                html.Ol([
                    html.Li("Select the source type, publisher, keyword, emotions, and aggregation value using the dropdown menus."),
                    html.Li("Adjust the year range slider to filter data based on the selected year range."),
                    html.Li("The line graph will update automatically based on your selections."),
                    html.Li("Scroll down to see additional visualizations, such as the stacked area chart.")
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
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': st, 'value': st} for st in df['Source Type'].unique()],
                    value='All',
                    clearable=False
                ),
            ], width=6, md=3, className="text-center"),

            dbc.Col([
                html.Label("Publisher:", style={'font-family': 'Arial', 'color': '#2E4053'}),
                dcc.Dropdown(
                    id='publisher-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': publisher, 'value': publisher} for publisher in df['Publication Title'].unique()],
                    value='All',
                    clearable=False
                ),
            ], width=6, md=3, className="text-center"),

            dbc.Col([
                html.Label("Keyword:", style={'font-family': 'Arial', 'color': '#2E4053'}),
                dcc.Dropdown(
                    id='keyword-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': keyword, 'value': keyword} for keyword in df['keyword'].unique()],
                    value='All',
                    clearable=False
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
                    marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1) if year % 5 == 0},
                    step=1
                ),
            ], width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='sentiment-line-graph', style={'height': '45vh'})
            ], width=6),
            dbc.Col([
                dcc.Graph(id='stacked-area-graph', style={'height': '45vh'})
            ], width=6)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='animated-bar-graph', style={'height': '45vh'})
            ], width=6),
            dbc.Col([
                dcc.Graph(id='animated-source-type-graph', style={'height': '45vh'})
            ], width=6)
        ], className="mb-4"),
    ], fluid=True, style={'background-color': '#EAEDED', 'padding': '40px', 'border-radius': '10px', 'margin-top': '20px', 'width': '100vw'})
])

@app.callback(
    [Output('sentiment-line-graph', 'figure'),
     Output('stacked-area-graph', 'figure'),
     Output('animated-bar-graph', 'figure'),
     Output('animated-source-type-graph', 'figure')],
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
        filtered_df = filtered_df[filtered_df['Source Type'] == selected_source]
    if selected_publisher != 'All':
        filtered_df = filtered_df[filtered_df['Publication Title'] == selected_publisher]
    if selected_keyword != 'All':
        filtered_df = filtered_df[filtered_df['keyword'] == selected_keyword]

    filtered_df = filtered_df[(filtered_df['Year'] >= selected_years[0]) & (filtered_df['Year'] <= selected_years[1])]

    # Handle empty DataFrame scenario
    if filtered_df.empty:
        return (px.line(title="No data available for the selected filters."),
                px.area(title="No data available for the selected filters."),
                px.bar(title="No data available for the selected filters."),
                px.bar(title="No data available for the selected filters."))

    # Line Graph
    numeric_columns = selected_emotions
    if not set(numeric_columns).issubset(filtered_df.columns):
        return (px.line(title="Please select at least one emotion."),
                px.area(title="Please select at least one emotion."),
                px.bar(title="Please select at least one emotion."),
                px.bar(title="Please select at least one emotion."))

    filtered_df_numeric = filtered_df[['Date_x'] + numeric_columns].set_index('Date_x')
    filtered_df_numeric = filtered_df_numeric.resample('D').mean().interpolate(method='linear').ffill().bfill()

    if filtered_df_numeric.empty:
        line_fig = px.line(title="No data available for the selected filters.")
    else:
        if aggregation_value == 'mean':
            yearly_sentiments = filtered_df_numeric.resample('Y').mean().reset_index()
        elif aggregation_value == 'median':
            yearly_sentiments = filtered_df_numeric.resample('Y').median().reset_index()
        elif aggregation_value == 'max':
            yearly_sentiments = filtered_df_numeric.resample('Y').max().reset_index()
        elif aggregation_value == 'min':
            yearly_sentiments = filtered_df_numeric.resample('Y').min().reset_index()
        elif aggregation_value == 'rolling_mean':
            yearly_sentiments = filtered_df_numeric.resample('Y').mean().rolling(window=5, min_periods=1).mean().reset_index()

        line_fig = px.line(yearly_sentiments, x='Date_x', y=numeric_columns,
                           labels={'Date_x': 'Year', 'value': 'Sentiment Score', 'variable': 'Sentiment'},
                           title=f'Sentiment Trends for {selected_source} Source by {selected_publisher} Publisher from {selected_years[0]} to {selected_years[1]}')
        line_fig.update_layout(font_family="Arial", font_size=12, font_color="#2E4053", title_font_family="Arial", title_font_color="#2E4053",
                               legend_title_font_color="#2E4053", template="plotly")

    # Stacked Area Chart (not affected by 'Emotions' toggle)
    stacked_filtered_df = filtered_df[['Date_x', 'Positive', 'Negative']].set_index('Date_x')
    stacked_filtered_df = stacked_filtered_df.resample('D').mean().interpolate(method='linear').ffill().bfill()
    stacked_filtered_df = stacked_filtered_df[(stacked_filtered_df.index.year >= selected_years[0]) & (stacked_filtered_df.index.year <= selected_years[1])]

    if stacked_filtered_df.empty:
        stacked_area_fig = px.area(title="No data available for the selected filters.")
    else:
        yearly_stacked_sentiments = stacked_filtered_df.resample('Y').mean().reset_index()
        yearly_stacked_sentiments['Total'] = yearly_stacked_sentiments['Positive'] + yearly_stacked_sentiments['Negative']
        yearly_stacked_sentiments['Positive_Percentage'] = (yearly_stacked_sentiments['Positive'] / yearly_stacked_sentiments['Total']) * 100
        yearly_stacked_sentiments['Negative_Percentage'] = (yearly_stacked_sentiments['Negative'] / yearly_stacked_sentiments['Total']) * 100

        stacked_area_fig = go.Figure()
        stacked_area_fig.add_trace(go.Scatter(
            x=yearly_stacked_sentiments['Date_x'], 
            y=yearly_stacked_sentiments['Positive_Percentage'],
            mode='lines',
            name='Positive Sentiment',
            stackgroup='one',
            line=dict(width=0.5, color='rgba(135, 206, 250, 0.5)'),
            fillcolor='rgba(135, 206, 250, 0.5)'
        ))
        stacked_area_fig.add_trace(go.Scatter(
            x=yearly_stacked_sentiments['Date_x'], 
            y=yearly_stacked_sentiments['Negative_Percentage'],
            mode='lines',
            name='Negative Sentiment',
            stackgroup='one',
            line=dict(width=0.5, color='rgba(255, 99, 71, 0.5)'),
            fillcolor='rgba(255, 99, 71, 0.5)'
        ))

        stacked_area_fig.update_layout(
            title='Sentiment Distribution Over Time',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Sentiment Percentage Over Time', range=[0, 100]),
            font=dict(family="Arial", size=12, color="#2E4053"),
            title_font=dict(family="Arial", size=16, color="#2E4053"),
            legend_title_font=dict(family="Arial", size=14, color="#2E4053"),
            template="plotly"
        )

    # Simplified Animated Bar Chart
    if aggregation_value == 'mean':
        animation_df = filtered_df.melt(id_vars=['Date_x', 'Year', 'Source Type', 'Publication Title', 'keyword'], 
                                        value_vars=selected_emotions, 
                                        var_name='Emotion', 
                                        value_name='Score')
        animation_df = animation_df.groupby(['Year', 'Emotion']).mean().reset_index()
    elif aggregation_value == 'median':
        animation_df = filtered_df.melt(id_vars=['Date_x', 'Year', 'Source Type', 'Publication Title', 'keyword'], 
                                        value_vars=selected_emotions, 
                                        var_name='Emotion', 
                                        value_name='Score')
        animation_df = animation_df.groupby(['Year', 'Emotion']).median().reset_index()
    elif aggregation_value == 'max':
        animation_df = filtered_df.melt(id_vars=['Date_x', 'Year', 'Source Type', 'Publication Title', 'keyword'], 
                                        value_vars=selected_emotions, 
                                        var_name='Emotion', 
                                        value_name='Score')
        animation_df = animation_df.groupby(['Year', 'Emotion']).max().reset_index()
    elif aggregation_value == 'min':
        animation_df = filtered_df.melt(id_vars=['Date_x', 'Year', 'Source Type', 'Publication Title', 'keyword'], 
                                        value_vars=selected_emotions, 
                                        var_name='Emotion', 
                                        value_name='Score')
        animation_df = animation_df.groupby(['Year', 'Emotion']).min().reset_index()
    elif aggregation_value == 'rolling_mean':
        animation_df = filtered_df.melt(id_vars=['Date_x', 'Year', 'Source Type', 'Publication Title', 'keyword'], 
                                        value_vars=selected_emotions, 
                                        var_name='Emotion', 
                                        value_name='Score')
        animation_df = animation_df.groupby(['Year', 'Emotion']).mean().reset_index()
        animation_df = animation_df.groupby(['Emotion']).apply(lambda x: x.set_index('Year').rolling(window=5, min_periods=1).mean()).reset_index()

    animation_df['Year'] = animation_df['Year'].astype(str)
    animation_df.sort_values(by=['Year', 'Emotion'], inplace=True)

    # Set y-axis limit slightly above the max score
    y_max = animation_df['Score'].max() * 1.1

    bar_fig = px.bar(animation_df, x='Emotion', y='Score', color='Emotion', animation_frame='Year',
                     labels={'Score': 'Sentiment Score'},
                     title='Sentiment Animation Over Time',
                     range_y=[0, y_max],
                     color_discrete_map={
                         'Positive': 'rgba(135, 206, 250, 0.7)',
                         'Negative': 'rgba(255, 99, 71, 0.7)',
                         'Neutral': 'rgba(128, 128, 128, 0.7)',
                         'Other': 'rgba(128, 128, 128, 0.7)',
                         'Happiness': 'rgba(135, 206, 250, 0.7)',
                         'Love': 'rgba(135, 206, 250, 0.7)',
                         'Surprise': 'rgba(135, 206, 250, 0.7)',
                         'Anger': 'rgba(255, 99, 71, 0.7)',
                         'Disgust': 'rgba(255, 99, 71, 0.7)',
                         'Fear': 'rgba(255, 99, 71, 0.7)',
                         'Sadness': 'rgba(255, 99, 71, 0.7)'
                     })

    bar_fig.update_layout(
        title="Sentiment Animation Over Time",
        showlegend=False,
        font_family="Arial",
        font_size=12,
        font_color="#2E4053",
        title_font_family="Arial",
        title_font_color="#2E4053",
        legend_title_font_color="#2E4053",
        template="plotly"
    )

    # Fourth Graph: Animated Source Type Sentiment Analysis
    if aggregation_value == 'mean':
        source_type_df = filtered_df.groupby(['Year', 'Source Type']).mean().reset_index()
    elif aggregation_value == 'median':
        source_type_df = filtered_df.groupby(['Year', 'Source Type']).median().reset_index()
    elif aggregation_value == 'max':
        source_type_df = filtered_df.groupby(['Year', 'Source Type']).max().reset_index()
    elif aggregation_value == 'min':
        source_type_df = filtered_df.groupby(['Year', 'Source Type']).min().reset_index()
    elif aggregation_value == 'rolling_mean':
        source_type_df = filtered_df.groupby(['Year', 'Source Type']).mean().reset_index()
        source_type_df = source_type_df.groupby(['Source Type']).apply(lambda x: x.set_index('Year').rolling(window=5, min_periods=1).mean()).reset_index()

    source_type_df['Year'] = source_type_df['Year'].astype(str)
    source_type_df = source_type_df.sort_values(by='Year')

    source_type_df['positive_percentage'] = (source_type_df['Positive'] / (source_type_df['Positive'] + source_type_df['Negative'])) * 100
    source_type_df['negative_percentage'] = (source_type_df['Negative'] / (source_type_df['Positive'] + source_type_df['Negative'])) * 100

    fourth_fig = px.bar(source_type_df, x='Source Type', y=['positive_percentage', 'negative_percentage'], animation_frame='Year',
                        labels={'value': 'Sentiment Percentage'},
                        title='Sentiment Animation by Source Type Over Time',
                        range_y=[0, 100],
                        color_discrete_map={
                            'positive_percentage': 'rgba(135, 206, 250, 0.7)',
                            'negative_percentage': 'rgba(255, 99, 71, 0.7)'
                        })

    fourth_fig.update_layout(
        title="Sentiment Animation by Source Type Over Time",
        showlegend=True,
        font_family="Arial",
        font_size=12,
        font_color="#2E4053",
        title_font_family="Arial",
        title_font_color="#2E4053",
        legend_title_font_color="#2E4053",
        template="plotly"
    )

    return line_fig, stacked_area_fig, bar_fig, fourth_fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  # Change the port number as needed