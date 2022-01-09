import pickle
from matplotlib import pyplot as plt

file = open("recorded_clicks.obj", 'rb')
clicks = pickle.load(file)
file.close()

# invert y axis because the origin is in the top left, not bottom left
clicks = [[pt[0], 1080-pt[1]]
          for pt in clicks if pt[0] > 700]  # remove one obvious outlier

plt.hist2d([x[0] for x in clicks], [x[1] for x in clicks],
           bins=150,
           range=[[750, 1250], [0, 400]])

plt.savefig("heatmap.png")
