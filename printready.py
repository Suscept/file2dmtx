from PIL import Image, ImageDraw, ImageFont

width = 750
height = 971

def MakePrintReady(image: Image, label1: str, label2: str):
    """
    Returns the provided data matrix labeled and sized for printing on A4 paper.

    `label1` goes on the top left

    `label2` goes on the top right
    """
    image = image.resize((width, width))

    im = Image.new('RGB', (width, height), 'white')
    im.paste(image, (0, height - width))

    d = ImageDraw.Draw(im)
    d.text((0, 0), label1, fill=('black'), font=ImageFont.truetype('arial', 24))
    d.text((width, 0), label2, fill=('black'), font=ImageFont.truetype('arial', 24), anchor="ra")

    return im