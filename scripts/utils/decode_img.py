from PIL import Image
from io import BytesIO
import re, time, base64

def save_b64_as_png(codec, image_path):
    base64_data = re.sub('^data:image/.+;base64,', '', codec)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img.save(image_path, "PNG")