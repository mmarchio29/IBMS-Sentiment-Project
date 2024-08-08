from dash import html, dcc, register_page

# Register the page with the path and additional options
register_page(
    __name__,
    name='home',
    top_nav=True,
    title='Mehrotra Institute - Economic Sentiment',
    path='/'
)

def create_ideology_block(icon, title, items, link_text, href):
    return html.Div(className='ideology-block', children=[
        html.Img(src=f'/assets/images/{icon}.png', className='ideology-icon'),
        html.Div(className='ideology-block-header', children=[
            html.H3(title)
        ]),
        html.Div(className='ideology-block-list', children=[
            html.Ul(children=[html.Li(item) for item in items])
        ]),
        dcc.Link(link_text, href=href, className='ideology-button')
    ])

# Define the layout directly
layout = html.Div(className='main-container', children=[
    html.Div(className='header-topic', children=[
        html.H2("Economic Ideology Sentiment Analysis Report")
    ]),
    html.Div(className='header-section-parent', children=[
        html.Div(className='header-section', children=[
            html.Img(src='/assets/images/route.png', className='header-icon'),
            html.Div(className='header-section-text', children=[
                html.H1([
                    "Navigate the Currents of",
                    html.Br(),
                    "Economic Sentiments"
                ]),
                html.H3([
                    "Explore in-depth sentiment analysis",
                    html.Br(),
                    "across key economic ideologies",
                    html.Br(),
                    "like Capitalism, Socialism, and Communism."
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
                title='Other',
                items=['Have ideas to share?', 'We’d love to hear.'],
                link_text='Reach Out to Us',
                href='#bottom'
            )
        ])
    ])
])