import base64
from pylibdmtx.pylibdmtx import decode
from PIL import Image

#decde_File = open('test.png', 'rb')
#decde_Data = decde_File.read()
#decde_File.close()

decde_File = decode(Image.open(r'C:\Users\garfi\Pictures\Code\Misc\DataMatrix/dmtx.png'), max_count=None)
decde_Data = decde_File[0]

decde_Data = str(decde_Data).split("'")
#decoded = base64.b64decode(decde_Data[1])
decoded = bytes(decde_Data[1])
print(decoded)

decde_File = open('decoded.png', 'wb')
decde_File.write(decoded)

#img = Image.frombytes('RGB', (decde_Data.width, decde_Data.height), decde_Data.pixels)
#img = Image.frombytes('RGB', (10, 10), decde_Data)
#img.save('dmtx_decoded.png')