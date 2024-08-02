from rembg import remove
from PIL import Image

input_path = '/media/drakosfire/Shared/bandit.png'
output_path = '/media/drakosfire/Shared/bandit-white.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)