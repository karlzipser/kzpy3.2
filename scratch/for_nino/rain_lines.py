"""
Rain simulation

Simulates rain drops on a surface by animating the scale and opacity
of 50 scatter points.

Author: Nicolas P. Rougier
"""
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib.animation import FuncAnimation
from kzpy3.utils import *

def plot_axes(n=100):
    plt.plot([-n,n],[0,0],'k')
    plt.plot([0,0],[-n,n],'k')
    plt.xlim((-n,n))
    plt.ylim((-n,n))


def cool_nino_plot_1(m,b):
    cool_x_list=range(-1200,1200)
    cool_y_list=[]
    for x in cool_x_list:
        y = m * x + b
        cool_y_list.append(y)
    plt.plot(cool_x_list,cool_y_list,'o-')
    plot_axes(n=100)
    plt.plot(0,b,'r.')


# Create new Figure and an Axes which fills it. 
fig = plt.figure(figsize=(7,7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0,1), ax.set_xticks([])
ax.set_ylim(0,1), ax.set_yticks([])

# Create rain data
n_drops = 50
rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

# Initialize the raindrops in random positions and with
# random growth rates.
rain_drops['position'] = np.random.uniform(0, 1, (n_drops, 2))
rain_drops['growth'] = np.random.uniform(50, 200, n_drops)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(rain_drops['position'][:,0], rain_drops['position'][:,1],
                  s=rain_drops['size'], lw=0.5, edgecolors=rain_drops['color'],
                  facecolors='none')

m = -10
b = -20
def update(frame_number):
  global m
  global b
  # Get an index which we can use to re-spawn the oldest raindrop.
  current_index = frame_number % n_drops

  # Make all colors more transparent as time progresses.
  rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
  rain_drops['color'][:,3] = np.clip(rain_drops['color'][:,3], 0, 1)

  # Make all circles bigger.
  rain_drops['size'] += rain_drops['growth']

  # Pick a new position for oldest rain drop, resetting its size,
  # color and growth factor.
  rain_drops['position'][current_index] = np.random.uniform(0, 1, 2)
  rain_drops['size'][current_index] = 5
  rain_drops['color'][current_index] = (0, 0, 0, 1)
  rain_drops['growth'][current_index] = np.random.uniform(50, 200)

  # Update the scatter collection, with the new colors, sizes and positions.
  plt.clf()
  cool_nino_plot_1(m,b)
  plot_axes(n=20)
  if np.abs(m)<0.001:
    m = 0.0
  plt.title(d2s('m =',m,', b =',b))
  m = m + 0.1
  b = b + 0.1
  if m > 10:
    m = -10
  if b > 20:
    b = -20

# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()
