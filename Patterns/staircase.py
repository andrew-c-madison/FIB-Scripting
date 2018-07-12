import os
import argparse
import numpy as np
from PIL import Image


parser = argparse.ArgumentParser(description="Creates a staircase pattern")
parser.add_argument("-n", "--num_steps", type=int, default=128, help="Number of steps")
args = parser.parse_args()

n = args.num_steps
size = (4096, 4096)
w = size[0]/n
dv = 256/n

img = np.zeros(size)
val = 0
for i,row in enumerate(img):
    img[i, :] = val*np.ones(row.shape)
    if i%w == 0:
        val += dv


#
img = np.dstack((img, img, img))
img = Image.fromarray(np.uint8(img))
img.save('staircase.png')
img.show()
