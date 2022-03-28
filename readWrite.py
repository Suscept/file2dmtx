from pylibdmtx.pylibdmtx import encode
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import base64
import ntpath

def f2dmtxEncode(path: str) -> Image:
    #fileToEncode = open(r'C:\Users\garfi\Pictures\Code\file2dmtx\lowfrog.jpg', 'rb')
    fileToEncode = open(path, 'rb')

    rawData = fileToEncode.read()

    fileToEncode.close()

    # Encode raw bytes for dmtx encoding
    # Encoding raw bytes into dmtx fails for unknown reasons
    #encde_Data = base64.b64encode(encde_File) # Encode with base64
    encde_Data = base64.b85encode(rawData) # Encode with base85(Ascii85) probably the best encoding
    if (len(encde_Data) > 1500):
        raise ValueError('File larger than 1.5kb! Support for larger files coming soon.')
    print(encde_Data)

    encoded = encode(encde_Data, 'base256', )
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    return img
    #img.save('dmtx.png')

def f2dmtxDecode(dmtxPath: str, writePath: str):
    #matrix = decode(Image.open(r'C:\Users\garfi\Pictures\Code\file2dmtx\dmtx.png'))
    matrix = decode(Image.open(dmtxPath))
    matrixRaw = matrix[0] # Get data on first found matrix

    matrixData = str(matrixRaw).split("'")[1] # Get only the data contained in the matrix

    # Decode data using the method it was encoded with
    #decoded = base64.b64decode(matrixData)
    decoded = base64.b85decode(matrixData)

    print(decoded)

    decde_File = open('decoded.png', 'wb')
    decde_File.write(decoded)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)