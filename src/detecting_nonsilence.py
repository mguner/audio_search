import os
import pickle
import speech_recognition as sr


def detecting_speech(chunk_folder_path='data/audio_chunks'):
    chapter_chunks = os.listdir(chunk_folder_path)
    chapter_chunks.sort()
    try:
        os.mkdir("data/texts")
    except FileExistsError:
        pass
    for folder in chapter_chunks:
        chapter_text = []
        try:
            folder_path = os.path.join(chunk_folder_path, folder)
            chunks_names = os.listdir(folder_path)
            chunks_names.sort()
            range_name = 'ranges.obj'
            chunks_names.remove(range_name)
            range_path = os.path.join(folder_path, range_name)
            with open(range_path, 'rb') as file:
                ranges_list = pickle.load(file)
            chunks_names.sort()

            for chunk, rng in zip(chunks_names, ranges_list):
                if 'wav' in chunk:
                    chunk_path = os.path.join(folder_path, chunk)
                    r = sr.Recognizer()
                    with sr.AudioFile(chunk_path) as source:
                        audio_listened = r.listen(source)
                    try:
                        print('recognizer listens the audio {}'.format(chunk))
                        rec = r.recognize_google(audio_listened)
                        chapter_text.append((rng, rec))
                        print("{} recorded".format(chunk_path))
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                    except sr.RequestError:
                        print("Could not request results. check your internet connection")
            text_path = os.path.join("data/texts", folder) + '.obj'
            print(text_path)

            pickle.dump(chapter_text, open(text_path, "wb"))

        except:
            print(folder)
            pass


if __name__ == '__main__':
    detecting_speech()
