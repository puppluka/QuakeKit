#!/usr/bin/env python3

"""
TGA 2 PAL in Python

A Python script to convert 16x16, 24-bit uncompressed TGA files
to Quake-format .lmp color palettes.

This script is a functional equivalent of the C program provided.
"""

import sys
import os
import argparse
import struct

# Constants derived from the C code
TGA_HEADER_SIZE = 18
QUAKE_PALETTE_SIZE = 768  # 16x16 pixels * 3 bytes/pixel = 768

def convert_tga_to_pal(filename: str):
    """
    Reads a TGA file, validates it, and converts it to a .lmp palette file.

    Args:
        filename: The path to the input TGA file.
    """
    try:
        with open(filename, "rb") as f_tga:
            # Read and unpack the TGA header
            header = f_tga.read(TGA_HEADER_SIZE)
            if len(header) < TGA_HEADER_SIZE:
                print(f"Error: {filename} is not a valid TGA file.", file=sys.stderr)
                return

            # Unpack specific header fields for validation.
            # '<' specifies little-endian byte order.
            # 'B' is an unsigned char (1 byte), 'H' is an unsigned short (2 bytes).
            image_type = struct.unpack_from('<B', header, 2)[0]
            width = struct.unpack_from('<H', header, 12)[0]
            height = struct.unpack_from('<H', header, 14)[0]
            bpp = struct.unpack_from('<B', header, 16)[0]

            # --- Validation checks, mirroring the C code ---
            # 1. Check if the image is uncompressed, true-color RGB
            if image_type != 2:
                print(f"Error: {filename} should be an uncompressed, RGB image.", file=sys.stderr)
                return

            # 2. Check for 24-bit color depth
            if bpp != 24:
                print(f"Error: {filename} is not 24 bit in depth.", file=sys.stderr)
                return

            # 3. Check for 16x16 image dimensions
            if width != 16 or height != 16:
                print(f"Error: {filename} is not a 16x16 image.", file=sys.stderr)
                return

            # Read the pixel data (the palette itself)
            tga_data = f_tga.read(QUAKE_PALETTE_SIZE)
            if len(tga_data) != QUAKE_PALETTE_SIZE:
                print(f"Error: Could not read {QUAKE_PALETTE_SIZE} bytes of image data from {filename}.", file=sys.stderr)
                return

    except FileNotFoundError:
        print(f"Error: couldn't find {filename}", file=sys.stderr)
        return
    except Exception as e:
        print(f"An error occurred while reading {filename}: {e}", file=sys.stderr)
        return

    # Create a mutable byte array for the output palette
    pal_data = bytearray(QUAKE_PALETTE_SIZE)

    # --- Pixel processing, mirroring the C code logic ---
    # TGA files store pixels from bottom-to-top, and in BGR format.
    # We need to flip the image vertically and swap the Red and Blue channels.
    for tga_row in range(15, -1, -1):  # Iterate source rows from 15 down to 0
        for pal_col in range(16):      # Iterate source columns from 0 to 15
            # Calculate the index for the source pixel in the TGA data
            src_idx = (tga_row * 16 + pal_col) * 3

            # The destination row is flipped vertically
            dest_row = 15 - tga_row
            # Calculate the index for the destination pixel in the palette data
            dest_idx = (dest_row * 16 + pal_col) * 3

            # Swap BGR from TGA to RGB for the palette and assign
            pal_data[dest_idx + 0] = tga_data[src_idx + 2]  # Destination Red   = Source Blue
            pal_data[dest_idx + 1] = tga_data[src_idx + 1]  # Destination Green = Source Green
            pal_data[dest_idx + 2] = tga_data[src_idx + 0]  # Destination Blue  = Source Red

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
        description="Converts 16x16 24-bit TGA files to Quake-format .lmp palettes.",
        epilog="This is a Python port of Marco 'eukara' Hladik's tga2pal.c."
    )
    parser.add_argument(
        'files',
        metavar='file.tga',
        type=str,
        nargs='+',  # Accepts one or more file arguments
        help='One or more TGA files to convert.'
    )

    args = parser.parse_args()

    for file in args.files:
        convert_tga_to_pal(file)

if __name__ == "__main__":
    main()