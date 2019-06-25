from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter


def plot(x, counts, title):
    p = figure(plot_height=400, title=title, plot_width=400,
               x_axis_type='datetime',
               toolbar_location=None, tools="")
    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    p.vbar(x=x, top=counts, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p
