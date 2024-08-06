from dash import html, dcc

def layout():
    return html.Div([
        html.H1('Here is the main analysis report', className='home-title'),
        dcc.Link('Go back', href='/', className='link-button')
    ], className='page-content')