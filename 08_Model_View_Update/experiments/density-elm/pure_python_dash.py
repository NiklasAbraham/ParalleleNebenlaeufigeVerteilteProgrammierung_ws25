import numpy as np
import plotly.graph_objects as go

# Reuse the same KDE+contour function from backend/main.py
from backend.main import compute_contours_payload, sample_points
from dash import Dash, Input, Output, dcc, html

PTS = sample_points()

app = Dash(__name__)
app.layout = html.Div(
    style={"fontFamily": "system-ui", "padding": "16px", "maxWidth": "920px"},
    children=[
        html.Div(
            style={"display": "flex", "gap": "24px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    children=[
                        html.Div("Bandwidth"),
                        dcc.Slider(0.2, 8.0, 0.1, value=2.0, id="bw"),
                    ],
                    style={"minWidth": "280px"},
                ),
                html.Div(
                    children=[
                        html.Div("Levels"),
                        dcc.Slider(3, 40, 1, value=15, id="levels"),
                    ],
                    style={"minWidth": "280px"},
                ),
            ],
        ),
        dcc.Graph(id="fig", style={"height": "560px"}),
    ],
)


@app.callback(
    Output("fig", "figure"),
    Input("bw", "value"),
    Input("levels", "value"),
)
def update(bandwidth, levels):
    payload = compute_contours_payload(
        PTS, float(bandwidth), int(levels), grid_size=200
    )

    fig = go.Figure()

    # scatter points
    pts = np.array(payload["points"])
    fig.add_trace(
        go.Scatter(
            x=pts[:, 0],
            y=pts[:, 1],
            mode="markers",
            marker={"size": 5, "opacity": 0.5},
            name="points",
        )
    )

    # contour polylines
    for c in payload["contours"]:
        for path in c["paths"]:
            arr = np.array(path)
            fig.add_trace(
                go.Scatter(
                    x=arr[:, 0],
                    y=arr[:, 1],
                    mode="lines",
                    line={"width": 1.2},
                    name=f"level {c['level']:.4g}",
                    showlegend=False,
                )
            )

    fig.update_layout(margin={"l": 20, "r": 20, "t": 20, "b": 20})
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
