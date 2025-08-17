"""
    Turns 256 x 1 color palette pixel maps into 16x16 grid image.
"""

import sys
from PIL import Image

def process_and_resize_image(input_path, output_path):
    """
    Takes an input image, resizes it to a 16x16 grid, and saves it as a 256-pixel PNG.

    Args:
        input_path (str): The path to the input image file.
        output_path (str): The path to save the processed output image.
    """
    # Open the input image
    try:
        with Image.open(input_path) as img:
            # Get the size of the original image
            width, height = img.size

            # Create a new 16x16 image with a black background
            new_img = Image.new('RGB', (16, 16), (0, 0, 0))

            # Calculate the number of pixels to copy
            num_pixels_to_copy = min(width * height, 256)

            # Get the pixel data from the original image
            original_pixels = list(img.getdata())

            # Paste the original pixels into the new image
            new_img.putdata(original_pixels[:num_pixels_to_copy])

            # Save the new image as a PNG
            new_img.save(output_path, 'PNG')
            print(f"Image successfully processed and saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: The file at {input_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # sys.argv is a list containing the command-line arguments
    # sys.argv[0] is the script name itself
    # sys.argv[1] is the first argument (the file path)
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
        # You can customize the output file name here, for example by
        # adding a suffix or changing the extension.
        # This example simply hardcodes it for simplicity.
        output_file = 'palette.png'
        
        process_and_resize_image(input_file, output_file)
    else:
        print("Usage: Drag and drop an image file onto this script, or run it from the command line with a file path as an argument.")
        print("Example: python your_script_name.py gmpalette-raw.png")