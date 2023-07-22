import cv2
from PIL import Image

def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Thresholding to convert to binary image
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    # Find contours to isolate individual letters
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return image, contours

def extract_and_save_letters(image, contours, output_directory):
    # Create output directory if it doesn't exist
    import os
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Crop and save each letter as a separate image
        letter_image = image[y:y + h, x:x + w]

        # Create a filename with the detected letter
        letter_filename = f"letter_{i}.png"

        letter_path = os.path.join(output_directory, letter_filename)
        cv2.imwrite(letter_path, letter_image)

if __name__ == "__main__":
    input_image_path = "letters.jpg"
    output_directory = "/tmp/letters/all/"

    # Preprocess the image
    image, contours = preprocess_image(input_image_path)

    # Perform OCR and save individual letters
    extract_and_save_letters(image, contours, output_directory)

