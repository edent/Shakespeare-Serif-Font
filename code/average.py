import os
import numpy as np
import math
from PIL import Image, ImageChops

def load_and_resize_images_from_directory(directory, target_size):
    image_files = [f for f in os.listdir(directory) if f.endswith(".png")]

    images = []
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        print("Reading " + image_path)
        image = Image.open(image_path).convert("L")  # Convert to grayscale

        # Create a new white background image
        new_size = (target_size[0], target_size[1])
        new_image = Image.new("L", new_size, color=255)  # White background
        
        old_width, old_height = image.size

        # Center the image
        x1 = int(math.floor((target_size[0] - old_width)  / 2))
        y1 = int(math.floor((target_size[1] - old_height) / 2))
        
        # Paste the image at the center
        new_image.paste(image, (x1, y1, x1 + old_width, y1 + old_height))
        
        # Make it larger to see if that improves the curve detection  
        new_image = new_image.resize( (600,600), Image.LANCZOS)
        images.append(new_image)

    return images

def calculate_average_image(images):
    # Convert the list of images to numpy arrays
    images_array = [np.array(img) for img in images]

    # Calculate the average image along the first axis
    average_image = np.mean(images_array, axis=0)

    return average_image

def convert_to_1bpp(average_image, threshold=120):
    # Convert the average image to 1bpp by setting a threshold value
    binary_image = np.where(average_image >= threshold, 255, 0).astype(np.uint8)

    return binary_image

def save_1bpp_image(binary_image, output_path):
    # Convert the numpy array to a binary image
    binary_image = Image.fromarray(binary_image, mode="L")
    
    # Crop the whitespace around the image
    binary_image = trim(binary_image)

    # Save the 1bpp monochrome image to the specified output path
    binary_image.save(output_path)
    
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


if __name__ == "__main__":
    #args = get_arguments()
    #letter = args['letter']
    letters = next(os.walk('../letters/raw/'))[1]

    for letter in letters:
        print("Averaging letter " + letter)
        input_directory   = "../letters/raw/" + letter + "/"
        if ( len(os.listdir(input_directory)) > 0 ):
            output_png_path = "../letters/average/" + letter + ".png"
            target_size = (200, 200)  # Set the desired target size for resizing
        
            # Load, resize, and add border to all images from the directory
            images = load_and_resize_images_from_directory(input_directory, target_size)

            # Calculate the average image
            average_image = calculate_average_image(images)

            # Convert the average image to 1bpp
            binary_image = convert_to_1bpp(average_image)
            
            # Save the 1bpp monochrome image
            save_1bpp_image(binary_image, output_png_path)

