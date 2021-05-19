import pandas
import altair


def mark_blurred_line(chart, n_glows=10, base_opacity=0.5):
    opacity = base_opacity/n_glows
    glows = (
        chart.mark_line(opacity=opacity, strokeWidth=2 + (1.05 * i))
        for i in range(1, n_glows + 1)
    )
    return altair.layer(*glows)


def synthwave():
    background = "#efefef" 
    grid =       "#ffffff"       
    text =       "#444444"       
    line_colors = [
        "#228C22",         
        "#5f249f",
        "#FF0000",
        "#ffff00",
        "#00FFFF",
        "#000000",
        "#FFFFFF"
    ]

    return {
        "config": {
            "view": {
                "continuousWidth": 800,
                "continuousHeight": 400
            },
            "background": background,
            "axis": {
                "gridColor": grid,
                "domainColor": None,
                "tickColor": None,
                "labelColor": text,
                "titleColor": text
            },
            "legend": {
                "labelColor": text,
                "titleColor": text
            },
            "range": {
                "category": line_colors
            },
            "area": {
                "line": True,
                "fillOpacity": 0.4
            },
            "line": {
                "strokeWidth": 2
            }
        }
    }

def prepare(cases, arg, tpl):
    return [(dt['x'], dt[arg], dt['label']) for dt in cases], tpl

def plotter(*args):
    x, label = prepare(*args)
    df = pandas.DataFrame({"x": [el[0] for el in x], "y": [el[1] for el in x], "z": [el[2] for el in x]})

    chart = altair.Chart(df).encode(
        x=altair.X("x", title=label[0], axis=altair.Axis(tickMinStep=1)),
        y=altair.Y("y", title=label[1]),
        color=altair.Color("z:N", title=label[2])
    ).mark_line()

    altair.themes.register("synthwave", synthwave)
    altair.themes.enable("synthwave")
    fill = chart.mark_area()
    blur = mark_blurred_line(chart)
    return altair.layer(fill, blur)
