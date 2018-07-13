import os
import argparse
import numpy as np
from PIL import Image


# Get input from command line
parser = argparse.ArgumentParser(description="Creates an NxN test pattern")
parser.add_argument("-n", "--num_steps", type=int, default=8, help="Number of steps")
args = parser.parse_args()


# Set parameters
n = args.num_steps
size = (4096, 4096)
v = 0
dv = 256/n**2


# Create base image and tile
img = Image.new("RGB", size)
tile_size = tuple(i/n for i in size)
tile = Image.new("RGB", tile_size)
for j in range(n):
    for i in range(n):
        arr = np.uint8(v*np.ones(tile_size))
        tile = Image.fromarray(np.dstack((arr, arr, arr)))
        img.paste(tile, (i*tile_size[1],j*tile_size[0]))
        v += dv


# Save image
img = Image.fromarray(np.uint8(img))
img_dir = "Images"
if not os.path.exists(img_dir): os.makedirs(img_dir)
fname = os.path.join(img_dir, "test_pattern_{}x{}.png".format(n,n))
img.save(fname)
print "Pattern saved as {}.".format(fname)
img.show()
