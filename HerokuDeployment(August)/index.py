from dash import html, dcc
from dash import page_container
from components.common import get_header, get_footer
from app import app  # Import the already initialized app from app.py

# Set up the application layout
app.layout = dcc.Loading(
    html.Div(className='main-container', children=[
        get_header(),
        page_container,  # Automatically load the correct page based on the URL
        get_footer()
    ]),
    type="circle",
)

if __name__ == '__main__':
    app.run_server(debug=True)