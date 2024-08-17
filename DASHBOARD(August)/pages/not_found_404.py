from dash import html, register_page

register_page(__name__)

# Define the layout directly
layout = html.Div(className='error-page', children=[
    html.Div(className='error-content', children=[
        html.Img(src='/assets/images/franklin.png', className='header-icon'),
        html.H1("404: Oops, a Penny Lost!", className="error-title"),
        html.H3("“A penny saved is a penny earned” - Benjamin Franklin", className="error-quote"),
        html.H4("But it looks like we misplaced this page.", className="error-message"),
        html.H4("Don’t worry, you’re not losing any pennies—just a few seconds of your time.", 
                className="error-message", style={'padding-bottom': '50px'}),
        html.A("Return Home", href="/", className="back-button"),
    ]),
])