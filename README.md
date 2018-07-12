The script, img2stream.py converts the blue channel of an R,G,B image into a stream files for automating FIB milling procedures with the FEI Helios NanoLab 660 Dual Beam Scanning Electron Microscope and Focused Ion Beam.

Python dependencies are: os, numpy, argparse, and pillow.

Application parameters are as follows:
-i: path to image to be converted (required)
-t: type of stream file to create: s, s16, or c (optional with default value of s)
-d: boolean variable to specify the usage of minimum dwell time of 25 ns (optional with default value of True)
-s: size of image (optional, active only if -t is set to c, and set to have default value of 4096x4096 pixels)
-p: number of passes (optional with default value of 1)
-f: width of frame around input image (optional with default value of 48 pixels)
-o: output path to stream file (optional with default value of output.str)

If executed as a python script, typical usage is:
python img2stream .\Patterns\staircase.png -p 100 -o .\StreamFiles\staircase.str

When compiled into an executable, typical usage of the application is as follows:
.\img2stream.exe -i .\Patterns\staircase.png -p 100 -o .\StreamFiles\staircase.str
.\img2stream.exe -i .\Patterns\nist.png -p 10 -o .\StreamFiles\nist.str
.\img2stream.exe -i .\Patterns\test.png -t c -s 7 -p 1 -o .\StreamFiles\test.str

For Help:
python img2stream.py -h
.\img2stream.exe -h

# FIB-Sripting
