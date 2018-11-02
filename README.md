# FIB-Sripting

The script, **img2stream.py**, converts the blue channel of an R,G,B image into a stream file for automating FIB milling procedures with the FEI Helios NanoLab 660 Dual Beam Scanning Electron Microscope and Focused Ion Beam. The python source is available within this master branch, and an executable is available upon request. Example image patterns and pattern-generation scripts are included in the Patterns subdirectory. Python dependencies are: os, numpy, argparse, and pillow.

**Application parameters are as follows:**
- *i*: path to image to be converted (required)
- *t*: type of stream file to create: s, s16, or c (optional with default value of s)
- *d*: boolean variable to specify the usage of minimum dwell time of 25 ns (optional with default value of True)
- *a*: pixel size in units of µm, which is assumed to be equivalent to the apparent ion beam diameter
- *ov*: overlap between dwell locations, (default value of 50%)
- *l*: size of the feature in units of µm
- *r*: Patterning resolution (default of 1024, 4096 is assumed to be the highest patterning resolution) 
- *p*: number of passes (optional with default value of 1)
- *f*: width of frame to blank around input image (optional with default value of 0 pixels)
- *b*: boolean variable to specify whether to blank the beam between non-adjacent dwell locations
- *m*: maximum dwell time in units of 100 ns (0.1 µs)
- *pre*: Numerical prefix to append to the beginning of the output file name 
- *o*: output path to stream file (optional with default value of output.str)

## Usage
### Examples
If executed as a python script, typical usage is as follows. The following call converts the image, test_pattern_8x8.png in the Patterns\Images subdirectory, into a stream file:
`python img2stream.py -i .\Patterns\Images\test_pattern_8x8.png -a 0.190 -ov 0.5 -l 20 -r 1024 -m 8192 -p 249 -pre 0 -o .\StreamFiles\`

### Help
For help with input parameters:
`python img2stream.py -h`
or
`.\img2stream.exe -h`


## Pattern Generation
Several scripts are included in the Patterns subdirectory for algorithmically generating patterns. 
- `python small_test_pattern.py` generates a small pattern for examining .str output.
- `python test_pattern.py -n 8` generates a 4096x4096 pixel patterned with an 8x8 array of graded tiles.
- `python staircase.py -n 128` generates a linear gradient, or staircase, with 128 steps.
