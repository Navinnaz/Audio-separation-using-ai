import sounddevice as sd
import numpy as np
import soundfile as sf
from spleeter.separator import Separator
import tempfile
import os


def process_audio(indata, samplerate):
    try:
        if len(indata) == 0:
            print("No audio data received")
            return

        # Save the incoming audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            sf.write(temp_file.name, indata, samplerate)
            temp_file.close()

            # Print debug information
            print(f"Temporary file saved to: {temp_file.name}")

            # Process the temporary file with Spleeter
            separator.separate_to_file(temp_file.name, output_dir)

            # Read the separated audio files
            vocal_file = os.path.join(output_dir, os.path.basename(temp_file.name).replace('.wav', '/vocals.wav'))
            accompaniment_file = os.path.join(output_dir, os.path.basename(temp_file.name).replace('.wav', '/accompaniment.wav'))

            # Output paths for verification
            print(f"Vocals saved to: {vocal_file}")
            print(f"Accompaniment saved to: {accompaniment_file}")

            # Check if files were created and process target voice
            if os.path.exists(vocal_file):
                # Process or use the vocal file as needed
                print(f"Target voice file is available: {vocal_file}")
            else:
                print(f"Vocals file not found: {vocal_file}")

            # Clean up the temporary file
            os.remove(temp_file.name)
    except Exception as e:
        print(f"Error processing audio: {e}")

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    process_audio(indata, 48000)
 
if __name__ == '__main__':
    # Initialize Spleeter for 2 stems (vocals and accompaniment)
    separator = Separator('spleeter:2stems')

    # Directory to save output files
    output_dir = 'New_output'
    os.makedirs(output_dir, exist_ok=True)

    # Adjust buffer size
    buffer_size = 2048  # Change this value if needed

    # Start the real-time audio stream
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=48000, blocksize=buffer_size):
        print("Recording...")
        sd.sleep(20000)  # Record for 60 seconds (adjust as needed)
        print("Done recording")
