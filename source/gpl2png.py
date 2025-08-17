import sys
from PIL import Image

def parse_gpl_palette(gpl_file_path):
    """
    Parses a GIMP .gpl palette file and returns a list of RGB tuples.
    """
    colors = []
    with open(gpl_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('GIMP Palette') or line.startswith('Name:') or line.startswith('Columns:'):
                continue
            
            # Split the line by whitespace to get RGB values
            parts = line.split()
            if len(parts) >= 3:
                try:
                    r = int(parts[0])
                    g = int(parts[1])
                    b = int(parts[2])
                    colors.append((r, g, b))
                except (ValueError, IndexError):
                    # Skip lines that don't contain valid RGB values
                    continue
    return colors

def create_palette_image(colors, size=(16, 16)):
    """
    Creates a 16x16 PNG image with the given palette.
    """
    num_colors = len(colors)
    if num_colors > 256:
        print("Warning: Palette has more than 256 colors. PNG will only show the first 256.")
        colors = colors[:256]

    # Create a new indexed-color image
    img = Image.new('P', size)
    
    # Create the palette for the image
    palette = []
    for r, g, b in colors:
        palette.extend([r, g, b])
    
    # Pad the palette to 256 entries if necessary
    while len(palette) < 768:
        palette.append(0)
    
    img.putpalette(palette)
    
    # Fill the image with the palette colors
    pixel_data = list(range(num_colors))
    img.putdata(pixel_data)
    
    return img

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python palette_converter.py <path_to_gpl_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not input_file.lower().endswith('.gpl'):
        print("Error: The provided file must be a .gpl file.")
        sys.exit(1)

    try:
        colors = parse_gpl_palette(input_file)
        if not colors:
            print("Error: Could not read any colors from the file.")
            sys.exit(1)

        img = create_palette_image(colors)
        output_path = input_file.replace('.gpl', '_palette.png')
        img.save(output_path)
        print(f"Successfully converted {input_file} to {output_path}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)