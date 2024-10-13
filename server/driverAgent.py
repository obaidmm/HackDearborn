from uagents import Agent, Model
import os
import subprocess
from google.cloud import speech
import pyaudio
import wave

# Set Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/obaidmohiuddin/Downloads/just-terminus-438501-k7-6119e3603b7b.json"

# Define the Driver Agent
driver_agent = Agent(
    name="driver_agent",
    port=8001,
    seed="YOUR_COMMUNICATION_AGENT_SECRET_PHRASE",  # Replace with your unique secret phrase
    endpoint=["http://<127.0.0.1>:8001/submit"]  # Update <127.0.0.1> with the server IP if needed
)

class TranscriptionMessage(Model):
    transcription: str

communication_agent_address = "fetch1g88yj3wtmjlzyqlwrwx7nl7fxknuzu9cf9wgrj"  # Replace this with your actual communication agent address


def record_audio_wav(wav_path):
    # Parameters for recording
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    rate = 16000  # 16kHz sample rate

    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=sample_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    print("Recording started. Please speak now...")

    frames = []  # Initialize array to store frames

    # Record for 10 seconds
    for _ in range(0, int(rate / chunk * 10)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    
    print(f"Recording saved as {wav_path}")
    return True



async def send_transcription_message(address: str, transcription: str):
    print(f"Sending transcription to {address}: {transcription}")
    await driver_agent.send(address, TranscriptionMessage(transcription=transcription))



def convert_wav_to_m4a(wav_path, m4a_path):
    print(f"Converting '{wav_path}' to '{m4a_path}'...")
    try:
        subprocess.run(["ffmpeg", "-i", wav_path, m4a_path], check=True)
        print(f"Conversion finished. '{m4a_path}' created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error during conversion to .m4a:", e)
        return False

def convert_m4a_to_wav(m4a_path, wav_path):
    print(f"Converting '{m4a_path}' back to '{wav_path}' for transcription...")
    try:
        subprocess.run(["ffmpeg", "-i", m4a_path, "-ar", "16000", "-ac", "1", wav_path], check=True)
        print(f"Conversion finished. '{wav_path}' created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error during conversion to .wav:", e)
        return False

async def transcribe_audio(wav_path):
    # Check if the file exists
    if not os.path.exists(wav_path):
        print(f"Error: File '{wav_path}' does not exist. Ensure the conversion completed successfully.")
        return

    print(f"Audio file '{wav_path}' found. Proceeding with transcription.")
    speech_client = speech.SpeechClient()

    try:
        with open(wav_path, "rb") as audio_file:
            content = audio_file.read()

        # Configuration for WAV files with LINEAR16 encoding
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,  # Optional: Enable punctuation for better readability
        )

        # Transcribe the audio file
        response = speech_client.recognize(config=config, audio=audio)
        transcription = [result.alternatives[0].transcript for result in response.results]
        transcribed_text = " ".join(transcription)
        
        print("Transcription:", transcribed_text)
        
        # Send transcription to communication agent
        await send_transcription_message(communication_agent_address, transcribed_text)
        
    except Exception as e:
        print("Error during transcription:", e)

if __name__ == '__main__':
    # Define paths
    initial_wav_path = os.path.expanduser("~/Downloads/initial_recording.wav")
    m4a_path = os.path.expanduser("~/Downloads/converted_recording.m4a")
    final_wav_path = os.path.expanduser("~/Downloads/final_recording.wav")
    
    # Step 1: Record audio directly to .wav
    if record_audio_wav(initial_wav_path):
        # Step 2: Convert .wav to .m4a
        if convert_wav_to_m4a(initial_wav_path, m4a_path):
            # Step 3: Convert .m4a back to .wav for transcription
            if convert_m4a_to_wav(m4a_path, final_wav_path):
                # Step 4: Transcribe the .wav file
                import asyncio
                asyncio.run(transcribe_audio(final_wav_path))
                
                # Delete all audio files after transcription
                for file_path in [initial_wav_path, m4a_path, final_wav_path]:
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Could not delete file {file_path}: {e}")
