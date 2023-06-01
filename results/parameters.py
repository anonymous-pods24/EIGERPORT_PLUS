import numpy as np

# parameters for plot
title_font = 60
axis_font = 70
tick_font = 60
title_info = {'fontsize': title_font,
            'fontweight' : "bold",
            'verticalalignment': 'baseline',
            'horizontalalignment': "center"}

marker_size = 30
line_width = 2.5
tick_font_inaxis = 15
haveGrid = False
showPlot = True
bar_width = 0.2
allBar = False
normalize = False
# edit this if you want to change the algorithms you can plot
algorithms = ["EIGER", "EIGER_PORT", "EIGER_PORT_PLUS"]
# save the images as pdfs here
saveTo = "/home/luca/ETH/Thesis/EIGERPORT+/results/"

if normalize:
    saveTo += "normalized/"
    algorithms = ["EIGER_PORT", "EIGER_PORT_PLUS"]

colors = {
    "EIGER": "#1f77b4",
    "EIGER_PORT": "#ff7f0e",
    "EIGER_PORT_PLUS": "#2ca02c",
}

bar_line_width = 1.5

is_full = {
    "EIGER": True,
    "EIGER_PORT": False,
    "EIGER_PORT_PLUS": False,
}

bar_markers = {
    "EIGER": "",
    "EIGER_PORT": "/",
    "EIGER_PORT_PLUS": "+",
}

markers = {
    "EIGER": "o",
    "EIGER_PORT": "s",
    "EIGER_PORT_PLUS": "v",
}

names = {
    "EIGER": "Eiger",
    "EIGER_PORT": "Eiger-PORT",
    "EIGER_PORT_PLUS": "Eiger-PORT+",
}