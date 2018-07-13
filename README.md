# FIB-Sripting

The script, img2stream.py, converts the blue channel of an R,G,B image into a stream file for automating FIB milling procedures with the FEI Helios NanoLab 660 Dual Beam Scanning Electron Microscope and Focused Ion Beam. Python source available within master, executable available upon request. Example image patterns are included in the Patterns subdirectory.

Python dependencies are: os, numpy, argparse, and pillow.

Application parameters are as follows:
- i: path to image to be converted (required)
- t: type of stream file to create: s, s16, or c (optional with default value of s)
- d: boolean variable to specify the usage of minimum dwell time of 25 ns (optional with default value of True)
- s: size of image (optional, active only if -t is set to c, and set to have default value of 4096x4096 pixels)
- p: number of passes (optional with default value of 1)
- f: width of frame around input image (optional with default value of 48 pixels)
- o: output path to stream file (optional with default value of output.str)

## Usage
If executed as a python script, typical usage is:

`python img2stream.py -i .\Patterns\Images\test_pattern_8x8.png -p 100 -o .\StreamFiles\test_pattern_8x8.str`

`python .\img2stream.py -i .\Patterns\Images\staircase_128_steps.png -p 10 -d False -o .\StreamFiles\staircase_128_steps.str`

`python img2stream.py -i .\Patterns\Images\small_test_pattern.png -t c -s 7 -f 1 -o .\StreamFiles\small_test.str`

`python img2stream.py -i .\Patterns\Images\nist.jpg -p 10 -o .\StreamFiles\nist.str`



When compiled into an executable, typical usage of the application is as follows:
`.\img2stream.exe -i .\Patterns\staircase.png -p 100 -o .\StreamFiles\staircase.str`


For help with input parameters:
`python img2stream.py -h`
or
`.\img2stream.exe -h`


## Pattern Generation:
`python small_test_pattern.py`
`python test_pattern.py -n 8`
`python staircase.py -n 128`
