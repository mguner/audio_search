import speech_recognition as sr
from listen import recognize_speech_from_mic

PROMPT_LIMIT = 5


def listen_from_mic():
    for j in range(PROMPT_LIMIT):
        print("""
        *****Attempt_{}***
        Which keyword do you want to search? 
        Speak after the command!
        """.format(j))
        # after the question wait a sec
        print("""
        Speak the word now!
        """)
        keyword = recognize_speech_from_mic()
        if keyword["transcription"]:
            print("""
            You Said: {}
            """.format(keyword['transcription']))
            check = input("""
            If you want to give a new word: P
            ress 1
            To continue: Press any key
            """)
            if check == '1':
                pass
            else:
                break
        if not keyword["success"]:
            break
        print("I didn't catch that. What did you say?\n")
    return keyword

if __name__ == "__main__":
    listen_from_mic()

