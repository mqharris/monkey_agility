import pickle
from matplotlib import pyplot as plt
import numpy as np

file = open("mouse_path.obj", 'rb')
mouse_path = pickle.load(file)
file.close()


data = np.array(mouse_path)

x, y = data.T

x = list(x)
y = list(y)

x = x[:50] + x[200:]
y = y[:50] + y[200:]


plt.scatter(x, y)

ax = plt.gca()
ax.invert_yaxis()

plt.show()
