#!/bin/bash
# --- Qonverter: Audio Conversion Script ---

# Set the file containing the list of audio files to convert.
# The file should be formatted as:
# input/path/file.wav=output/path/file.wav
DATAFILE="sounds.txt"

# Check if the data file exists before proceeding
if [ ! -f "$DATAFILE" ]; then
    echo "Error: Data file not found at '$DATAFILE'"
    exit 1
fi

# Read the data file line by line
# IFS='=' sets the delimiter to the equals sign.
# The '-r' option prevents backslash escapes from being interpreted.
while IFS='=' read -r input_file output_file; do
    # Skip empty or commented lines
    [[ -z "$input_file" || "$input_file" =~ ^# ]] && continue

    echo "Converting '$input_file' to '$output_file'..."

    # Extract the directory path from the output file path
    output_dir=$(dirname "$output_file")

    # Create the output directory if it doesn't already exist.
    # The '-p' option creates parent directories as needed.
    if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
    fi

    # Run the FFmpeg conversion command.
    # -i:       Specifies the input file.
    # -ar 11025: Sets the audio sample rate to 11025 Hz.
    # -ac 1:     Sets the audio channels to 1 (mono).
    # -acodec pcm_u8: Sets the codec to unsigned 8-bit PCM audio.
    # -y:       Overwrite output file if it exists.
    ffmpeg -i "$input_file" -ar 11025 -ac 1 -acodec pcm_u8 -y "$output_file"

done < "$DATAFILE"

echo "Conversion process finished."

exit 0