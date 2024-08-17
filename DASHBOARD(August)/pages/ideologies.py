from dash import html, dcc, callback, Input, Output, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
from data_manager import get_data

# Register the page with necessary attributes
register_page(
    __name__,
    name='ideologies',
    title='Mehrotra IBMS',
    path='/comparative/ideologies'
)

df = get_data()

# Define reusable components
def create_dropdown(id, label, options, value, multi=False):
    return html.Div([
        html.Label(label, style={'fontFamily': 'Roboto', 'color': 'white'}),
        dcc.Dropdown(
            id=id,
            options=options,
            value=value,
            clearable=False,
            multi=multi
        )
    ], className="mb-3")

# Define layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.A(html.Img(src='../assets/images/info.png', height='70px'), href='#', id='info-icon'), width=1, className="text-right")
    ]),
    dbc.Row([
        dbc.Col(html.H2("Economic Ideology Sentiment Analysis Report", className="text-center my-4", style={'fontFamily': 'Roboto', 'color': 'white'})),
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
        target="info-icon",
        placement="right"
    ),
    dbc.Row([
        dbc.Col(create_dropdown('publication-type-dropdown', "Publication:", 
                                [{'label': 'All', 'value': 'All'}] + [{'label': st, 'value': st} for st in df['Publication'].unique() if st],
                                'All', multi=True), width=9, md=3),
        dbc.Col(create_dropdown('keyword-dropdown', "Keyword:", 
                                [{'label': 'All', 'value': 'All'}] + [{'label': keyword, 'value': keyword} for keyword in df['Keyword'].unique() if keyword],
                                'All', multi=True), width=9, md=3),
        dbc.Col(create_dropdown('emotions-dropdown', "Emotions:", 
                                [{'label': emotion, 'value': emotion} for emotion in ['Positive', 'Negative', 'Anger', 'Disgust', 'Fear', 'Sadness', 'Happiness', 'Love', 'Surprise', 'Neutral', 'Other']],
                                ['Positive', 'Negative'], multi=True), width=9, md=3),
        dbc.Col(create_dropdown('aggregation-dropdown', "Aggregation Value:", 
                                [{'label': label, 'value': value} for label, value in [
                                    ('Average Sentiment', 'mean'),
                                    ('Median Sentiment', 'median'),
                                    ('Max Sentiment', 'max'),
                                    ('Min Sentiment', 'min'),
                                    ('5-Year Rolling Average', 'rolling_mean')
                                ]],
                                'mean'), width=9, md=3),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            html.Label("Year Range:", style={'fontFamily': 'Roboto', 'color': 'white'}),
            dcc.RangeSlider(
                id='year-slider',
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
            html.Div(id='graph-container')
        ], width=12),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='keyword-dist-graph', style={'height': '400px'})
        ], width=12),
    ], className="mb-4"),
], fluid=True, style={'backgroundColor': 'rgba(0, 51, 102, 0.8)', 'padding': '40px', 'borderRadius': '15px', 'marginTop': '20px', 'width': '100%'})


# Define callback
@callback(
    [Output('graph-container', 'children'),
     Output('keyword-dist-graph', 'figure')],
    [Input('publication-type-dropdown', 'value'),
     Input('keyword-dropdown', 'value'),
     Input('emotions-dropdown', 'value'),
     Input('aggregation-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graphs(selected_publication, selected_keyword, selected_emotions, aggregation_value, selected_years):
    filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
    
    if 'All' not in selected_publication:
        filtered_df = filtered_df[filtered_df['Publication'].isin(selected_publication)]
    if 'All' not in selected_keyword:
        filtered_df = filtered_df[filtered_df['Keyword'].isin(selected_keyword)]
    
    # Apply dark theme settings
    dark_theme = {
        'plot_bgcolor': 'rgba(17, 17, 17, 0.7)',
        'paper_bgcolor': 'rgba(10, 10, 10, 0.7)',
        'font_color': 'white',
        'title_font_color': 'white',
        'xaxis': {'showgrid': True, 'gridcolor': 'grey'},
        'yaxis': {'showgrid': True, 'gridcolor': 'grey'}
    }

    if filtered_df.empty or not set(selected_emotions).issubset(filtered_df.columns):
        return [html.Div("No data available for the selected filters.")], px.bar(title="No data available for the selected filters.")

    # Prepare data for graphs
    filtered_df_numeric = filtered_df[['Date', 'Year', 'Keyword'] + selected_emotions].set_index('Date')
    if aggregation_value == 'rolling_mean':
        filtered_df_numeric = filtered_df_numeric.groupby(['Year', 'Keyword']).mean().rolling(window=5, min_periods=1).mean().reset_index()
    else:
        filtered_df_numeric = filtered_df_numeric.groupby(['Year', 'Keyword']).agg(aggregation_value).reset_index()

    # Function to create a single sentiment graph
    def create_sentiment_graph(emotion):
        fig = px.line(
            filtered_df_numeric,
            x='Year',
            y=emotion,
            color='Keyword',
            line_group='Keyword',
            labels={'Year': 'Year', 'value': 'Sentiment Score'},
            title=f'{emotion} Sentiment Trend from {selected_years[0]} to {selected_years[1]}'
        )
        fig.update_layout(**dark_theme)
        return dcc.Graph(figure=fig, style={'height': '400px'})

    # Create a list of graphs for each selected emotion
    sentiment_graphs = [create_sentiment_graph(emotion) for emotion in selected_emotions]

    # Keyword Distribution Graph
    keyword_dist = filtered_df.groupby(['Year', 'Keyword']).size().reset_index(name='Count')
    bar_fig = px.bar(
        keyword_dist,
        x='Year',
        y='Count',
        color='Keyword',
        labels={'Count': 'Count of Observations'},
        title='Keyword Distribution Over Time'
    )
    bar_fig.update_layout(**dark_theme)

    return sentiment_graphs, bar_fig