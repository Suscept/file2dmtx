from readWrite import f2dmtxEncode
from PIL import Image

filePath = input('Enter path to file:\n')

outputPath = input('Enter output path. Leave blank to output to the same path as the input file.\n')

f2dmtxEncode(filePath).save('dmtx.png')
print('File saved as dmtx.png')