from dash import html, dcc, register_page
from dash_extensions import Lottie  # Import Lottie component

# Register the page with the path and additional options
register_page(
    __name__,
    name='home',
    top_nav=True,
    title='Mehrotra IBMS',
    path='/'
)

# Define Lottie options
lottie_options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

def create_ideology_block(icon, title, items, link_text, href):
    # Use dcc.Link for internal links and html.A for external links
    if href.startswith('http'):
        link_component = html.A(link_text, href=href, className='ideology-button', target="_blank")
    else:
        link_component = dcc.Link(link_text, href=href, className='ideology-button')

    return html.Div(className='ideology-block', children=[
        html.Img(src=f'/assets/images/{icon}.png', className='ideology-icon'),
        html.Div(className='ideology-block-header', children=[
            html.H3(title)
        ]),
        html.Div(className='ideology-block-list', children=[
            html.Ul(children=[html.Li(item) for item in items])
        ]),
        link_component
    ])

# Define the layout directly
layout = html.Div(className='home-container', children=[
    html.Div(className='header-topic', children=[
        html.H2("Economic Ideology Sentiment Analysis Report")
    ]),
    html.Div(className='header-section-parent', children=[
        html.Div(className='header-section', children=[
                Lottie(options=lottie_options, url="https://lottie.host/2a6af053-ad2e-4dd5-a2ac-eb5d568e9e27/2sSaLKwxst.json", width="150px", height="150px"),
                html.Div(className='header-section-text', children=[
                html.H1([
                    "Navigate the Currents of",
                    html.Br(),
                    "Economic Sentiments"
                ]),
                html.H3([
                    "Explore in-depth sentiment analysis across key economic",
                    html.Br(),
                    "ideologies like Capitalism, Socialism, and Communism.",
                ])
            ]),
            html.Div(className='header-section-button-box', children=[
                dcc.Link('View Report', href='/report', className='header-section-button')
            ])
        ]),
        html.Div(className='header-section-img')
    ]),
    html.Div(className='ideology-section', children=[
        html.Div(className='ideology-section-one', children=[
            create_ideology_block(
                icon='capitalism',
                title='Capitalism',
                items=['Competitive Markets', 'Profit Focused'],
                link_text='Maximize Profit',
                href='/capitalism'
            ),
            create_ideology_block(
                icon='socialism',
                title='Socialism',
                items=['Regulated Resources', 'Social Welfare'],
                link_text='Share Wealth',
                href='/socialism'
            ),
            create_ideology_block(
                icon='communism',
                title='Communism',
                items=['Collective Ownership', 'Targeted Allocation'],
                link_text='Distribute Equally',
                href='/communism'
            )
        ]),
        html.Div(className='ideology-section-two', children=[
            create_ideology_block(
                icon='imperialism',
                title='Imperialism',
                items=['Territorial Expansion', 'Cultural Influence'],
                link_text='Extend Influence',
                href='/imperialism'
            ),
            create_ideology_block(
                icon='colonialism',
                title='Colonialism',
                items=['Economic Colonization', 'Cultural Assimilation'],
                link_text='Examine Impact',
                href='/colonialism'
            ),
            create_ideology_block(
                icon='more',
                title='Discover',
                items=['Ravi K. Mehrotra', 'Institute for BMS'],
                link_text='Learn More',
                href='https://ibms.bu.edu/'
            )
        ])
    ])
])
