import os
import argparse
import numpy as np
from PIL import Image


# Get arguments from command line
parser = argparse.ArgumentParser(description="Creates a staircase pattern")
parser.add_argument("-n", "--num_steps", type=int, default=128, help="Number of steps")
args = parser.parse_args()


# Set parameters
n = args.num_steps
size = (4096, 4096)
w = size[0]/n
dv = 256/n
val = 0


# Create staircase image
img = np.zeros(size)
for i,row in enumerate(img):
    img[i, :] = val*np.ones(row.shape)
    if i%w == 0:
        val += dv

# Save image
img = np.dstack((img, img, img))
img = Image.fromarray(np.uint8(img))
img.save('staircase.png')
img.show()
