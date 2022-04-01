from readWrite import f2dmtxEncode
from PIL import Image

filePath = input('Enter path to file:\n')

outputPath = input('Enter output path. Leave blank to output to the same path as the input file.\n')

dmtxs = f2dmtxEncode(filePath)
for dmtx in dmtxs:
    dmtx[1].save(outputPath + "/" + dmtx[0] + '.png')
print('File saved as dmtx.png')