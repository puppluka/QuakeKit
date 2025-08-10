# Python conversion of 'getpop.c' from LibreQuake source library

import os
import sys
import struct

# The data from the C program's `pop` array
pop = [
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,
    0x0000, 0x0000, 0x6600, 0x0000, 0x0000, 0x0000, 0x6600, 0x0000,
    0x0000, 0x0066, 0x0000, 0x0000, 0x0000, 0x0000, 0x0067, 0x0000,
    0x0000, 0x6665, 0x0000, 0x0000, 0x0000, 0x0000, 0x0065, 0x6600,
    0x0063, 0x6561, 0x0000, 0x0000, 0x0000, 0x0000, 0x0061, 0x6563,
    0x0064, 0x6561, 0x0000, 0x0000, 0x0000, 0x0000, 0x0061, 0x6564,
    0x0064, 0x6564, 0x0000, 0x6469, 0x6969, 0x6400, 0x0064, 0x6564,
    0x0063, 0x6568, 0x6200, 0x0064, 0x6864, 0x0000, 0x6268, 0x6563,
    0x0000, 0x6567, 0x6963, 0x0064, 0x6764, 0x0063, 0x6967, 0x6500,
    0x0000, 0x6266, 0x6769, 0x6a68, 0x6768, 0x6a69, 0x6766, 0x6200,
    0x0000, 0x0062, 0x6566, 0x6666, 0x6666, 0x6666, 0x6562, 0x0000,
    0x0000, 0x0000, 0x0062, 0x6364, 0x6664, 0x6362, 0x0000, 0x0000,
    0x0000, 0x0000, 0x0000, 0x0062, 0x0062, 0x0000, 0x0000, 0x0000,
    0x0000, 0x0000, 0x0000, 0x0061, 0x6661, 0x0000, 0x0000, 0x0000,
    0x0000, 0x0000, 0x0000, 0x0000, 0x6500, 0x0000, 0x0000, 0x0000,
    0x0000, 0x0000, 0x0000, 0x0000, 0x6400, 0x0000, 0x0000, 0x0000
]

def main():
    filename = "pop.lmp"
    
    # Handle the USE_STDOUT preprocessor directive
    if os.environ.get("USE_STDOUT") is not None:
        extract = sys.stdout.buffer
    else:
        try:
            extract = open(filename, "wb")
        except IOError:
            sys.stderr.write(f"{filename} could not be created.\n")
            return 1
    
    try:
        for v in pop:
            # The C code writes the high byte then the low byte.
            # This is equivalent to big-endian byte order.
            # `struct.pack` handles this efficiently. `>H` means big-endian unsigned short.
            # If the C code was `fputc(v, extract); fputc(v >> 8, extract);`, it would be little-endian (`<H`).
            # Based on the order in the C code, big-endian seems to be the intent.
            try:
                extract.write(struct.pack('>H', v))
            except IOError:
                sys.stderr.write(f"failed to complete {filename}.\n")
                if extract is not sys.stdout.buffer:
                    extract.close()
                    if os.environ.get("NO_UNLINK") is None:
                        os.remove(filename)
                return 1

        if extract is not sys.stdout.buffer:
            extract.close()
    
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred: {e}\n")
        if extract is not sys.stdout.buffer:
            extract.close()
            if os.environ.get("NO_UNLINK") is None:
                os.remove(filename)
        return 1

    sys.stderr.write(f"{filename} successfully created.\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())