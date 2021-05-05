import os
import pickle

from fuzzywuzzy import fuzz
from play import play_wav
from listen import recognize_speech_from_mic


def keyword_match(keyword):
    results = []
    chapter_texts = os.listdir("data/texts")
    chapter_texts.sort()
    flag = False
    for chapter_name in chapter_texts:
        pickle_path = os.path.join("data/texts", chapter_name)
        chapter = chapter_name.split('_')[1]
        with open(pickle_path, 'rb') as file:
            chapter_texts = pickle.load(file)
        for (interval, sentence) in chapter_texts:
            score = fuzz.token_set_ratio(keyword['transcription'], sentence)
            if score > 95:
                chapter_audio = chapter_name.split(".")[0]+".wav"
                audio_path = os.path.join("data/audio_file_wav", chapter_audio)
                results.append((audio_path, interval, sentence))
                # we need to change min code
                # this is wrong but it is ok right now
                min_start = round((interval[0]/1000)/60, 2)
                min_end = round((interval[1]/1000)/60, 2)
                print('Result is found in chapter {} between [{}, {}]'.format(chapter, min_start, min_end))
                print(""" 
                {}
                """.format(sentence))
                play_wav(audio_path, interval)
                print("""
                Say 'Next!' to find next match with {} in the text
                Say 'Stop!' to play the audio_book from current match
                """.format(keyword['transcription']))
                user = recognize_speech_from_mic()
                if user['transcription'] == 'next':
                    pass
                elif user['transcription'] == 'stop':
                    new_interval = (interval[0], interval[1] + 5000)
                    play_wav(audio_path, new_interval)
                    flag = True
                    break

                else:
                    print("Couldn't Understand the command")
                    break
        if flag:
            break
        print("No match has been found in chapter {}".format(chapter))

    print('We are done here!')
