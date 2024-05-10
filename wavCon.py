from pydub import AudioSegment
import os


def convert_wav(wav_path, target_path, target_format="wav"):
    """
    Convert a WAV file to a specified format, ensuring it is compatible with speech recognition requirements:
    - Format: WAV
    - Channels: 1 (Mono)
    - Sample Width: 16 bit
    - Frame Rate: 16000 Hz
    """
    try:
        # Load the audio file
        audio = AudioSegment.from_wav(wav_path)

        # Convert to mono and 16000 Hz frame rate
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)

        # Export the converted file
        audio.export(target_path, format=target_format, bitrate="256k")
        print("Conversion successful. File saved to:", target_path)
    except Exception as e:
        print("An error occurred during conversion:", e)


# Example usage
source_wav_path = "2024-05-10_073744_000.wav"
target_wav_path = "2024-05-10_073744_000C.wav"
convert_wav(source_wav_path, target_wav_path)
