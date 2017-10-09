import math
import numpy as np
import pandas as pd
import plotly.graph_objs as go


def one_exp(t, a, b):
    return a * np.exp(-b * t)


def multi_exp(t, parameters):
    total_value = 0
    exp = 1
    while exp <= len(parameters) / 2:
        a, b = parameters[exp * 2 - 2: exp * 2]
        total_value += one_exp(t, a, b)
        exp += 1
    total_value += parameters[-1]  # last element in params ie c term
    return total_value


def data_map(data, parameters):
    return [multi_exp(x, parameters) for x in data]


def interpolate_data(time_a, time_b, data_a, data_b):
    all_time = np.union1d(time_a, time_b)
    series_a = list(zip(time_a, data_a))
    series_b = list(zip(time_b, data_b))
    for t in all_time:
        if t in [x[1] for x in series_a]:
            series_b.append((t, np.nan))
        else:
            series_a.append((t, np.nan))
    new_a = pd.Series([x[1] for x in sorted(series_a)]).interpolate().tolist()
    new_b = pd.Series([x[1] for x in sorted(series_b)]).interpolate().tolist()
    truncate = [(x[0], x[1]) for x in zip(new_a, new_b) if not math.isnan(x[0]) and not math.isnan(x[1])]
    return [x[0] for x in truncate], [x[1] for x in truncate]


def get_value(row, index):
    try:
        return float(row[index])
    except:
        return np.NaN


def create_data_trace(f_data, f_time, f_index, f_col_num):
    color_num = 255/f_col_num * f_index
    new_plot = go.Scatter(
        x=f_time,
        y=f_data,
        mode='markers',
        marker=dict(
            size='10',
            color='rgb(0,' + str(color_num) + ',0)',
            showscale=False
        ),
        name=str(f_index) + ' Data'
    )
    return new_plot


def create_curve_trace(f_data, f_time, f_index):
    new_plot = go.Scatter(
        x=f_time,
        y=f_data,
        mode='lines',
        line=dict(
            color='rgb(255,0,0)',
        ),
        name=str(f_index) + ' Curve'
    )
    return new_plot

