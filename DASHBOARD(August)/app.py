from dash import Dash
# import dash_auth
import dash_bootstrap_components as dbc

# Initialize the Dash app with pages support
app = Dash(
    __name__,
    use_pages=True,  # Enable multi-page support
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        '/assets/css/style_header_footer.css',
        '/assets/css/style_home.css',
        '/assets/css/style_dashboard.css',
        '/assets/css/style_error.css',
        '/assets/css/style_navbar.css',
        '/assets/css/style_individual.css',
        '/assets/css/style_about.css'
    ],
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
    ]
)

# # Get the Flask server instance
# server = app.server

# # Set the secret key for session management
# server.secret_key = 'your_secret_key'  # Replace with a random string for production

# # Define username and password pairs for authentication
# VALID_USERNAME_PASSWORD_PAIRS = {
#     'questrom': 'ibms'
# }

# # Apply basic authentication
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )