import cv2
from PIL import Image
import numpy as np

def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite('image.png',image)
    # Erode the image vertically
    kernel = np.array([[0, 0, 0, 0, 0],
                       [0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 0]], dtype=np.uint8)

    erode = cv2.erode(image, kernel,iterations = 6)
    cv2.imwrite('erode.png',erode)

    # Thresholding to convert to binary image
    _, binary_image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('binary_image.png',binary_image)
    _, binary_erode = cv2.threshold(erode, 120, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('binary_erode.png',binary_erode)
    
    return image, binary_erode

def extract_and_save_letters(image, binary_image, output_directory):
    # Create output directory if it doesn't exist
    import os
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Find connected components (characters) in the binary image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image)

    for i in range(1, num_labels):  # Exclude background (index 0)
        x, y, w, h, area = stats[i]

        # Filter out noise (adjust these thresholds as needed)
        #if area < 50 or h > 1.5 * w:
        #    continue

        # Crop and save each character as a separate image
        # Add 1px padding to each side
        character_image = image[y-1:y + h+1, x-1:x + w+1]
        
        if ( character_image.any() ) :

            # Create a filename with the detected character
            character_filename = f"character_{i}.png"

            character_path = os.path.join(output_directory, character_filename)
            cv2.imwrite(character_path, character_image)

if __name__ == "__main__":
    input_image_path = "../samples/tempest-13.jpg"
    output_directory = "../letters/all/"

    # Preprocess the image
    image, binary_image = preprocess_image(input_image_path)

    # Perform OCR and save individual characters
    extract_and_save_letters(image, binary_image, output_directory)
