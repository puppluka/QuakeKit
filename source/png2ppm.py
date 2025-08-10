import sys
from PIL import Image

def convert_png_to_ppm(png_files):
    """
    Converts a list of PNG image files to the PPM format.

    Args:
        png_files (list): A list of paths to PNG image files.
    """
    if not png_files:
        print("Please provide at least one PNG file as an argument.")
        return

    for png_file in png_files:
        if not png_file.lower().endswith('.png'):
            print(f"Skipping '{png_file}'. It does not appear to be a PNG file.")
            continue

        try:
            with Image.open(png_file) as img:
                # Convert the image to RGB format, which is required for PPM
                rgb_img = img.convert('RGB')
                ppm_filename = f"{png_file[:-4]}.ppm"
                rgb_img.save(ppm_filename, "PPM")
                print(f"Successfully converted '{png_file}' to '{ppm_filename}'")
        except FileNotFoundError:
            print(f"Error: The file '{png_file}' was not found.")
        except Exception as e:
            print(f"An error occurred while processing '{png_file}': {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_images.py <image1.png> <image2.png> ...")
    else:
        # sys.argv[0] is the script name, so we slice from index 1
        png_files_to_convert = sys.argv[1:]
        convert_png_to_ppm(png_files_to_convert)