from bokeh.plotting import figure


def plot(x, counts, title):
    p = figure(plot_height=400, title=title, plot_width=400,
               toolbar_location=None, tools="")

    p.vbar(x=x, top=counts, width=0.9)
    p.yaxis.axis_label = "upvote"
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p
