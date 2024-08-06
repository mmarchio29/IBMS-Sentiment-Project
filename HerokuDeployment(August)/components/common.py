from dash import html

def get_header():
    return html.Div([
        html.A(
            html.Img(src='/assets/images/ibmslogo.png', className='header-logo'),
            href='/',  # Set this to the URL of the homepage
        )
    ], className='header')

def get_footer():
    return html.Div([
        html.Img(src='/assets/images/questromlogo.png', className='footer-logo'),
        html.P([
            'Contact us: ',
            html.A('karaca@bu.edu', href='mailto:karaca@bu.edu', className='footer-email'),
            ' ',
            html.A('zagorsky@bu.edu', href='mailto:zagorsky@bu.edu', className='footer-email')
        ])
    ], className='footer')