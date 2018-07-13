# FIB-Sripting

The script, **img2stream.py**, converts the blue channel of an R,G,B image into a stream file for automating FIB milling procedures with the FEI Helios NanoLab 660 Dual Beam Scanning Electron Microscope and Focused Ion Beam. The python source is available within this master branch, and an executable is available upon request. Example image patterns and pattern-generation scripts are included in the Patterns subdirectory. Python dependencies are: os, numpy, argparse, and pillow.

**Application parameters are as follows:**
- *i*: path to image to be converted (required)
- *t*: type of stream file to create: s, s16, or c (optional with default value of s)
- *d*: boolean variable to specify the usage of minimum dwell time of 25 ns (optional with default value of True)
- *s*: size of image (optional, active only if -t is set to c, and set to have default value of 4096x4096 pixels)
- *p*: number of passes (optional with default value of 1)
- *f*: width of frame around input image (optional with default value of 48 pixels)
- *o*: output path to stream file (optional with default value of output.str)

## Usage
### Examples
If executed as a python script, typical usage is as follows. The following call converts the image, test_pattern_8x8.png in the Patterns\Images subdirectory, into a 4096x4096-sized stream file with 100 passes (-p 100) and dwell time increments of 25 ns, and saves the stream file as specfied by the -o parameter, (-o .\StreamFiles\test_pattern_8x8.str). 
`python img2stream.py -i .\Patterns\Images\test_pattern_8x8.png -p 100 -o .\StreamFiles\test_pattern_8x8.str`

The following call converts the image, staircase_128_steps.png in the Patterns\Images subdirectory, to a stream file with 10 passes (-p 10) and dwell time increments of 100 ns (-d False).
`python .\img2stream.py -i .\Patterns\Images\staircase_128_steps.png -p 10 -d False -o .\StreamFiles\staircase_128_steps.str`

The following call converts a small test image, small_test_pattern.png in the Patterns\Images subdirectory, to a custom, single pass stream file (-t c) with a base size of 7x7 pixels (-s 7) and a blanked frame 1 pixel wide (-f 1).
`python img2stream.py -i .\Patterns\Images\small_test_pattern.png -t c -s 7 -f 1 -o .\StreamFiles\small_test.str`

The following call converts a the NIST logo with a superimposed linear gradient, nist.jpg in the Patterns\Images subdirectory, into a stream file with 10 passes (-p 10)
`python img2stream.py -i .\Patterns\Images\nist.jpg -p 10 -o .\StreamFiles\nist.str`


When compiled into an executable, typical usage of the application is as follows:
`.\img2stream.exe -i .\Patterns\staircase.png -p 100 -o .\StreamFiles\staircase.str`


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
