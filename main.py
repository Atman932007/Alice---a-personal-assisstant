from brain import ask_Alice, clear_memory
from voice_out import speak
from voice_in import listen
import time

# This displays the visual status on terminal like at what status Alice is currently at

def set_status(state: str):
    states = {
        "idle" : "Alice: Say Alice, wake up",
        "wake" : "Waking up.....",
        "listening" : "One second sir......",
        "thinking" : "Just a minute sir.....",
        "speaking" : "Speaking......",
        "type" : "type mode activates | type'voice mode to activate voice"
    }

    print(states.get(state, ""))

def main():
    # set_status("idle")
    # speak("Alice is at your service, sir.")

    # By default it starts at voice method and it waits for the wake up voice of mine

    mode = "voice"
    activated = False

    while True:

        # Type mode is selcted 

        if mode == "type":
            set_status("type")
            question = input("Me: ").strip()

            if not question:
                continue

            # Switching back to voice mode 

            if "voice mode" in question.lower():
                mode = "voice"
                activated = False
                speak("Switching baack to voice mode sir.")
                
                set_status("idle")
                continue

        # Voice mode is selected

        else:
            if not activated:
                set_status("idle")
                heard = listen()

                if not heard:
                    continue

                # Finally the voice is detected

                if "alice wake up" in heard.lower() or "alice" in heard.lower():
                    activated = True
                    set_status("wake")
                    speak("At your service sir.")
                    

                else:
                    continue 

            # Now making Alice listen for questions as it awake now

            set_status("listening")
            question = listen()

            if not question:
                speak("I didn't hear you sir.")
                
                set_status("idle")
                continue

            # Switching to type mode

            if "type mode" in question.lower():
                mode = "type"
                speak("Switching to type mode sir")
                
                continue

            # Alice sleeps after this

            if "alice sleep" in question.lower() or "alice, sleep" in question.lower() or "sleep" in question.lower():
                activated = False
                speak("Going to sleep sir. Say Alice Wake Up to wake me.")
                
                set_status("idle")
                continue            

        # It will make me exit Alice

        if "bye" in question.lower():
            print("Alice: Bye sir, Be the best.")
            speak("Bye sir, Be the best.")
            time.sleep(1.5)
            break
 
        # Forget it will clear ther meomry

        elif "forget" in question.lower():
            clear_memory()
            print("Alice: Lets start fresh sir.")
            speak("Lets start fresh sir.")
            
            set_status("idle")
 
        # Answer the question

        else:
            set_status("thinking")
            answer = ask_Alice(question)
            set_status("speaking")
            print(f"Alice: {answer}\n")
            speak(answer)
            

main()