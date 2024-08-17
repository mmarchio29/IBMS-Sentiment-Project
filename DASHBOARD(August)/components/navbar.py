import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0, className="custom-toggler"),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.DropdownMenu(
                                label="About",
                                nav=True,
                                in_navbar=True,
                                children=[
                                    dbc.DropdownMenuItem("The Project", href="/about"),
                                    dbc.DropdownMenuItem("Mehrotra Institute", href="https://ibms.bu.edu/", target="_blank"),
                                    dbc.DropdownMenuItem("Questrom Business School", href="https://www.bu.edu/questrom/", target="_blank"),
                                    dbc.DropdownMenuItem("Boston University", href="https://www.bu.edu/", target="_blank"),
                                ],
                                className="dropdown-menu-right"
                            ),
                            dbc.DropdownMenu(
                                label="Comparative",
                                nav=True,
                                in_navbar=True,
                                children=[
                                    dbc.DropdownMenuItem("Ideologies", href="/comparative/ideologies"),
                                    dbc.DropdownMenuItem("Consumer", href="/comparative/consumer"),
                                    dbc.DropdownMenuItem("Market", href="/comparative/market"),
                                    dbc.DropdownMenuItem("Inflation", href="/comparative/inflation"),
                                    dbc.DropdownMenuItem("Unemployment", href="/comparative/unemployment"),
                                    dbc.DropdownMenuItem("Wage", href="/comparative/wage"),
                                ],
                                className="dropdown-menu-right"
                            ),
                            dbc.DropdownMenu(
                                label="Capitalism",
                                nav=True,
                                in_navbar=True,
                                children=[
                                    dbc.DropdownMenuItem("Dashboard", href="/capitalism/dashboard"),
                                    dbc.DropdownMenuItem("Report", href="/capitalism/report")
                                ],
                                className="dropdown-menu-right"
                            ),
                            dbc.DropdownMenu(
                                label="Socialism",
                                nav=True,
                                in_navbar=True,
                                children=[
                                    dbc.DropdownMenuItem("Dashboard", href="/socialism/dashboard"),
                                    dbc.DropdownMenuItem("Report", href="/socialism/report")
                                ],
                                className="dropdown-menu-right"
                            ),
                            dbc.DropdownMenu(
                                label="Communism",
                                nav=True,
                                in_navbar=True,
                                children=[
                                    dbc.DropdownMenuItem("Dashboard", href="/communism/dashboard"),
                                    dbc.DropdownMenuItem("Report", href="/communism/report")
                                ],
                                className="dropdown-menu-right"
                            ),
                            dbc.DropdownMenu(
                                label="Colonialism",
                                nav=True,
                                in_navbar=True,
                                children=[
                                    dbc.DropdownMenuItem("Dashboard", href="/colonialism/dashboard"),
                                    dbc.DropdownMenuItem("Report", href="/colonialism/report")
                                ],
                                className="dropdown-menu-right"
                            ),
                            dbc.DropdownMenu(
                                label="Imperialism",
                                nav=True,
                                in_navbar=True,
                                children=[
                                    dbc.DropdownMenuItem("Dashboard", href="/imperialism/dashboard"),
                                    dbc.DropdownMenuItem("Report", href="/imperialism/report")
                                ],
                                className="dropdown-menu-right"
                            ),
                        ],
                        className="ms-auto",
                        navbar=True
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ],
            fluid=True,  # Ensure the container stretches across the width
            className="navbar-container",
        ),
        color="dark",
        dark=True,
        expand="lg",
        className="custom-navbar mb-0",
    )

# Callback for toggling the collapse on small screens
def nav_callback(app):
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open