from dash import html, dcc, register_page, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from data_manager import get_data

# Register the page with Dash
register_page(
    __name__,
    name='Communism Sentiment Analysis',
    title='Mehrotra IBMS',
    path='/communism/dashboard'
)

# Fetch and preprocess the data
df = get_data()

# Filter the data for "Communism" and "Communist" keywords only once
df = df.loc[(df['Keyword'] == 'Communism') | (df['Keyword'] == 'Communist')]

# Emotion options (for radio buttons)
emotion_options = [{'label': 'Positive', 'value': 'Positive'}, {'label': 'Negative', 'value': 'Negative'}]

# Keyword options (for radio items)
keyword_options = [{'label': 'Communism', 'value': 'Communism'}, {'label': 'Communist', 'value': 'Communist'}]

# Create an indicator figure
def create_indicator(filtered_df, selected_emotion):
    last_year = filtered_df['Year'].max()
    first_year = filtered_df['Year'].min()

    last_year_value = filtered_df[filtered_df['Year'] == last_year][selected_emotion].mean()
    first_year_value = filtered_df[filtered_df['Year'] == first_year][selected_emotion].mean()

    indicator = go.Figure(go.Indicator(
        mode="number+delta",
        value=last_year_value,
        delta={'reference': first_year_value, 'relative': True, 'increasing': {'color': '#57e389'}, 'decreasing': {'color': '#ff6347'}},
        title={"text": f"Year {int(last_year)} {selected_emotion.capitalize()} Sentiment", 'font': {'size': 20, 'color': 'white'}},
        number={'font': {'size': 50, 'color': 'white'}},
        domain={'x': [0, 1], 'y': [0, 1]},
    ))

    indicator.update_layout(
        paper_bgcolor='rgba(10, 10, 10, 0.7)',
        plot_bgcolor='rgba(10, 10, 10, 0.7)',
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(color='white')
    )
    return indicator

# Layout definition
# Layout definition
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.A(html.Img(src='../assets/images/info.png', height='70px'), href='#', id='communism-info-icon'), width=1, className="text-right")
    ], style={'padding-bottom': '15px'}),
    dbc.Row([
        dbc.Col(html.H2("Communism & Communist", className="text-center my-4", style={'fontFamily': 'Roboto', 'color': 'white'})),
    ], justify="center"),
    dbc.Tooltip(
        [
            html.P("How to use this dashboard:", className="mb-2"),
            html.Ol([
                html.Li("1. Select options from the dropdown menus."),
                html.Li("2. Adjust the year range using the slider."),
                html.Li("3. The graphs will automatically update to reflect your choices."),
                html.Li("4. Scroll down to explore additional visualizations.")
            ], style={'textAlign': 'left'})
        ],
        target="communism-info-icon",
        placement="right"
    ),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Label("Emotion:", style={'fontFamily': 'Roboto', 'color': 'white', 'fontSize': '18px'}),
                dbc.RadioItems(
                    id='communism-emotions-radio',
                    options=emotion_options,
                    value='Positive',
                    inline=True,
                    labelStyle={'margin-right': '10px', 'fontSize': '16px'}
                )
            ], className="dropdown-individual"), width=12, md=6
        ),
        dbc.Col(
            html.Div([
                html.Label("Keyword:", style={'fontFamily': 'Roboto', 'color': 'white', 'fontSize': '18px'}),
                dbc.RadioItems(
                    id='communism-keyword-radio',
                    options=keyword_options,
                    value='Communism',
                    inline=True,
                    labelStyle={'margin-right': '10px', 'fontSize': '16px'}
                )
            ], className="dropdown-individual"), width=12, md=6
        ),
    ], className="mb-4", style={'padding-top': '20px', 'padding-bottom': '20px'}),
    dbc.Row([
        dbc.Col([
            html.Label("Year Range:", style={'fontFamily': 'Roboto', 'color': 'white'}),
            dcc.RangeSlider(
                id='communism-year-slider',
                min=int(df['Year'].min()),
                max=int(df['Year'].max()),
                value=[int(df['Year'].min()), int(df['Year'].max())],
                marks={**{str(year): str(year) for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1) if year % 5 == 0},
                    str(df['Year'].min()): str(df['Year'].min()),
                    str(df['Year'].max()): str(df['Year'].max())},
                step=1,
                tooltip={"placement": "bottom", "always_visible": False}  # Tooltip to show the current value
            ),
        ], width=12)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='communism-sentiment-over-time-graph', style={'height': '400px', 'border': '1px solid #444'}),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='communism-high-low-indicator', style={'height': '400px', 'border': '1px solid #444'}),
        ], width=3),
        dbc.Col([
            dcc.Graph(id='communism-overall-sentiment-graph', style={'height': '400px', 'border': '1px solid #444'}),
        ], width=3),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='communism-emotion-graph', style={'height': '400px', 'border': '1px solid #444'}),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='communism-publication-graph', style={'height': '400px', 'border': '1px solid #444'}),
        ], width=6),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='communism-keyword-distribution-graph', style={'height': '400px', 'border': '1px solid #444'}),
        ], width=12)
    ], className="mb-4"),
], fluid=True, style={'backgroundColor': 'rgba(0, 51, 102, 0.8)', 'padding': '40px', 'borderRadius': '15px', 'marginTop': '20px', 'width': '100%'})


@callback(
    Output('communism-sentiment-over-time-graph', 'figure'),
    Output('communism-high-low-indicator', 'figure'),
    Output('communism-overall-sentiment-graph', 'figure'),
    Output('communism-emotion-graph', 'figure'),
    Output('communism-publication-graph', 'figure'),
    Output('communism-keyword-distribution-graph', 'figure'),
    [Input('communism-keyword-radio', 'value'),
     Input('communism-emotions-radio', 'value'),
     Input('communism-year-slider', 'value')]
)
def update_graphs(selected_keyword, selected_emotion, selected_years):
    # Filter the data based on the selected inputs
    filtered_df = df[
        (df['Year'] >= selected_years[0]) &
        (df['Year'] <= selected_years[1]) &
        (df['Keyword'] == selected_keyword)
    ]

    # Aggregate the data by year and keyword, taking the average sentiment score for each year
    aggregated_df = filtered_df.groupby(['Year', 'Keyword'])[selected_emotion].mean().reset_index()

    # Sentiment Over Time Graph (first graph)
    sentiment_over_time_fig = px.line(
        aggregated_df,
        x='Year',
        y=selected_emotion,
        color='Keyword',
        title=f'{selected_emotion.capitalize()} Sentiment Trend Over Time'
    )
    sentiment_over_time_fig.update_layout(
        plot_bgcolor='rgba(17, 17, 17, 0.7)',
        paper_bgcolor='rgba(10, 10, 10, 0.7)',
        font_color='white',
        title_font_color='white',
        xaxis={'showgrid': True, 'gridcolor': 'grey'},
        yaxis={'showgrid': True, 'gridcolor': 'grey'}
    )

    # High-Low Indicator (second graph)
    indicator = create_indicator(filtered_df, selected_emotion)

    # Overall Sentiment Graph (third graph)
    overall_sentiment_fig = px.pie(
        values=[filtered_df['Positive'].mean(), filtered_df['Negative'].mean()],
        names=['Positive', 'Negative'],
        title='Overall Sentiment'
    )
    overall_sentiment_fig.update_layout(
        paper_bgcolor='rgba(10, 10, 10, 0.7)',
        font_color='white',
        title_font_color='white'
    )

    # Top Emotions Graph (fourth graph)
    emotions_df = filtered_df[['Anger', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sadness', 'Surprise']].mean().nlargest(5)
    emotion_fig = px.bar(
        x=emotions_df.index,
        y=emotions_df.values,
        labels={'x': 'Emotions', 'y': 'Sentiment'},
        title=f'Top 5 Emotions for {selected_keyword.capitalize()}'
    )
    emotion_fig.update_layout(
        plot_bgcolor='rgba(17, 17, 17, 0.7)',
        paper_bgcolor='rgba(10, 10, 10, 0.7)',
        font_color='white',
        title_font_color='white',
        xaxis={'showgrid': True, 'gridcolor': 'grey'},
        yaxis={'showgrid': True, 'gridcolor': 'grey'}
    )

    # Top Publications Graph (fifth graph)
    top_publications_df = filtered_df.groupby('Publication')[selected_emotion].mean().nlargest(5)
    publication_fig = px.bar(
        x=top_publications_df.index,
        y=top_publications_df.values,
        labels={'x': 'Publications', 'y': f'{selected_emotion}'},
        title=f'Top 5 Publications for {selected_emotion.capitalize()} Sentiment'
    )
    publication_fig.update_layout(
        plot_bgcolor='rgba(17, 17, 17, 0.7)',
        paper_bgcolor='rgba(10, 10, 10, 0.7)',
        font_color='white',
        title_font_color='white',
        xaxis={'showgrid': True, 'gridcolor': 'grey'},
        yaxis={'showgrid': True, 'gridcolor': 'grey'}
    )

    # Keyword Distribution Graph (sixth graph)
    keyword_dist = filtered_df.groupby(['Year', 'Keyword']).size().reset_index(name='Count')
    keyword_dist_fig = px.bar(
        keyword_dist,
        x='Year',
        y='Count',
        color='Keyword',
        labels={'Count': 'Count of Observations'},
        title='Keyword Distribution Over Time'
    )
    keyword_dist_fig.update_layout(
        plot_bgcolor='rgba(17, 17, 17, 0.7)',
        paper_bgcolor='rgba(10, 10, 10, 0.7)',
        font_color='white',
        title_font_color='white',
        xaxis={'showgrid': True, 'gridcolor': 'grey'},
        yaxis={'showgrid': True, 'gridcolor': 'grey'}
    )

    return (
        sentiment_over_time_fig,
        indicator,
        overall_sentiment_fig,
        emotion_fig,
        publication_fig,
        keyword_dist_fig
    )