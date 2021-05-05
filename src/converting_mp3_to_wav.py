from pydub import AudioSegment
import os


def mp3_to_wav(data_path):
    in_data = os.listdir(data_path)
    for folder in in_data:
        folder_path = os.path.join(data_path, folder)
        wav_path = "data/audio_file" + '_wav'
        print('Folder Path is: ', folder_path)
        try:
            path_list = os.listdir(folder_path)
            try:
                os.mkdir(wav_path)
                print(wav_path)
            except FileExistsError:
                pass
            for mp3 in path_list:
                mp3_path = os.path.join(folder_path, mp3)
                target_path = os.path.join(wav_path, mp3.replace('.mp3', '.wav'))
                song = AudioSegment.from_mp3(mp3_path)
                song.export(target_path, format='wav')
        except NotADirectoryError:
            pass

    return wav_path


if __name__ == '__main__':
    mp3_to_wav('data')
