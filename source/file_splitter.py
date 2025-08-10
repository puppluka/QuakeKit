import os
import sys

def split_ascii_file(input_filepath):
    output_filename = None
    output_file_handle = None
    
    try:
        with open(input_filepath, 'r') as infile:
            for line in infile:
                if line.startswith('/*') and not line.startswith('*/'):
                    # [cite_start]Found an opening comment marker, extract filename [cite: 4]
                    if output_file_handle:
                        # Close the previous file if it was open
                        output_file_handle.close()
                    output_filename = line[2:].strip() # Remove '/*' and strip whitespace
                    output_file_handle = open(output_filename, 'w')
                elif line.startswith('*/'):
                    # Found a closing comment marker
                    if output_file_handle:
                        output_file_handle.close()
                        output_file_handle = None
                        output_filename = None
                else:
                    # [cite_start]Write lines to the current output file if one is open [cite: 5, 6]
                    if output_file_handle:
                        output_file_handle.write(line)

    except FileNotFoundError:
        print(f"Error: Input file '{input_filepath}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the last file is closed if the program exits
        if output_file_handle:
            output_file_handle.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: filesplitter <path_to_ascii_file>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    split_ascii_file(input_file_path)
    print(f"Processing complete. Files extracted from '{input_file_path}'.")