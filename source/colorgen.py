import sys
import os

def convert_24_to_8(palette, rgb):
    """
    Samples a 24-bit RGB value to the closest color on the provided
    8-bit palette. It calculates the squared Euclidean distance in RGB space
    to find the best match.

    :param palette: The input 256-color palette (a list of 768 bytes).
    :param rgb: The 24-bit RGB color to convert (a list/tuple of 3 integers).
    :return: The 8-bit index of the best-matching color in the palette.
    """
    best_index = -1
    best_dist = float('inf')

    for i in range(256):
        dist = 0
        for j in range(3):
            d = abs(rgb[j] - palette[i * 3 + j])
            dist += d * d  # Squared distance

        if dist < best_dist:
            best_index = i
            best_dist = dist

    return best_index

def generate_colormap(palette):
    """
    Generates Quake's 64 levels of lighting for a given 256-color palette.
    The final 32 colors are treated as "fullbright" and are not affected
    by lighting.

    :param palette: The input 256-color palette (a list of 768 bytes).
    :return: The generated colormap (a list of 16384 bytes).
    """
    colormap = [0] * (64 * 256)
    num_fullbrights = 32

    # A 256x64 grid: 256 palette entries, 64 light levels
    for y in range(64):       # Light level
        for x in range(256):  # Palette index
            # Fullbright colors are not dimmed
            if x >= 256 - num_fullbrights:
                colormap[y * 256 + x] = x
                continue

            rgb = [0, 0, 0]
            for i in range(3):
                # Dim the original palette color based on the light level 'y'
                rgb[i] = (palette[x * 3 + i] * (63 - y) + 16) >> 5

                # Clamp to a valid 8-bit range
                if rgb[i] > 255:
                    rgb[i] = 255

            # Find the closest color in the original palette for the new dimmed color
            colormap[y * 256 + x] = convert_24_to_8(palette, rgb)

    return colormap

def main():
    """
    Main function to handle file I/O and colormap generation.
    """
    # --- Argument check ---
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_palette.lmp>", file=sys.stderr)
        print("       Generates 'colormap.lmp' in the current directory.", file=sys.stderr)
        sys.exit(1)

    palette_filename = sys.argv[1]
    colormap_filename = "colormap.lmp"

    # --- Read input palette file ---
    try:
        with open(palette_filename, 'rb') as f_in:
            palette = list(f_in.read())
    except FileNotFoundError:
        print(f"Error: The file '{palette_filename}' was not found.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error opening input palette file: {e}", file=sys.stderr)
        sys.exit(1)

    if len(palette) != 768:
        print(f"Error: Input palette file is not 768 bytes long. Read {len(palette)} bytes.", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Successfully read {palette_filename} ({len(palette)} bytes).")

    # --- Generate the colormap ---
    print("🎨 Generating colormap...")
    colormap = generate_colormap(palette)

    # --- Write output colormap file ---
    try:
        with open(colormap_filename, 'wb') as f_out:
            f_out.write(bytes(colormap))
    except IOError as e:
        print(f"Error opening output colormap file: {e}", file=sys.stderr)
        sys.exit(1)

    if len(colormap) != 16384:
        print(f"Error: Failed to write all 16384 bytes to {colormap_filename}. Wrote {len(colormap)} bytes.", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Successfully wrote {colormap_filename} ({len(colormap)} bytes).")
    print("✨ Done!")

if __name__ == "__main__":
    main()