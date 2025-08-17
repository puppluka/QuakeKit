#!/usr/bin/env python3

"""
PNG 2 PAL in Python

A Python script to convert 16x16, 24-bit (or 32-bit with alpha) PNG files
to Quake-format .lmp color palettes.

This script replaces the TGA parsing logic with PNG parsing using the Pillow
library, but produces the exact same .lmp output file.

IMPORTANT NOTE: PNG FILE _CANNOT_ BE INDEXED, MUST BE RGB/RGBA FORMAT!!!

"""

import sys
import os
import argparse

# A friendly check for the required Pillow library.
try:
    from PIL import Image
except ImportError:
    print(
        "Error: The 'Pillow' library is required to run this script.",
        file=sys.stderr
    )
    print("Please install it using: pip install Pillow", file=sys.stderr)
    sys.exit(1)

# Constant for the expected size of the final palette data.
QUAKE_PALETTE_SIZE = 768  # 16x16 pixels * 3 bytes/pixel = 768

def convert_png_to_pal(filename: str):
    """
    Reads a PNG file, validates it, and converts it to a .lmp palette file.

    Args:
        filename: The path to the input PNG file.
    """
    try:
        # Open the image file using Pillow
        img = Image.open(filename)
    except FileNotFoundError:
        print(f"Error: couldn't find {filename}", file=sys.stderr)
        return
    except Image.UnidentifiedImageError:
        print(f"Error: {filename} is not a valid or supported image file.", file=sys.stderr)
        return
    except Exception as e:
        print(f"An error occurred while opening {filename}: {e}", file=sys.stderr)
        return

    # Use a 'with' block to ensure the image resource is closed.
    with img:
        # --- Validation checks, adapted for PNG files ---
        # 1. Check for 16x16 image dimensions
        if img.width != 16 or img.height != 16:
            print(f"Error: {filename} is not a 16x16 image.", file=sys.stderr)
            return

        # 2. Check for a compatible color mode (RGB or RGBA)
        if img.mode not in ('RGB', 'RGBA'):
            print(f"Error: {filename} should be an RGB or RGBA image.", file=sys.stderr)
            return
            
        # If the image has an alpha channel (RGBA), convert it to RGB.
        # This effectively drops the alpha channel to get 24-bit color data.
        if img.mode == 'RGBA':
            rgb_img = img.convert('RGB')
        else:
            rgb_img = img

        # --- Pixel processing ---
        # Pillow provides the pixel data in a standard top-to-bottom, RGB byte order.
        # This simplifies the process immensely, as no vertical flipping or
        # BGR-to-RGB swapping is needed.
        pal_data = rgb_img.tobytes()
        
        # Final sanity check on the byte data size
        if len(pal_data) != QUAKE_PALETTE_SIZE:
            print(f"Error: Extracted pixel data from {filename} is not the correct size.", file=sys.stderr)
            return

    # --- File Output ---
    # Determine the output filename by replacing the extension with .lmp
    base_name, _ = os.path.splitext(filename)
    output_filename = base_name + ".lmp"

    print(f"writing {output_filename}")
    try:
        with open(output_filename, "wb") as f_lmp:
            f_lmp.write(pal_data)
    except IOError as e:
        print(f"Error writing to {output_filename}: {e}", file=sys.stderr)

def main():
    """
    Main function to parse command-line arguments and process files.
    """
    parser = argparse.ArgumentParser(
        description="Converts 16x16 24/32-bit PNG files to Quake-format .lmp palettes.",
        epilog="This version uses the Pillow library to handle PNG images."
    )
    parser.add_argument(
        'files',
        metavar='file.png',
        type=str,
        nargs='+',  # Accepts one or more file arguments
        help='One or more PNG files to convert.'
    )

    args = parser.parse_args()

    for file in args.files:
        convert_png_to_pal(file)

if __name__ == "__main__":
    main()