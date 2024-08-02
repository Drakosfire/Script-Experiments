from pygltflib import GLTF2
from pygltflib.utils import ImageFormat

filename = "E:/Downloads/rainbow_chicken_model.glb"
gltf = GLTF2().load(filename)
# print(gltf)
gltf.images[0].name = "output_texture.png"  # Set the desired output filename
gltf.convert_images(ImageFormat.FILE)  # Convert images to separate files
gltf.images[0].uri # will now be cube.png and the texture image will be saved in cube.png
