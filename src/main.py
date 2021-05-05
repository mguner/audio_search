import os

from fuzzy_match import keyword_match
from listen import recognize_speech_from_mic
from converting_mp3_to_wav import mp3_to_wav
from wav_to_chunks import wav_to_chunks
from detecting_nonsilence import detecting_speech

if __name__ == '__main__':
    first_prompt = input("\n "
                         " !! Make sure that you downloaded the audio folder into /data directory !!!\n "
                         " If this is your first time running this app press 1 \n "
                         " Note that depending on the size of the audio book set-up might take approximately 10 "
                         "minutes\n "
                         " If you already created the chunks and converted them to the text press 2\n ")
    if first_prompt == "1":
        path = os.getcwd()
        data_path = os.path.join(path, 'data')
        print(data_path)
        wav_folder_path = mp3_to_wav(data_path)
        print("mp3 converted to wav")
        wav_to_chunks(wav_folder_path)
        print('Chunks are created')
        print('detecting speech: This might take some time...')
        detecting_speech()

    limit = input(" \n"
                  "    Depending on the background noise"
                  "    sometimes microphone might not recognize the keyword you said. \n"
                  "    Enter the number of times you would like to give a shot in such cases.\n"
                  "    Enter number of attempts:\n"
                  "    ")
    PROMPT_LIMIT = int(limit)
    keyword = {
        "success": False,
        "error": None,
        "transcription": None
    }
    for j in range(PROMPT_LIMIT):
        print(f"\n"
              f"        *****Attempt_{j + 1}***\n"
              f"        Which keyword do you want to search? \n"
              f"        Speak after the command!\n"
              f"        ")
        # after the question wait a sec
        print("\n"
              "        Speak the word now!\n"
              "        ")
        keyword = recognize_speech_from_mic()
        if keyword["transcription"]:
            print("""
              You Said: {}
              """.format(keyword['transcription']))
            check = input("""
              If you want to give a new word: Press 1
              To continue: Press any key
              """)
            if check == '1':
                pass
            else:
                break
        # if API is not available
        if not keyword["success"]:
            break
        print("I didn't catch that. What did you say?\n")
    keyword_match(keyword)
