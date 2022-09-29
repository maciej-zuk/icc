import sys
from tags import Profile
from PIL import Image
import functools
import math

with open(sys.argv[1], "rb") as ifile:
    profile = Profile(ifile)
    print(profile)
    print(profile.header)
    print(profile.table)
    for tag in profile.table.tags:
        print(tag)

    clutTag = profile.table.getTag(b"A2B0")
    print(f"Clut has {clutTag.gridPoints} grid points")

    clImgDim = math.ceil(math.sqrt(functools.reduce(lambda a, b: a*b, clutTag.gridPoints, 1)))

    clutImgLo = Image.new(mode="RGB", size=(clImgDim*2, clImgDim))
    clutImgLoP = clutImgLo.load()

    for d1 in range(clutTag.gridPoints[0]):
        for d2 in range(clutTag.gridPoints[1]):
            for d3 in range(clutTag.gridPoints[2]):
                for d4 in range(clutTag.gridPoints[3]):
                    icolor = clutTag.grid[d1][d2][d3][d4]
                    w = d4 + d3*clutTag.gridPoints[3] + d2*(clutTag.gridPoints[2]*clutTag.gridPoints[3]) + d1 * \
                        (clutTag.gridPoints[1]*clutTag.gridPoints[2]*clutTag.gridPoints[3])
                    py = w // clImgDim
                    px = w % clImgDim
                    clutImgLoP[2*px, py] = tuple(x & 0xff for x in icolor)
                    clutImgLoP[2*px+1, py] = tuple((x>>8) & 0xff for x in icolor)

    clutImgLo.save('clut.png')
