import pdb
import pickle
import numpy as np
from matplotlib import pyplot as plt
import altair as alt
import altair_viewer
import pandas as pd

file = open("recorded_clicks.obj", 'rb')
clicks = pickle.load(file)
file.close()

# set edges
center = clicks[0]
left = clicks[1]
right = clicks[2]
bottom = clicks[3]
top = clicks[4]

length = abs(right[0] - left[0])
height = abs(top[1] - bottom[1])

# remove edge points from clicks
clicks = clicks[5:]

xs = [x[0] for x in clicks]
ys = [y[1] for y in clicks]

# set up data
raw_x_df = pd.DataFrame({"raw_x": [x for x in xs if x > 600]})
raw_y_df = pd.DataFrame({"raw_y": [x for x in ys if x > 700]})

delta_x = [((xs[i] - center[0])) for i in range(len(xs))]
delta_x = [x for x in delta_x if x < 100 and x > -100]
delta_x_df = pd.DataFrame({"delta_x": delta_x})

delta_y = [((ys[i] - center[1])) for i in range(len(ys))]
delta_y = [x for x in delta_y if x < 100 and x > -100]
delta_y_df = pd.DataFrame({"delta_y": delta_y})

x_std = np.std(delta_x)
sim_delta_x = np.random.normal(np.mean(delta_x), x_std, 100)
sim_delta_x_df = pd.DataFrame({"sim_delta_x": sim_delta_x})

y_std = np.std(delta_y)
sim_delta_y = np.random.normal(np.mean(delta_y), y_std, 100)
sim_delta_y_df = pd.DataFrame({"sim_delta_y": sim_delta_y})

# set up x charts
raw_x_chart = alt.Chart(raw_x_df).mark_bar().encode(
    alt.X("raw_x:Q", bin=True, scale=alt.Scale(domain=[950, 1000])),
    y="count()"
)
delta_x_chart = alt.Chart(delta_x_df).mark_bar().encode(
    alt.X("delta_x:Q", bin=True, scale=alt.Scale(domain=[-50, 50])),
    y="count()"
)
sim_delta_x_chart = alt.Chart(sim_delta_x_df).mark_bar().encode(
    alt.X("sim_delta_x:Q", bin=True, scale=alt.Scale(domain=[-50, 50])),
    y="count()"
)
x_charts = alt.vconcat(raw_x_chart, delta_x_chart, sim_delta_x_chart)

# set up y charts
raw_y_chart = alt.Chart(raw_y_df).mark_bar().encode(
    alt.X("raw_y:Q", bin=True, scale=alt.Scale(domain=[850, 940])),
    y="count()"
)
delta_y_chart = alt.Chart(delta_y_df).mark_bar().encode(
    alt.X("delta_y:Q", bin=True, scale=alt.Scale(domain=[-50, 50])),
    y="count()"
)
sim_delta_y_chart = alt.Chart(sim_delta_y_df).mark_bar().encode(
    alt.X("sim_delta_y:Q", bin=True, scale=alt.Scale(domain=[-50, 50])),
    y="count()"
)
y_charts = alt.vconcat(raw_y_chart, delta_y_chart, sim_delta_y_chart)

print("x mean: {}, x std: {}".format(np.mean(delta_x), x_std))
print("y mean: {}, y std: {}".format(np.mean(delta_y), y_std))

# display charts
altair_viewer.show(x_charts | y_charts)
