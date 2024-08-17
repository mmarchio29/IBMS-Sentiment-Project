from dash import html, dcc, callback, Input, Output, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
from data_manager import get_data, get_consumer

# Register the page with necessary attributes
register_page(
    __name__,
    name='consumer report',
    title='Mehrotra IBMS',
    path='/comparative/consumer'
)

df = get_data()
consumer_df = get_consumer()

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
        dbc.Col(html.A(html.Img(src='../assets/images/info.png', height='70px'), href='#', id='consumer-info-icon'), width=1, className="text-right")
    ]),
    dbc.Row([
        dbc.Col(html.H2("Economic Ideology Sentiment v. Consumer Sentiment", className="text-center my-4", style={'fontFamily': 'Roboto', 'color': 'white'})),
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
        target="consumer-info-icon",
        placement="right"
    ),
    dbc.Row([
        dbc.Col(create_dropdown('consumer-publication-type-dropdown', "Publication:", 
                                [{'label': 'All', 'value': 'All'}] + [{'label': st, 'value': st} for st in df['Publication'].unique() if st],
                                'All', multi=True), width=9, md=3),
        dbc.Col(create_dropdown('consumer-keyword-dropdown', "Keyword:", 
                                [{'label': 'All', 'value': 'All'}] + [{'label': keyword, 'value': keyword} for keyword in df['Keyword'].unique() if keyword],
                                'All', multi=True), width=9, md=3),
        dbc.Col(create_dropdown('consumer-emotions-dropdown', "Emotions:", 
                                [{'label': emotion, 'value': emotion} for emotion in ['Positive', 'Negative', 'Anger', 'Disgust', 'Fear', 'Sadness', 'Happiness', 'Love', 'Surprise', 'Neutral', 'Other']],
                                ['Positive', 'Negative'], multi=True), width=9, md=3),
        dbc.Col(create_dropdown('consumer-aggregation-dropdown', "Aggregation Value:", 
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
                id='consumer-year-slider',
                min=int(consumer_df['Year'].min()),
                max=int(consumer_df['Year'].max()),
                value=[int(consumer_df['Year'].min()), int(consumer_df['Year'].max())],
                marks={**{str(year): str(year) for year in range(int(consumer_df['Year'].min()), int(consumer_df['Year'].max()) + 1) if year % 5 == 0},
                    str(consumer_df['Year'].min()): str(consumer_df['Year'].min()),
                    str(consumer_df['Year'].max()): str(consumer_df['Year'].max())},
                step=1,
                tooltip={"placement": "bottom", "always_visible": False}  # Tooltip to show the current value
            ),
        ], width=12)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            html.Div(id='consumer-graph-container')
        ], width=12),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='consumer-umcsent-trend-graph', style={'height': '400px'})
        ], width=12),
    ], className="mb-4"),
], fluid=True, style={'backgroundColor': 'rgba(0, 51, 102, 0.8)', 'padding': '40px', 'borderRadius': '15px', 'marginTop': '20px', 'width': '100%'})


# Define callback
@callback(
    [Output('consumer-graph-container', 'children'),
     Output('consumer-umcsent-trend-graph', 'figure')],
    [Input('consumer-publication-type-dropdown', 'value'),
     Input('consumer-keyword-dropdown', 'value'),
     Input('consumer-emotions-dropdown', 'value'),
     Input('consumer-aggregation-dropdown', 'value'),
     Input('consumer-year-slider', 'value')]
)
def update_consumer_graphs(selected_publication, selected_keyword, selected_emotions, aggregation_value, selected_years):
    # Filter the main df data based on selected years
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
        return [html.Div("No data available for the selected filters.")], px.line(title="No data available for the selected filters.")

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
    
    # UMCSENT Trend Graph using consumer_df
    consumer_filtered_df = consumer_df[(consumer_df['Year'] >= selected_years[0]) & (consumer_df['Year'] <= selected_years[1])]

    # Ensure the dataframe is sorted by Year before plotting
    consumer_filtered_df = consumer_filtered_df.sort_values(by='Year')

    umcsent_fig = px.line(
        consumer_filtered_df,
        x='Year',
        y='UMCSENT',
        labels={'Year': 'Year', 'UMCSENT': 'Consumer Sentiment'},
        title='Consumer Sentiment Trend Over Time'
    )
    umcsent_fig.update_layout(**dark_theme)

    return sentiment_graphs, umcsent_fig