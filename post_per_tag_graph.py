from bokeh.plotting import figure


def plot(x, counts, title):
    p = figure(width=800, height=600, y_range=x, title=title)

    p.background_fill_color = "#EAEAF2"

    p.grid.grid_line_alpha=1.0
    p.grid.grid_line_color = "white"

    p.xaxis.axis_label = 'totale'
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.major_label_text_font_size = '14pt'
    #p.x_range = Range1d(0,50)
    #p.xaxis[0].ticker=FixedTicker(ticks=[i for i in xrange(0,5,1)])

    p.yaxis.major_label_text_font_size = '14pt'
    p.yaxis.axis_label = 'tags'

    p.yaxis.axis_label_text_font_size = '14pt'


    j = 0.5
    for k,v in zip(x,counts):

        p.rect(x=v/2, y=j, width=abs(v), height=0.4,color=(76,114,176),
               width_units="data", height_units="data")
        j += 1
    return p