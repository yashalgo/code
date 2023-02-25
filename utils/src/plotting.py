import plotly.graph_objects as go


def save_plot(group, imgname):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=group["DateTime"],
                open=group["open"],
                high=group["high"],
                low=group["low"],
                close=group["close"],
            ),
            go.Scatter(x=group["DateTime"], y=group["vwap"]),
        ]
    )
    fig.update_xaxes(rangeslider_visible=False)
    # fig.update_yaxes(visible = False)
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )
    fig["data"][1]["line"]["color"] = "#0000FF"
    fig.write_image(imgname + ".png")
