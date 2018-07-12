import os
import argparse
import numpy as np
from PIL import Image


# Function to convert pixel value to dwell time,
# Minimum increment is 25 ns, Max allowed value is 4096 (12-bit resolution)
def px2dwell(p, inc):
    return p*inc # maps to range [0 ns, 6375 ns]

# Generate beam position data
def img2pos(size):
    x_pos, y_pos = np.meshgrid(np.arange(size[0]), np.arange(size[1]))
    return x_pos, y_pos

# Rasterize beam path
def rasterize(p):
    return np.array([sublst if (i+1)%2 else sublst[::-1] for i,sublst in enumerate(p)])


# Read data from command line
parser = argparse.ArgumentParser(description="Converts an image into a stream file")
parser.add_argument("-i", "--image_path", type=str, required=True, default=None, help="Path to image")
parser.add_argument("-t", "--head", choices=["s","s16", "c"], default="s", help="Type of output pattern")
parser.add_argument("-d", "--min_dwell", type=bool, default=True, help="Flag for minimum dwell time, 25 ns")
parser.add_argument("-s", "--size", type=int, default=4096, help="Size of output pattern")
parser.add_argument("-p", "--passes", type=int, default=1, help="Number of passes")
parser.add_argument("-f", "--frame", type=int, default=48, help="Frame size")
parser.add_argument("-o", "--output", type=str, default="output.str", help="Outpu path for stream file")
args = parser.parse_args()


# Set parameters
image_path = args.image_path

if args.head == "s":
    header = "s" #s:(4096,4096); s16:(65536,65536); s16,25ns:(65536,65536) with 25 ns
    size = (4096, 4096)
elif args.head == "s16":
    header = "s16"
    size = (65536, 65536)
elif args.head == "c":
    header = "CUSTOM TEST"
    size = (args.size, args.size) # width, height
else:
    header = "s"
    size = (4096, 4096)

if args.min_dwell:
    header += ",25ns"

    
passes = args.passes
pad = args.frame
output_path = args.output


# Import 8-bit Image, scale to size, and convert to numpy array
print "Importing image"
img = Image.open(image_path).convert("RGB")
img = img.resize(size, Image.ANTIALIAS)
img_arr = np.asarray(img)


# Convert B channel to dwell time
# dwell = px2dwell(img_arr[:,:,2], 1.0)
dwell = img_arr[:, :, 2]


# Create position data, index is X[row][column]
print "Processing dwell time and beam position"
X, Y = img2pos(size)


# Rasterize dwell and position, then flatten data
dwell = rasterize(dwell)
X = rasterize(X)
Y = rasterize(Y)


# Flatten image into 1D array
D = dwell.flatten()
X = X.flatten()
Y = Y.flatten()


# Remove zeros, pad the image and remove the edges
idx_D = np.where(D>0)
idx_X = np.where((X>=pad) & (X<=size[1]-pad-1))
idx_Y = np.where((Y>=pad) & (Y<=size[0]-pad-1))
idx = np.intersect1d(idx_X, idx_Y)
idx = np.intersect1d(idx, idx_D)


# Structure data for writing to file
D = D[idx]
X = X[idx]
Y = Y[idx]
P = zip(D, X, Y)
mill_pts = np.count_nonzero(D)


# Write data to file
print "Writing stream file"
with open(output_path, 'w') as f:
    f.write(header)
    f.write("\n" + str(passes))
    f.write("\n" + str(mill_pts))
    for i,p in enumerate(P):
        f.write("\n{} {} {}".format(p[0], p[1], p[2]))

print "Stream file exported to {}".format(output_path)
