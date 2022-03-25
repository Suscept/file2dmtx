from pylibdmtx.pylibdmtx import decode
from pylibdmtx.pylibdmtx import encode
from PIL import Image
import base64

#print(Image.open('Capture.PNG').getpixel([5,5]))
#print(decode(Image.open("IMG_1674.jpg")))

encde_File = open(r'C:\Users\garfi\Pictures\Code\Misc\DataMatrix\lowfrog.jpg', 'rb')
#encde_Data = base64.b64encode(encde_File.read())
encde_Data = encde_File.read()

encde_File.close()

print(encde_Data)

encoded = encode(encde_Data, 'base256', )
img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
img.save('dmtx.png')