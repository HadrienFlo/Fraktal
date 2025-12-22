"""Simple Mandelbrot page stub to restart from scratch."""

import dash
import dash_mantine_components as dmc
from dash import html, dcc

from components.tab_components.mandelbrot_form import form as mandelbrot_form # noqa: F401
from components.tab_components.render_tab_content import *  # noqa: F401
from components.tab_components.add_tab_to_store import *  # noqa: F401
from components.tab_components.sync_tabs_to_store import *  # noqa: F401

dash.register_page(__name__, name="Mandelbrot")

layout = dmc.Container([
    # Store for tabs data
    dcc.Store(id="tabs-store", data={"form-tab": mandelbrot_form}, storage_type="session"),
    # 
    dmc.Title("Mandelbrot", order=1, mt="lg", mb="lg"),
    # Tabs component
    html.Div(
        children=[
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab("Form tab", value="form-tab"),
                        ]
                    ),
                ],
                id="tabs",
                value="form-tab",
            ),
            html.Div(id="tabs-content", style={"paddingTop": 10}),
        ]
    )
], size="xl", py="lg")