def gen_texas():
    from bokeh.io import show
    from bokeh.models import LogColorMapper
    from bokeh.palettes import Viridis6 as palette
    from bokeh.plotting import figure

    from bokeh.sampledata.us_counties import data as counties
    from bokeh.sampledata.unemployment import data as unemployment

    palette.reverse()

    counties = {
        code: county for code, county in counties.items() if county["state"] == "tx"
    }

    county_xs = [county["lons"] for county in counties.values()]
    county_ys = [county["lats"] for county in counties.values()]

    county_names = [county['name'] for county in counties.values()]
    county_rates = [unemployment[county_id] for county_id in counties]
    color_mapper = LogColorMapper(palette=palette)

    data=dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        rate=county_rates,
    )

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(
        title="Texas Unemployment, 2009", tools=TOOLS,
        x_axis_location=None, y_axis_location=None,
        tooltips=[
            ("Name", "@name"), ("Unemployment rate)", "@rate%"), ("(Long, Lat)", "($x, $y)")
        ])
    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    p.patches('x', 'y', source=data,
              fill_color={'field': 'rate', 'transform': color_mapper},
              fill_alpha=0.7, line_color="white", line_width=0.5)

    show(p)
    
def gen_mis():
    
    import numpy as np

    from bokeh.plotting import figure, show, output_file
    from bokeh.sampledata.les_mis import data

    nodes = data['nodes']
    names = [node['name'] for node in sorted(data['nodes'], key=lambda x: x['group'])]

    N = len(nodes)
    counts = np.zeros((N, N))
    for link in data['links']:
        counts[link['source'], link['target']] = link['value']
        counts[link['target'], link['source']] = link['value']

    colormap = ["#444444", "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99",
                "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a"]

    xname = []
    yname = []
    color = []
    alpha = []
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            xname.append(node1['name'])
            yname.append(node2['name'])

            alpha.append(min(counts[i,j]/4.0, 0.9) + 0.1)

            if node1['group'] == node2['group']:
                color.append(colormap[node1['group']])
            else:
                color.append('lightgrey')

    data=dict(
        xname=xname,
        yname=yname,
        colors=color,
        alphas=alpha,
        count=counts.flatten(),
    )

    p = figure(title="Les Mis Occurrences",
               x_axis_location="above", tools="hover,save",
               x_range=list(reversed(names)), y_range=names,
               tooltips = [('names', '@yname, @xname'), ('count', '@count')])

    p.plot_width = 800
    p.plot_height = 800
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/3

    p.rect('xname', 'yname', 0.9, 0.9, source=data,
           color='colors', alpha='alphas', line_color=None,
           hover_line_color='black', hover_color='colors')

    show(p) # show the plot
    
def gen_hex():
    
    import numpy as np

    from bokeh.io import output_file, show
    from bokeh.models import HoverTool
    from bokeh.plotting import figure

    n = 500
    x = 2 + 2*np.random.standard_normal(n)
    y = 2 + 2*np.random.standard_normal(n)

    p = figure(title="Hexbin for 500 points", match_aspect=True,
               tools="wheel_zoom,reset", background_fill_color='#440154')
    p.grid.visible = False

    r, bins = p.hexbin(x, y, size=0.5, hover_color="pink", hover_alpha=0.8)

    p.circle(x, y, color="white", size=1)

    p.add_tools(HoverTool(
        tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]
    ))

    show(p)