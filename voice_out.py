from kokoro_onnx import Kokoro
import sounddevice as sd
import soundfile as sf
import time

# Loading Kokoro into the model

kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
print("Output Model ready")

Output_File = "/tmp/alice_speech.wav"

def speak(text: str):

    # Voice guard if you don't speak anything

    if not text or text.strip() == "":
        print("Nothing to speak.")
        return
    
    try:

        # Generate speech and customising that speech

        samples, sample_rate = kokoro.create(
            text,
            voice = "af_heart",
            speed = 1.0,
            lang = "en-us"
        )

        # Helps in reading the soundfile

        sf.write(Output_File, samples, sample_rate)
        data, fs = sf.read(Output_File)
        sd.play(data, fs)
        sd.wait()

       # Herlpful in making the mic not picking alice own voice

        words = len(text.split())
        wait_time = max(2.0, words * 0.07)
        time.sleep(wait_time)

        time.sleep(0.5)

    except Exception as e:
        print(f"Error: {e}")

# this is simply a demo run only works when specifically this file will run

if __name__ == "__main__":
    speak("At your service sir. How can i help you")