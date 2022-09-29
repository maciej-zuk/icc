import sys
from tags import Profile
import functools
import math

from PIL import Image
iim = Image.open('out.tif')
oim = Image.new(mode="RGB", size=iim.size)

pixels = iim.load()
pixels2 = oim.load()

with open(sys.argv[1], "rb") as ifile:
    profile = Profile(ifile)
    print(profile)
    print(profile.header)
    print(profile.table)
    for tag in profile.table.tags:
        print(tag)

    for i in range(iim.size[0]):
        print(i)
        for j in range(iim.size[1]):
            color = pixels[i, j]
            normalizedColor = [o/256.0 for o in color]
            normalizedOut = profile.table.getTag(b"A2B0").get(normalizedColor)
            out = tuple(int(255*o) for o in normalizedOut)
            pixels2[i, j] = out


oim.save('out.png')
