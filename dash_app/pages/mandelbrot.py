"""Simple Mandelbrot page stub to restart from scratch."""

import dash
from dash import html, dcc
import dash_mantine_components as dmc

from components.tab_components.render_tab_content import *  # noqa: F401
from components.tab_components.add_tab_to_store import *  # noqa: F401
from components.tab_components.sync_tabs_to_store import *  # noqa: F401

dash.register_page(__name__, name="Mandelbrot")


form = dmc.Container(
    [
        dmc.TextInput(label="This is a placeholder for the Mandelbrot form.", id="text-input", my=10),
        dmc.Group([
            dmc.Button("Submit", id="submit-button", variant="outline", my=10),
            dmc.Button("Add Tab", id="add-tab-button", variant="outline", my=10),
        ]),
    ],
    id="form-container",
    size="sm", py="lg"
)

layout = dmc.Container([
    # Store for tabs data
    dcc.Store(id="tabs-store", data={"form-tab": form}),
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