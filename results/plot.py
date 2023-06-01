import argparse
from os import listdir
import os
from sys import argv
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.ticker as ticker
from parameters import *

paths = {
    "num_clients" : "/home/luca/ETH/Thesis/EIGERPORT+/results/num_clients.csv",
    "num_servers" : "/home/luca/ETH/Thesis/EIGERPORT+/results/num_servers.csv",
    "zipf" : "/home/luca/ETH/Thesis/EIGERPORT+/results/zipf.csv",
}

labels = {
    "num_clients" : "Number of Clients",
    "num_servers" : "Number of Servers",
    "zipf" : "Zipf Parameter",
}

titles = {
    "num_clients" : " vs. Number of Client Threads",
    "num_servers" : " vs. Number of Servers",
    "zipf" : " vs. Zipf Parameter",
}

nums = ["(a)", "(d)", "(c)", "(b)", "(e)", "(f)", "(g)", "(h)", "(i)", "(j)", "(k)", "(l)", "(m)", "(n)", "(o)", "(p)", "(q)", "(r)", "(s)", "(t)", "(u)", "(v)", "(w)", "(x)", "(y)", "(z)"]
idx = 0

def plot(path, title):
    global idx
    num = nums[idx]
    idx+=1
    with open(path) as f:
        lines = f.readlines()
        x_label = labels[title]
        x_axis = []
        y_axises = { "throughput" : {}, "latency" : {} }
        for line in lines[1:]:
            line = line.strip().split(",")
            algorithm = line[0]
            if algorithm not in algorithms:
                continue
            if algorithm not in y_axises["throughput"]:
                y_axises["throughput"][algorithm] = []
            if algorithm not in y_axises["latency"]:
                y_axises["latency"][algorithm] = []
            if line[1] not in x_axis:
                x_axis.append(line[1])
            y_axises["throughput"][algorithm].append(line[2])
            y_axises["latency"][algorithm].append(line[3])
        bar = False
        throughput_label = "Tput (ops/s)"
        latency_label = "Latency (ms)"
        if title == "zipf":
            bar = True
            throughput_label = "Normalized TP"
            latency_label = "Normalized Latency"
        else:
            bar = allBar
        is_y_tp = True
        if title == "zipf":
            is_y_tp = False
        generate_plot(x_axis, y_axises["throughput"], "Throughput" + titles[title], x_label,throughput_label, path, bar, num, is_y_tp= is_y_tp)
        num = nums[idx]
        idx += 1
        is_lat = True
        if title == "zipf":
            is_lat = False
        generate_plot(x_axis, y_axises["latency"], "Latency" + titles[title], x_label,latency_label, path, bar, num, is_lat)
        
        if title == "num_clients":
            num = nums[idx]
            generate_plot(y_axises["throughput"],y_axises["latency"], "Latency vs. Throughput",throughput_label, latency_label, path, bar, num, is_x_tp=True)
            idx += 1
    return

def plot_all():
    for i, path in enumerate(paths):
        plot(paths[path], path)
    return

def convert_str_to_int(x_axis, y_axises, is_lat = False):
    # check if x_axis is a dict
    if isinstance(x_axis, dict):
        for algorithm in x_axis:
            x_axis[algorithm] = [float(x) for x in x_axis[algorithm]]
        if all(all(x.is_integer() for x in x_axis[algorithm]) for algorithm in x_axis):
            for algorithm in x_axis:
                x_axis[algorithm] = [int(x) for x in x_axis[algorithm]]
        for algorithm in y_axises:
            y_axises[algorithm] = [float(y) for y in y_axises[algorithm]]
        if all(all(y.is_integer() for y in y_axises[algorithm]) for algorithm in y_axises):
            for algorithm in y_axises:
                y_axises[algorithm] = [int(y) for y in y_axises[algorithm]]
        # convert latency from ms to s
        if is_lat:
            for algorithm in y_axises:
                y_axises[algorithm] = [y / 1000 for y in y_axises[algorithm]]
        return x_axis, y_axises
    
    x_axis = [float(x) for x in x_axis]
    for algorithm in y_axises:
        y_axises[algorithm] = [float(y) for y in y_axises[algorithm]]
    # if the floats have no decimals then convert them to int
    if all(x.is_integer() for x in x_axis):
        x_axis = [int(x) for x in x_axis]
    if all(all(y.is_integer() for y in y_axises[algorithm]) for algorithm in y_axises):
        for algorithm in y_axises:
            y_axises[algorithm] = [int(y) for y in y_axises[algorithm]]
    # convert latency from ms to s
    if is_lat:
        for algorithm in y_axises:
            y_axises[algorithm] = [y / 1000 for y in y_axises[algorithm]]
    return x_axis, y_axises

def format_label(value, is_tp):
    if is_tp:
        if value >= 1000000:
            return '{:.1f}M'.format(value / 1000000)
        elif value >= 1000:
            return '{:.1f}k'.format(value / 1000)
    return str(value)

def generate_plot(x_axis, y_axises, title, x_label, y_label, directory, barPlot = False, num = "", is_lat = False, is_x_tp = False, is_y_tp = False):
    if barPlot:
        _, y_axises = convert_str_to_int([], y_axises, is_lat)
        fig, ax = plt.subplots()
        new_y_axises = dict(y_axises)
        miny = 10000000
        maxy = 0
        if normalize and title != "Latency vs. Throughput":
            eiger_port = y_axises["EIGER_PORT"]
            for key in y_axises.keys():
                new_y_axises[key] = [round(y / eiger_port[i],2) if eiger_port[i] != 0 else y for i, y in enumerate(new_y_axises[key])]
                if key in algorithms:
                    miny = min(miny, min(new_y_axises[key]))
                    maxy = max(maxy, max(new_y_axises[key]))
            plt.ylim(miny-0.05, maxy+0.01)
        x_positions = np.arange(len(x_axis))  # create an array of x positions for each set of bars
        le = 0

        for i, algorithm in enumerate(y_axises):
            if(algorithm not in algorithms):
                continue
            
            offset = le * bar_width
            le += 1
            color = "white"
            if is_full[algorithm]:
                color = colors[algorithm]
            bar_style = {'hatch': bar_markers[algorithm], 'edgecolor': colors[algorithm], 'linewidth': bar_line_width}
            ax.bar(x=x_positions + offset, height=new_y_axises[algorithm], width = bar_width, label=names[algorithm], color=color, **bar_style)
        
        mid_pos = (le - 1) / 2.0

        # Set the tick position to the middle position of the middle bar
        ax.set_xticks(x_positions + (mid_pos * bar_width))

        #ax.set_title(num + " " + title, **title_info)
        ax.set_xlabel(x_label, fontsize=axis_font)
        ax.set_ylabel(y_label, fontsize=axis_font)
        ax.tick_params(axis='both', which='major', labelsize=tick_font)
        ax.set_xticklabels(x_axis, fontsize=tick_font)
        legend = ax.legend(bbox_to_anchor=(0.5, 1.17), loc='center', ncol = le,frameon = False ,prop = {"size" : 16}, fontsize = 12)
        #legend.get_frame().set_edgecolor('black')
        #legend.get_frame().set_linewidth(1.4)
        export_legend(legend, "zipf_legend.pdf")
        fig.subplots_adjust(top=0.8)
        # legend = ax.legend(bbox_to_anchor=(0.5, 1.8), loc='center', ncol = len(algorithms),frameon = False ,prop = {"size" : 16}, fontsize = 12)
        # legend.get_frame().set_edgecolor('black')
        # legend.get_frame().set_linewidth(1.4)
        # export_legend(legend)
        if haveGrid:
            ax.grid(haveGrid, color='gray', linestyle='--', linewidth=1, axis='y')
        
        if is_x_tp:
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_label(x, True)))
    
        # Format y-axis labels
        if is_y_tp:
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: format_label(y, True)))
    
        
        title_no_spaces = title.replace(" ", "_")
        filename = os.path.basename(directory)

        dir_name = filename.replace(".csv", "")

        new_dir_path = os.path.join(saveTo, dir_name)

        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
        
        dir_name += "/"
        plt.savefig(saveTo + dir_name + title_no_spaces + ".pdf",dpi=100)
        if showPlot:
            plt.show()
        return
    x_axis, y_axises = convert_str_to_int(x_axis, y_axises, is_lat)
    fig, ax = plt.subplots()

    plt.gcf().set_size_inches(15, 15)
    plt.subplots_adjust(top=0.905, bottom=0.16, left=0.155, right=0.975, hspace=0.2, wspace=0.2)
    for algorithm in y_axises:
        if(algorithm not in algorithms):
            continue
        # if x_axis is a dict
        if isinstance(x_axis, dict):
            ax.plot(x_axis[algorithm], y_axises[algorithm], label=names[algorithm], color=colors[algorithm], marker=markers[algorithm], linewidth=line_width,markersize=marker_size,markeredgewidth=2, markeredgecolor= colors[algorithm], markerfacecolor='None')
        else:
            ax.plot(x_axis, y_axises[algorithm], label=names[algorithm], color=colors[algorithm], marker=markers[algorithm],linewidth = line_width,markersize=marker_size,markeredgewidth=2, markeredgecolor= colors[algorithm], markerfacecolor='None')
    ax.set_title(num,**title_info)
    ax.set_xlabel(x_label, fontsize=axis_font)
    ax.set_ylabel(y_label, fontsize=axis_font)
    ax.tick_params(axis='both', which='major', labelsize=tick_font)
    #ax.legend()
    legend = ax.legend(bbox_to_anchor=(0.5, 1.8), loc='center', ncol = len(algorithms),frameon = False ,prop = {"size" : 16}, fontsize = 12)
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_linewidth(1.4)
    export_legend(legend, filename = "legend_scatter.pdf")
    if haveGrid:
        ax.grid(haveGrid, color='gray', linestyle='--', linewidth=1, axis='y')
    title_no_spaces = title.replace(" ","_")
    filename = os.path.basename(directory)
    
    if is_x_tp:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_label(x, True)))
    
    # Format y-axis labels
    if is_y_tp:
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: format_label(y, True)))
    
    
    dir_name = filename.replace(".csv", "")

    new_dir_path = os.path.join(saveTo, dir_name)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    
    dir_name += "/"
    plt.gcf().set_size_inches(15, 15)
    # top=0.885,
    # bottom=0.18,
    # left=0.195,
    # right=0.975,
    # hspace=0.2,
    # wspace=0.2
    plt.subplots_adjust(top=0.875, bottom=0.195, left=0.195, right=0.975, hspace=0.2, wspace=0.2)
    plt.savefig(saveTo+dir_name+title_no_spaces+".pdf",dpi=200)
    
    if showPlot:
        plt.show()
    return

def export_legend(legend, filename="legend.pdf"):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(saveTo + filename, dpi="figure", bbox_inches=bbox)

if __name__ == "__main__":
    plot_all()