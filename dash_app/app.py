"""Minimal Dash app using the fraktal library and dash-mantine-components.

This app is a skeleton. It demonstrates calling a function from the `fraktal` package and
showing results in the UI.
"""
from __future__ import annotations

import dash
from dash import html, dcc
import dash_mantine_components as dmc
from dash.dependencies import Input, Output, State

from fraktal import load_default_config, time_and_memory

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dmc.theme.DEFAULT_THEME])
server = app.server

config = load_default_config()


@time_and_memory()
def run_heavy_calculation(n: int = 1000) -> dict:
    # Placeholder calculation — in real project replace with fractal computation
    total = 0
    for i in range(n):
        total += (i / (i + 1))
    return {"n": n, "result": total}


app.layout = dmc.Container([
    dmc.Title(config.get("app", {}).get("title", "Fraktal App")),
    dmc.Space(h=20),
    dmc.NumberInput(id="input-n", label="Iterations", value=config.get("calculation", {}).get("iterations", 1000)),
    dmc.Button("Run", id="run-btn"),
    dmc.Space(h=10),
    html.Div(id="output")
], size="lg")


@app.callback(Output("output", "children"), Input("run-btn", "n_clicks"), State("input-n", "value"))
def on_run(n_clicks, n):
    if not n_clicks:
        return "App ready. Click run to start calculation."
    res = run_heavy_calculation(int(n or 1000))
    return dmc.Prism(language="json", children=str(res))


if __name__ == "__main__":
    app.run_server(debug=True)
