import os
import argparse
import numpy as np
from PIL import Image


# Get input from command line
parser = argparse.ArgumentParser(description="Creates a staircase pattern")
parser.add_argument("-n", "--num_steps", type=int, default=128, help="Number of steps")
args = parser.parse_args()


# Set parameters
n = args.num_steps
size = (4096, 4096)
w = size[0]/n
dv = 256/n


# Create image
img = np.zeros(size)
val = 0
for i,row in enumerate(img):
    img[i, :] = val*np.ones(row.shape)
    if i%w == 0:
        val += dv


# Save image
img = np.dstack((img, img, img))
img = Image.fromarray(np.uint8(img))
img_dir = "Images"
if not os.path.exists(img_dir): os.makedirs(img_dir)
fname = os.path.join(img_dir, "staircase_{}_steps.png".format(n))
img.save(fname)
print "Pattern saved as {}.".format(fname)
img.show()
