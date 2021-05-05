import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
import pickle


def wav_to_chunks(wav_folder_path, min_silence_len=750, silence_thresh=-40, pad=300):
    wav_file_names = os.listdir(wav_folder_path)
    print('File to divide into chunks: {}'.format(wav_file_names))
    try:
        os.mkdir('data/audio_chunks')
        print("data/audio_chunks directory created")
    except FileExistsError:
        pass

    for wav_file_name in wav_file_names:
        chunk_file_name = wav_file_name.replace('.wav', '')
        chunk_files_path = os.path.join('data/audio_chunks', chunk_file_name)
        try:
            os.mkdir(chunk_files_path)
            print('Chunk directory {} created'.format(chunk_files_path))
        except FileExistsError:
            pass

        wav_file_path = os.path.join(wav_folder_path, wav_file_name)
        song = AudioSegment.from_wav(wav_file_path)
        print('Splitting the wav files from silence...')
        chunks = split_on_silence(song,
                                  # must be silent for at least 0.75 seconds
                                  # or 750 ms. adjust this value based on user
                                  # requirement. if the speaker stays silent for
                                  # longer, increase this value. else, decrease it.
                                  min_silence_len=min_silence_len,

                                  # consider it silent if quieter than -40 dBFS
                                  # adjust this per requirement
                                  silence_thresh=silence_thresh,

                                  # pad chunks so that there wouldn't be abrupt cut
                                  keep_silence=pad,
                                  seek_step=2
                                  )
        ranges = detect_nonsilent(song, min_silence_len=min_silence_len,
                                  silence_thresh=silence_thresh,
                                  seek_step=2)

        ranges_file_path = os.path.join(chunk_files_path, 'ranges.obj')
        pickle.dump(ranges, open(ranges_file_path, "wb"))
        i = 0
        for chunk in chunks:
            print("saving ../chunk{0}.wav".format(i))
            if i < 10:
                chunk_path = os.path.join(chunk_files_path, 'chunk0{}.wav'.format(i))
                chunk.export(chunk_path, bitrate='192k', format="wav")
                i += 1
            else:
                chunk_path = os.path.join(chunk_files_path, 'chunk{}.wav'.format(i))
                chunk.export(chunk_path, bitrate='192k', format="wav")
                i += 1
        print('****** File {} is done! *******'.format(wav_file_path))


if __name__ == '__main__':
    wav_to_chunks('/Users/mguner/Documents/personal/Experiments/audio_search/data/alices_adventures_64kb_wav')
