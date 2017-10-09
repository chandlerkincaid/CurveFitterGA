#!/usr/bin/env python

import pandas as pd
import plotly
import plotly.graph_objs as go
import argparse

import functions as f
import geno

file_parser = argparse.ArgumentParser(description="Hello, this tool optimizes sum of exponentials "
                                                  "to fit a curve of plotted data.")
file_parser.add_argument("data", help="input for the program in csv format. First column must be time."
                                      "Remaining columns are data sets. Columns must be equal length. No Header.")
file_parser.add_argument("output_name", help="specify file output name, if no path is included the "
                                             "file will output where the script is located")
file_parser.add_argument("-a", "--arity", default=1, type=int, help="The number of exponential terms to fit. Default is one.")
file_parser.add_argument("-g", "--params", nargs=10, type=float, default=[-10, 10, 100, 1000, 100, 0.4, 0.3, 0.9, 0.3, 0.1],
                         help="optional parameter list for genetic algorithm:"
                              "min, max, pop, gen, mut_rate, stop_num, mut_rate, mut_amount, mut_decay, death_rate,"
                              "elitism"
                              "Defaults are: -10, 10, 100, 1000, 100, 0.4, 0.3, 0.9, 0.3, 0.1, False"
                              "See README for explanation")
file_parser.add_argument("-v", "--verbosity", default=False, action='store_true', help="Enabling verbosity will provide"
                                                                                 "more output during evolution")
args = file_parser.parse_args()

my_arity = args.arity * 2 + 1
geno_args = [my_arity, *args.params]

df = pd.read_csv(args.data, header=None)

time = list(df[0])
data = df.ix[:, 1:]
data_list = [list(data[col]) for col in data.columns]
col_num = len(data_list)
param_list = [geno.evolve(time, value, *geno_args, args.verbosity, index) for index, value in enumerate(data_list)]
y_preds = [f.data_map(time, x) for x in param_list]
[print(x) for x in param_list]
data_traces = [f.create_data_trace(value, time, index + 1, col_num) for index, value in enumerate(data_list)]
curve_traces = [f.create_curve_trace(value, time, index + 1) for index, value in enumerate(y_preds)]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
fig = go.Figure(data=data_traces + curve_traces, layout=layout)
plotly.offline.plot(fig, filename='curve_fitting.html')

