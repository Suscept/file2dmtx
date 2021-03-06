from math import ceil
from pylibdmtx.pylibdmtx import encode
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import base64

version = 1
maxPartitionSize = 1555

def partitionIndex(e):
    return e[2]

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
        matrix = thisHeader + thisData
        matrices.append(matrix)

    return(matrices)

def ParsePartition(partition):
    return tuple(bytes(partition, 'utf8').split(b'!', 4))

def mergePartitions(partitions):
    # Decode partitions into a list of tuples
    decodedPartitions = []
    for part in partitions:
        decodedPartitions.append(ParsePartition(part))

    # Verify all partitions are for the same file
    # by checking if all partitions have the same filename as the first given partition
    for part in decodedPartitions:
        if (part[1] != decodedPartitions[0][1]):
            raise ValueError('Mixed partitions! ' + str(part[1]))

    # Verify all partitions are present for the file
    if (len(decodedPartitions) <= int(decodedPartitions[0][3])):
        raise ValueError('Missing partition(s)! ' + decodedPartitions.count + '/'+ decodedPartitions[0][3])

    # Sort by index
    decodedPartitions.sort(key=partitionIndex)

    # Merge each partition's data
    fileData = bytes()
    for part in decodedPartitions:
        fileData += part[4]
    
    # Return file as a tuple with it's name and data
    filename = decodedPartitions[0][1].decode("utf-8")
    return (filename, fileData)

def f2dmtxEncode(data: bytes, filename: str):
    # Encode raw bytes for dmtx encoding
    # Encoding raw bytes into dmtx fails for unknown reasons
    #encde_Data = base64.b64encode(encde_File) # Encode with base64
    encde_Data = base64.b85encode(data) # Encode with base85(Ascii85) probably the best encoding

    # Partition given data
    partitions = partitionData(encde_Data, filename)

    # Create data matrix for each partition
    images = []
    for i, item in enumerate(partitions):
        encoded = encode(item, 'base256', )
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        matrixImg = (filename, img, i, len(partitions), len(item))
        images.append(matrixImg)

    return images

def GetBytesFromEncoded(partitions):
    matrixData = mergePartitions(partitions)

    # The data is encoded using ASCII85. More information in issue #3
    decoded = base64.b85decode(matrixData[1])

    return (matrixData[0], decoded)

def DecodeFromImage(image: Image):
    partitions = []
    for img in image:
        matrices = decode(img) # Get all matrices found in the image

        for matrix in matrices:
            # Parse only the data encoded in the matrix
            matrixRaw = matrix[0]

            partitions.append(matrixRaw)
    
    # Return filename, and the file's bytes
    return GetBytesFromEncoded(partitions=partitions)