from PIL import Image, ImageOps
import numpy as np
import cv2

def apply_transparency_to_white_areas(image_path):
    # Load the image in RGBA format to handle transparency
    image = Image.open(image_path).convert('RGBA')
    original = image.copy()  # Keep the original for final processing
    image.save('01_original.png')

    # Convert the image to a grayscale NumPy array
    gray_image = ImageOps.grayscale(image)
    gray_array = np.array(gray_image)

    # Normalize the background by setting near-white to white
    normalized_background = np.where(gray_array > 200, 255, gray_array)
    normalized_background_image = Image.fromarray(normalized_background.astype(np.uint8))
    normalized_background_image.save('02_normalized_background.png')

    # Edge detection to help locate an effective seed point for flood fill
    edges = cv2.Canny(normalized_background, 50, 150)
    edge_image = Image.fromarray(edges)
    edge_image.save('02a_edges.png')

    # Finding a seed point away from the edges by erosion
    kernel = np.ones((5, 5), np.uint8)
    eroded_edges = cv2.erode(edges, kernel, iterations=5)
    seed_point = np.unravel_index(np.argmin(eroded_edges), eroded_edges.shape)

    # Convert the normalized background image to a numpy array before thresholding
    normalized_background_array = np.array(normalized_background_image)

    # Flood fill from the dynamically found seed point
    mask = np.zeros((gray_array.shape[0] + 2, gray_array.shape[1] + 2), np.uint8)
    cv2.floodFill(normalized_background_array, mask, seed_point, 255, 0, 0, 8)

    # Create transparency mask
    transparency_mask = cv2.bitwise_not(mask[1:-1, 1:-1])
    transparency_image = Image.fromarray(transparency_mask)
    transparency_image.save('03_transparency_mask.png')

    # Combine RGB and modified Alpha into the final image
    alpha_channel = np.array(image)[:, :, 3]
    alpha_channel[transparency_mask == 0] = 0  # Apply transparency
    final_image = np.dstack((np.array(original.convert('RGB')), alpha_channel))
    final_image_with_original_colors = Image.fromarray(final_image)
    final_image_with_original_colors.save('04_final_image_with_original_colors.png')

# Uncomment to test
# apply_transparency_to_white_areas('path_to_your_image.png')

apply_transparency_to_white_areas('Bubbles the Floatgoat.webp')
