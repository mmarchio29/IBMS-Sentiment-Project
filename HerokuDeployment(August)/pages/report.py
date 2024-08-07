from dash import html, dcc, callback, Input, Output, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Register the page with necessary attributes
register_page(
    __name__,
    name='report',
    title='Economic Ideology Sentiment Analysis Report',
    path='/report'
)

# Load data using data_manager
import data_manager as dm
df = dm.load_data()

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Economic Ideology Sentiment Analysis Report", className="text-center my-4", style={'font-family': 'Arial', 'color': 'white'})),
        ], justify="center"),
        dbc.Row([
            dbc.Col(html.A(html.Img(src='/assets/images/infoicon.svg', height='30px'), href='#', id='info-icon'), width=1, className="text-right")
        ]),
        dbc.Tooltip(
            [
                html.P("How to use this dashboard:", className="mb-2"),
                html.Br(),
                html.Ol([
                    html.Li("1. Select options such as source type, publisher, keyword, emotions, and aggregation value from the dropdown menus."),
                    html.Br(),
                    html.Li("2. Adjust the year range using the slider to filter the data based on the selected time frame."),
                    html.Br(),
                    html.Li("3. The graphs will automatically update to reflect your choices."),
                    html.Br(),
                    html.Li("4. Scroll down to explore additional visualizations and insights.")
                ], style={'text-align': 'left'})
            ],
            target="info-icon",
            placement="right"
        ),
        dbc.Row([
            dbc.Col([
                html.Label("Source Type:", style={'font-family': 'Arial', 'color': 'white'}),
                dcc.Dropdown(
                    id='source-type-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': st, 'value': st} for st in df['Source Type'].unique() if st],
                    value='All',
                    clearable=False,
                    multi=True
                ),
            ], width=6, md=3, className="text-center"),
            dbc.Col([
                html.Label("Publisher:", style={'font-family': 'Arial', 'color': 'white'}),
                dcc.Dropdown(
                    id='publisher-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': publisher, 'value': publisher} for publisher in df['Publication Title'].unique() if publisher],
                    value='All',
                    clearable=False,
                    multi=True
                ),
            ], width=6, md=3, className="text-center"),
            dbc.Col([
                html.Label("Keyword:", style={'font-family': 'Arial', 'color': 'white'}),
                dcc.Dropdown(
                    id='keyword-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': keyword, 'value': keyword} for keyword in df['Keyword'].unique() if keyword],
                    value='All',
                    clearable=False,
                    multi=True
                ),
            ], width=6, md=3, className="text-center"),
        ], className="mb-4 justify-content-center"),
        dbc.Row([
            dbc.Col([
                html.Label("Emotions:", style={'font-family': 'Arial', 'color': 'white'}),
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
                html.Label("Aggregation Value:", style={'font-family': 'Arial', 'color': 'white'}),
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
                html.Label("Year Range:", style={'font-family': 'Arial', 'color': 'white'}),
                dcc.RangeSlider(
                    id='year-slider',
                    min=int(df['Year'].min()),
                    max=int(df['Year'].max()),
                    value=[int(df['Year'].min()), int(df['Year'].max())],
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
                dcc.Graph(id='keyword-dist-graph', style={'height': '45vh'})
            ], width=12),
        ], className="mb-4"),
    ], fluid=True, style={'background-color': 'rgba(167, 24, 49, 0.6)', 'padding': '40px', 'border-radius': '10px', 'margin-top': '20px', 'width': '100vw'})
])

@callback(
    [Output('sentiment-line-graph', 'figure'),
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
    if 'All' not in selected_source:
        filtered_df = filtered_df[filtered_df['Source Type'].isin(selected_source)]
    if 'All' not in selected_publisher:
        filtered_df = filtered_df[filtered_df['Publication Title'].isin(selected_publisher)]
    if 'All' not in selected_keyword:
        filtered_df = filtered_df[filtered_df['Keyword'].isin(selected_keyword)]
    filtered_df = filtered_df[(filtered_df['Year'] >= selected_years[0]) & (filtered_df['Year'] <= selected_years[1])]
    
    # Apply dark theme settings
    dark_theme = {
        'plot_bgcolor': 'rgba(17, 17, 17, 0.7)',  # Dark grey background in the plot area
        'paper_bgcolor': 'rgba(10, 10, 10, 0.7)', # Darker grey around the plot area
        'font_color': 'white',                  # White text for visibility
        'title_font_color': 'white',            # White title
        'xaxis': {
            'showgrid': True,                   # Show gridlines
            'gridcolor': 'grey'                 # Gridline color
        },
        'yaxis': {
            'showgrid': True,
            'gridcolor': 'grey'
        }
    }

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
        line_fig.update_layout(**dark_theme)

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
    bar_fig.update_layout(**dark_theme)

    return line_fig, bar_fig