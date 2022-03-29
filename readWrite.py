from math import ceil
from pylibdmtx.pylibdmtx import encode
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import base64
import ntpath

version = 1
maxPartitionSize = 1555

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# Possible better way than recursive checking
def partitionData(data: bytes, fileName: str):
    header = bytes('{0}!{1}!1!1!'.format(version, fileName), 'utf8') # Create a header assuming there will be only one partition
    dataLength = len(data) + len(header)
    partitions = 1

    # Get the amount of partitions needed to store the given data
    while (dataLength > maxPartitionSize * partitions):
        partitions = ceil(dataLength/maxPartitionSize)
        header = bytes('{0}!{1}!{2}!{2}!'.format(version, fileName, partitions), 'utf8')
        dataLength = len(data) + len(header) * partitions
    
    # Generate the partitions
    matrices = []
    dataSize = maxPartitionSize - len(header) # How many bytes will be left for data after the header
    for x in range(partitions):
        thisHeader = bytes('{0}!{1}!{2}!{3}!'.format(version, fileName, x, partitions - 1), 'utf8')
        thisData = data[dataSize * x:dataSize * (x + 1)] # Get the data to be stored in this partition
        matrix = thisHeader + bytes(thisData, 'utf8')
        matrices.append(matrix)

    return(matrices)



def f2dmtxEncode(path: str):
    # Read file
    fileToEncode = open(path, 'rb')
    rawData = fileToEncode.read()
    fileToEncode.close()

    # Encode raw bytes for dmtx encoding
    # Encoding raw bytes into dmtx fails for unknown reasons
    #encde_Data = base64.b64encode(encde_File) # Encode with base64
    encde_Data = base64.b85encode(rawData) # Encode with base85(Ascii85) probably the best encoding

    fileName = path_leaf(path)

    # Partition given data
    partitions = partitionData(encde_Data, fileName)

    # Create data matrix for each partition
    images = []
    for i in range(partitions.count):
        encoded = encode(partitions[i], 'base256', )
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        matrixImg = (fileName + '_' + i + partitions.count - 1, img)
        images.append(matrixImg)

    return images


def f2dmtxDecode(dmtxPath: str, writePath: str):
    matrix = decode(Image.open(dmtxPath))
    matrixRaw = matrix[0] # Get data on first found matrix

    matrixData = str(matrixRaw).split("'")[1] # Get only the data contained in the matrix
    matrixData = matrixData.split('!', 5)

    # Decode data using the method it was encoded with
    #decoded = base64.b64decode(matrixData)
    decoded = base64.b85decode(matrixData[6])

    decde_File = open(str(matrixData[1]), 'wb')
    decde_File.write(decoded)