import base64
from pylibdmtx.pylibdmtx import decode
from PIL import Image

matrix = decode(Image.open(r'C:\Users\garfi\Pictures\Code\file2dmtx\dmtx.png'))
matrixRaw = matrix[0] # Get data on first found matrix

matrixData = str(matrixRaw).split("'")[1] # Get only the data contained in the matrix

# Decode data using the method it was encoded with
#decoded = base64.b64decode(matrixData)
decoded = base64.b85decode(matrixData)

print(decoded)

decde_File = open('decoded.png', 'wb')
decde_File.write(decoded)