import os
import numpy as np
from PIL import Image

img = np.random.randint(0,255, (7,7))
img[1:-1, 1:-1] = 0
pattern = np.arange(9).reshape(3,3) + 1
pattern = pattern*255.0/9.0
img[2:5, 2:5] = pattern

di = np.diag_indices(7)
img[di] = 0

img = np.dstack((img, img, img))
img = Image.fromarray(np.uint8(img))
img.save('test.png')
img.show()
