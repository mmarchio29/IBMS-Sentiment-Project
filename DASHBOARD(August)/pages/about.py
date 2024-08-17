from dash import html, dcc, register_page
import dash_bootstrap_components as dbc

# Register the page with Dash
register_page(
    __name__,
    name='About',
    title='Mehrotra IBMS',
    path='/about'
)

# Layout for the About page
layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.Img(src='/assets/images/about.png', className="about-image")]),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(html.H1("About Economic Ideology Sentiment Project - REQUIRE EDITING", className="about-title")),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H3(
                """
                This dashboard is designed to provide in-depth sentiment analysis across various economic ideologies.
                By leveraging data from numerous publications, this tool enables users to explore trends and distributions 
                of sentiments over time. The dashboard allows for comprehensive analysis by breaking down sentiments into 
                positive and negative categories, tracking keywords, and examining sentiment across different sources.
                """, 
                className="about-text"
            ),
            html.H3(
                """
                Whether you are a researcher, a student, or just curious about the shifts in public opinion over time, 
                this dashboard offers valuable insights into how sentiments evolve in relation to capitalism, socialism, 
                and other ideologies. Explore the visualizations, adjust filters, and uncover trends that have shaped 
                our worldviews over the decades.
                """,
                className="about-text"
            ),
            html.H3(
                """
                The dashboard is built using Python, Dash, and Plotly, ensuring a smooth and interactive user experience. 
                With a modern design and easy navigation, it’s accessible to everyone from data enthusiasts to academic professionals.
                """,
                className="about-text"
            ),
        ], width=10),
    ], className="mb-5", style={'align-items': 'center', 'justify-content': 'center'}),
    
    html.Hr(className="about-divider"),

    dbc.Row([
        dbc.Col(html.H3("Key Features", className="about-subtitle"), width=12),
    ], className="mb-3"),
    
    dbc.Row([
        dbc.Col([
            html.Ul([
                html.Li("Sentiment Analysis across multiple economic ideologies", className="about-list"),
                html.Li("Interactive visualizations and filters", className="about-list"),
                html.Li("Analysis of keyword trends over time", className="about-list"),
                html.Li("Insights into the distribution of sentiments by sources", className="about-list"),
                html.Li("Built with Dash, Plotly, and Bootstrap for a modern UI", className="about-list")
            ])
        ], width=15)
    ], className="mb-5", style={'align-items': 'center', 'justify-content': 'center'}),

    html.Hr(className="about-divider"),

    dbc.Row([
        dbc.Col(html.H2("Contributors", className="about-subtitle"), width=12),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Ul([
                html.Li("Marcel Rindisbacher - Director - rindisbm@bu.edu", className="about-list"),
                html.Li("Jay L. Zagorsky - Professor - zagorsky@bu.edu", className="about-list"),
                html.Li("Sami H. Karaca - Professor - karaca@bu.edu", className="about-list"),
                html.Li("David E. Kim - Assistant - dk98@bu.edu", className="about-list"),
                html.Li("Madison Marchionna - Assistant - mmarchio@bu.edu", className="about-list")
            ])
        ], width=15)
    ], className="mb-5", style={'align-items': 'center', 'justify-content': 'center'}),

    html.Hr(className="about-divider"),

    dbc.Row([
        dbc.Col(html.H2("Get In Touch", className="about-subtitle"), width=12),
    ], className="mb-3"),
    
    dbc.Row([
        dbc.Col([
            html.H3("If you have any questions or feedback, feel free to reach out via email at ", className="about-contact"),
            html.A("zagorsky@bu.edu", href="mailto:zagorsky@bu.edu", className="about-contact-link"),
            html.Span(" & ", className="about-contact"),
            html.A("karaca@bu.edu", href="mailto:karaca@bu.edu", className="about-contact-link")
        ], width=10)
    ], className="mb-5", style={'align-items': 'center', 'justify-content': 'center'}),
    
    html.Hr(className="about-divider"),

], fluid=True, className="about-container")