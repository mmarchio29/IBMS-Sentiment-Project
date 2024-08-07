from dash import html, register_page

# Register the page with necessary attributes
register_page(
    __name__,
    name='error',
    title='404: Page Not Found',
    path='/404'
)

# Define the layout directly
layout = html.Div(className='error-page', children=[
    html.Img(src='/assets/images/dollarmask.jpg', className='header-icon'),
    html.H1("404: Page Not Found"),
    html.P("The page you are looking for does not exist."),
    html.A("Go back to the homepage", href="/", className="back-button"),
])