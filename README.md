


Usage:


.\img2stream.exe -i .\Patterns\test.png -t c -s 7 -p 1 -o .\StreamFiles\test.str

.\img2stream.exe -i .\Patterns\nist.png -p 10 -o .\StreamFiles\nist.str

.\img2stream.exe -i .\Patterns\staircase.png -p 100 -o .\StreamFiles\stai
rcase.str


Help:
.\img2stream.exe -h

usage: img2stream.exe [-h] -i IMAGE_PATH [-t {s,s16,c}] [-d MIN_DWELL]
                      [-s SIZE] [-p PASSES] [-f FRAME] [-o OUTPUT]

Converts an image into a stream file

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE_PATH, --image_path IMAGE_PATH
                        Path to image
  -t {s,s16,c}, --head {s,s16,c}
                        Type of output pattern
  -d MIN_DWELL, --min_dwell MIN_DWELL
                        Flag for minimum dwell time, 25 ns
  -s SIZE, --size SIZE  Size of output pattern
  -p PASSES, --passes PASSES
                        Number of passes
  -f FRAME, --frame FRAME
                        Frame size
  -o OUTPUT, --output OUTPUT
                        Output path for stream file
# FIB-Sripting
