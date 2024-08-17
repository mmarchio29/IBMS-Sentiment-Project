from dash import html

def get_header():
    return html.Div([
        html.A(
            html.Img(src='/assets/images/ibmslogo.png', className='header-logo'),
            href='/',
        ),
    ], className='header')

def get_footer():
    return html.Div([
        html.Div([
            html.Img(src='/assets/images/questromlogo.png', className='footer-logo'),
        ], className='footer-logo-container'),
        
        html.Div([
            html.A('© 2024 Questrom School of Business. All rights reserved.', className='footer-copyright'),
        ], className='footer-contact-container')
    ], className='footer')