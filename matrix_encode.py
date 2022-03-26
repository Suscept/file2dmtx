from pylibdmtx.pylibdmtx import decode
from pylibdmtx.pylibdmtx import encode
from PIL import Image
import base64

#print(Image.open('Capture.PNG').getpixel([5,5]))
#print(decode(Image.open("IMG_1674.jpg")))

fileToEncode = open(r'C:\Users\garfi\Pictures\Code\file2dmtx\lowfrog.jpg', 'rb')

rawData = fileToEncode.read()

fileToEncode.close()

# Encode raw bytes for dmtx encoding
# Encoding raw bytes into dmtx fails for unknown reasons
#encde_Data = base64.b64encode(encde_File) # Encode with base64
encde_Data = base64.b85encode(rawData) # Encode with base85(Ascii85) probably the best encoding


print(encde_Data)

encoded = encode(encde_Data, 'base256', )
img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
img.save('dmtx.png')