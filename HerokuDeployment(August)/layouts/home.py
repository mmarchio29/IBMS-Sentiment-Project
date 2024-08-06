from dash import html, dcc

def layout():
    return html.Div([
        html.Div(className='header-topic', children=[
            html.H2("Economic Ideology Sentiment Analysis Report")
        ]),
        html.Div(className='header-section-parent', children=[
            html.Div(className='header-section', children=[
                html.Img(src='/assets/images/route.png', className='header-icon'),
                html.Div(className='header-section-text', children=[
                    html.H2("Navigate the Currents of Economic Sentiments", className='header-subtitle'),
                    html.P("Explore in-depth sentiment analysis across key economic ideologies like Capitalism, Socialism, and Communism.", className='header-body')
                ]),
                html.Div(className='header-section-button-box', children=[
                    dcc.Link('View Report', href='/report', className='header-section-button')
                ]),
            ]),
            html.Div(className='header-section-img',children=[
                
            ])
        ]),
        # Ideology Sections
        html.Div(className='ideology-section', children=[
            html.Div(className='ideology-section-one', children=[
                html.Div(className='ideology-block', children=[
                    html.Img(src='/assets/images/capitalism.png', className='ideology-icon'),
                    html.Div(className='ideology-block-header', children=[
                        html.H2("Capitalism")
                    ]),
                    html.Div(className='ideology-block-list', children=[
                        html.Ul(children=[
                            html.Li("Competitive markets"),
                            html.Li("Profit focus")
                        ])
                    ]),
                    dcc.Link("Maximize Profit", href='/capitalism', className='ideology-button')
                ]),
                html.Div(className='ideology-block', children=[
                    html.Img(src='/assets/images/socialism.png', className='ideology-icon'),
                    html.Div(className='ideology-block-header', children=[
                        html.H2("Socialism")
                    ]),
                    html.Div(className='ideology-block-list', children=[
                        html.Ul(children=[
                            html.Li("Regulated resources"),
                            html.Li("Social welfare")
                        ])
                    ]),
                    dcc.Link("Share Wealth", href='/socialism', className='ideology-button')
                ]),
                html.Div(className='ideology-block', children=[
                    html.Img(src='/assets/images/communism.png', className='ideology-icon'),
                    html.Div(className='ideology-block-header', children=[
                        html.H2("Communism")
                    ]),
                    html.Div(className='ideology-block-list', children=[
                        html.Ul(children=[
                            html.Li("Collective ownership"),
                            html.Li("Needs-based distribution")
                        ])
                    ]),
                    dcc.Link("Distribute Equally", href='/communism', className='ideology-button')
                ]),
            ]),
            html.Div(className='ideology-section-two', children=[
                html.Div(className='ideology-block', children=[
                    html.Img(src='/assets/images/imperialism.png', className='ideology-icon'),
                    html.Div(className='ideology-block-header', children=[
                        html.H2("Imperialism")
                    ]),
                    html.Div(className='ideology-block-list', children=[
                        html.Ul(children=[
                            html.Li("Territorial expansion"),
                            html.Li("Cultural influence")
                        ])
                    ]),
                    dcc.Link("Extend Influence", href='/imperialism', className='ideology-button')
                ]),
                html.Div(className='ideology-block', children=[
                    html.Img(src='/assets/images/colonialism.png', className='ideology-icon'),
                    html.Div(className='ideology-block-header', children=[
                        html.H2("Colonialism")
                    ]),
                    html.Div(className='ideology-block-list', children=[
                        html.Ul(children=[
                            html.Li("Economic colonization"),
                            html.Li("Cultural assimilation")
                        ])
                    ]),
                    dcc.Link("Examine Impact", href='/colonialism', className='ideology-button')
                ]),
                html.Div(className='ideology-block', children=[
                    html.Img(src='/assets/images/nationalism.png', className='ideology-icon'),
                    html.Div(className='ideology-block-header', children=[
                        html.H2("Nationalism")
                    ]),
                    html.Div(className='ideology-block-list', children=[
                        html.Ul(children=[
                            html.Li("Sovereignty"),
                            html.Li("National unity")
                        ])
                    ]),
                    dcc.Link("Strengthen Unity", href='/nationalism', className='ideology-button')
                ])
            ])
        ])
    ], className='main-container')