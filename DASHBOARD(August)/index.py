from dash import html, dcc
from dash import page_container
from components.common import get_header, get_footer
from components.navbar import create_navbar, nav_callback
from app import app  # Import the already initialized app from app.py
from data_manager import get_data

df = get_data()

# Set up the application layout
app.layout = dcc.Loading(
    html.Div(className='main-container', children=[
        get_header(),
        create_navbar(),  # Add the navbar here
        page_container,  # Automatically load the correct page based on the URL
        get_footer(),
        dcc.Location(id='url', refresh=False)
    ]),
    type="circle",
)

nav_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)