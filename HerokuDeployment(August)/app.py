from dash import Dash
import dash_auth
import dash_bootstrap_components as dbc

# Initialize the Dash app with pages support
app = Dash(
    __name__,
    use_pages=True,  # Enable multi-page support
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        '/assets/css/style.css',
        '/assets/css/style_report.css',
        '/assets/css/style_error.css',
    ]
)

# Get the Flask server instance
server = app.server

# Set the secret key for session management
server.secret_key = 'your_secret_key'  # Replace with a random string for production

# Define username and password pairs for authentication
VALID_USERNAME_PASSWORD_PAIRS = {
    'questrom': 'ibms'
}

# Apply basic authentication
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server