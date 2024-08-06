from dash import html, dcc

def layout():
    return html.Div([
        html.H1('Home Page', className='home-title'),
        dcc.Link('Go to Analysis', href='/main-analysis', className='link-button')
    ], className='page-content')