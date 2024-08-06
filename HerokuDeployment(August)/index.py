from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from app import app
import layouts.home as home_layout
import layouts.report as report
from components.common import get_header, get_footer

# Setup the application layout
app.layout = html.Div(className='main-container', children=[
    get_header(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    get_footer()
])

# Define the callback for dynamic page routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/report':
        return report.layout()
    return home_layout.layout() 

if __name__ == '__main__':
    app.run_server(debug=True)