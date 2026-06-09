import speech_recognition as sr
import time
from faster_whisper import WhisperModel

# Loading the voice model

whisper_model = WhisperModel("small", device = "cpu", compute_type = "int8")
print("Input Model ready")

# It directly loads into the system making it easier as we dont have to load into the systemall the time

recognise = sr.Recognizer()

# Making recognizer more sensitive — picks up softer speech better

recognise.energy_threshold = 250
recognise.dynamic_energy_threshold = True

def listen() -> str:

    time.sleep(0.5)

    # Making a microphone type of thing which will listen to whatever i will speak

    with sr.Microphone() as source:
        print("Listening......")

        # This is to reduce the ambient noise such as the fan noise etc.

        recognise.adjust_for_ambient_noise(source, duration = 2.5)

        # Now deciding how it took my its understood or what state my voice is at

        try:

            # Take my audio and waits for 5 seconds if there is something else to say 

            audio = recognise.listen(source, timeout = 60, phrase_time_limit = 20)

            # Now my recognised audio will be converted to text for further processing and this will be done using whisper

            print("Thinking.....")

            # SAving the audio to a temp file

            with open("/tmp/alice_input.wav", "wb") as fin:
                fin.write(audio.get_wav_data())

            segments, info = whisper_model.transcribe(
                "/tmp/alice_input.wav",
                language="en",
            )
 
            # Join all segments
            text = " ".join([seg.text for seg in segments]).strip()

            if text:
                print(f"Sir you said: {text}")
                return text
            else:
                return ""

        # My speech is active but i dont say anything for a long time then it will timeout mentioned above 5 seconds

        except sr.WaitTimeoutError:
            print("No speech detected sir.")
            return ""

        # Alice was unable to understand my voice so it will be an unknown value

        except sr.UnknownValueError:
            print("I didn't get it sir please repeat sir.")
            return ""

        # If there is any other kinda error

        except Exception as e:
            print(f"Error: {e}")
            return ""

# This is just a simple text block runs only when this particular file runs      

if __name__ == "__main__":
    print("sir....")
    result = listen()
    if result:
        print(f"Worked: {result}")
    else:
        print("try again")

