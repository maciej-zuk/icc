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

    clutImgLo = Image.new(mode="RGB", size=(clImgDim*2, clImgDim*2))
    clutImgLoP = clutImgLo.load()

    for d1 in range(clutTag.gridPoints[0]):
        for d2 in range(clutTag.gridPoints[1]):
            for d3 in range(clutTag.gridPoints[2]):
                icolor = clutTag.grid[d1][d2][d3]
                w = d3 + d2*clutTag.gridPoints[2] + d1 * clutTag.gridPoints[1]*clutTag.gridPoints[2]
                py = w // clImgDim
                px = w % clImgDim
                clutImgLoP[2*px, 2*py] = tuple([(icolor[0] >> 8) & 0xff, (icolor[1] >> 8) & 0xff, 255])
                clutImgLoP[2*px+1, 2*py] = tuple([(icolor[0] ) & 0xff, (icolor[1] ) & 0xff, 255])
                clutImgLoP[2*px, 2*py+1] = tuple([(icolor[2] >> 8) & 0xff, (icolor[3] >> 8) & 0xff, 255])
                clutImgLoP[2*px+1, 2*py+1] = tuple([(icolor[2] ) & 0xff, (icolor[3] ) & 0xff, 255])

    clutImgLo.save('clut.png')
