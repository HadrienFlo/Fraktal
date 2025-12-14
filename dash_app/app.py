"""Minimal Dash app using the fraktal library and dash-mantine-components.

This app is a skeleton. It demonstrates calling a function from the `fraktal` package and
showing results in the UI.
"""
from __future__ import annotations

import dash
from dash import Dash, Input, Output, State, callback, clientside_callback, ALL, callback_context
from dash_iconify import DashIconify
import dash_mantine_components as dmc

# from fraktal import load_default_config, time_and_memory


dash._dash_renderer._set_react_version("18.2.0")


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    title="Fraktal",
)
server = app.server


theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="radix-icons:sun", width=20, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]
    ),
    onLabel=DashIconify(
        icon="radix-icons:moon",
        width=20,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
    ),
    id="color-scheme-toggle",
    persistence=True,
    persistence_type="session",
    color=dmc.DEFAULT_THEME["colors"]["blue"][6],
    size="lg",
    checked=True,
)


layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group([
                dmc.Group([
                    dmc.Burger(
                        id="mobile-burger",
                        size="sm",
                        hiddenFrom="sm",
                        lineSize=3,
                        opened=True,
                        color=dmc.DEFAULT_THEME["colors"]["blue"][6],
                    ),
                    dmc.Burger(
                        id="desktop-burger",
                        size="sm",
                        visibleFrom="sm",
                        lineSize=3,
                        opened=False,
                        color=dmc.DEFAULT_THEME["colors"]["blue"][6],
                    ),
                    dmc.Title("Fraktal", c="blue", style={"margin-right": -16, "margin-left": 16}, className="app-title"),
                ], h="100%", px="md"),
                dmc.Group([
                    theme_toggle,
                ])
            ], justify="space-between", style={"flex": 1}, h="100%", px="md")
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                *[
                    dmc.NavLink(
                        label=f"{page['name']}", href=page["relative_path"], id={"type": "navlink", "index": page["relative_path"]},
                        variant="light",
                        color=dmc.DEFAULT_THEME["colors"]["blue"][6],
                        style={"fontWeight": "bold", "border-radius": "50px", "margin-bottom": "var(--mantine-spacing-sm)"},
                    )
                    for page in dash.page_registry.values()
                ],
            ],
            p="md",
        ),
        dmc.AppShellMain(children=dash.page_container),
    ],
    header={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(
    layout,
    theme={"fontFamily": "Montserrat, sans-serif", "defaultRadius": "md"},
)


@callback(
    Output("appshell", "navbar"),
    Input("mobile-burger", "opened"),
    Input("desktop-burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(mobile_opened, desktop_opened, navbar):
    navbar["collapsed"] = {
        "mobile": not mobile_opened,
        "desktop": not desktop_opened,
    }
    return navbar


@app.callback(
    Output({"type": "navlink", "index": ALL}, "active"), 
    Input("_pages_location", "pathname")
)
def update_navlinks(pathname):
    return [control["id"]["index"] == pathname for control in callback_context.outputs_list]


clientside_callback(
    """ 
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-toggle", "id"),
    Input("color-scheme-toggle", "checked"),
)


if __name__ == "__main__":
    app.run(debug=True)