# Example usage:
# python img2stream.py -i .\Patterns\Images\nist_flat_black.png -a 0.19427 -ov 0.5 -l 20 -r 1024 -m 8192 -p 249 -pre 0 -o .\StreamFiles\


import os
import sys
import argparse
import numpy as np
from PIL import Image


# Define Functions
# Generate beam position data
def img2pos(size):
    x_pos, y_pos = np.meshgrid(np.arange(size[0]), np.arange(size[1]))
    return x_pos, y_pos

	
# Rasterize beam path
def rasterize(p):
    return np.array([sublst if (i+1)%2 else sublst[::-1] for i,sublst in enumerate(p)])

	
# Blank the beam between points that are not adjacent
def blank_beam(points):
	P0 = np.roll(points, -1, axis=0)
	P0[-1] = points[-1]
	px_d = np.sqrt((points[:,1]-P0[:,1])**2 + (points[:,2]-P0[:,2])**2)<=1
	P_blanked = np.vstack((points[:,0], points[:,1], points[:,2], px_d)).T
	return P_blanked

	
# Split file string into directories, basename, and extension
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts	
	
	
# Get input from command line
parser = argparse.ArgumentParser(description="Converts an image into a stream file")
parser.add_argument("-i", "--image_path", type=str, required=True, default=None, help="Path to image")
parser.add_argument("-t", "--head", choices=["S","S16"], default="s", help="Type of output pattern")
parser.add_argument("-d", "--min_dwell", action='store_true', help="Flag for minimum dwell time, 25 ns")
parser.add_argument("-a", "--pixel_size", type=float, default=0.150, help="Apparent beam diameter")
parser.add_argument("-ov", "--overlap", type=float, default=0.50, help="Amount to overlap the beams")
parser.add_argument("-l", "--feature_length", type=float, default=20.0, help="Size of feature in um.")
parser.add_argument("-r", "--resolution", type=int, default=1024, help="Patterning resolution")
parser.add_argument("-p", "--passes", type=int, default=1, help="Number of passes")
parser.add_argument("-f", "--frame", type=int, default=0, help="Frame size")
parser.add_argument("-b", "--blanking", action='store_true', help="Flag for blanking beam during patterning")
parser.add_argument("-m", "--max_dwell", type=int, default=4096, help="Maximum increment of dwell time")
parser.add_argument("-pre", "--prefix", type=int, default=0, help="Prefix for file output")
parser.add_argument("-o", "--output", type=str, default="output.str", help="Output directory for stream file")
args = parser.parse_args()


# Set parameters
image_path = args.image_path
header = args.head
passes = args.passes
pad = args.frame
input_parts = splitall(image_path)
basename = os.path.splitext(input_parts[-1])[0]
basename = "{:02d}_{:s}_a_{:f}_L_{:.0f}_R_{:d}_m_{:d}_p_{:d}.str".format(args.prefix, basename, args.pixel_size, args.feature_length, args.resolution, args.max_dwell, args.passes)
output_path = os.path.join(args.output, basename)
max_dwell = args.max_dwell
resolution_scale_factor = 4096/args.resolution
print("Resolution Scaling Factor: {}".format(resolution_scale_factor))


# Change to 25 ns increment, if prompted
if args.min_dwell:
    print("Setting min dwell increment: 25 ns")
    header += ",25ns"

	
# Compute image size based on pixel size and feature length
if args.overlap > 0.0:
	s = round(args.feature_length/(args.pixel_size*args.overlap))
else:
	s = round(args.feature_length/(args.pixel_size))
size = (s, s)


# Import 8-bit Image, scale to size, and convert to numpy array
print("Importing image")
img = Image.open(image_path).convert("RGB")
img = img.resize(size, Image.ANTIALIAS)
img_arr = np.asarray(img)


# Convert B channel to dwell time
dwell = img_arr[:, :, 2]


# Create position data, index is X[row][column]
print("Processing dwell time and beam position")
X, Y = img2pos(size)


# Rasterize dwell and position
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
D = D/np.max(D)*max_dwell # Scale dwell to max_dwell
D = D.astype(int)
X = X[idx]*resolution_scale_factor
Y = Y[idx]*resolution_scale_factor
P = np.vstack((D, X, Y)).T


# Append beam blanking parameter if prompted
if args.blanking:
    print("Using optional beam blanking")
    P = blank_beam(P)

	
# Count mill points and calculate patterning time
mill_pts = np.count_nonzero(D)
t = (np.sum(100*D*1e-9))*passes
mill_time = '{0:02.0f} min, {1:02.0f} s'.format(*divmod(t, 60))


# Write data to file
print("Writing stream file")
with open(output_path, 'w') as f:
    header += "\n{}\n{}".format(passes, mill_pts)
    np.savetxt(output_path, P, fmt="%d", delimiter="\t", header=header, comments="")


# Print output file path 	
print("Pattern size: {:d}x{:d} pixels".format(s, s))
print("Estimated patterning time: {}".format(mill_time))
print("Stream file exported to {}".format(output_path))
