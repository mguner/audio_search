from load_audio_file import load_file, unzip_file
from converting_mp3_to_wav import *
from wav_to_chunks import wav_to_chunks
import os
if __name__ == '__main__':
	path = os.getcwd()
	data_path = os.path.join(path, 'data')
	print(data_path)
	print('Converting mp3 to wav format...')
	wav_folder_path = mp3_to_wav(data_path)
	print('mp3 --> wav conversion finished')
	print('Dividing the file into smaller chunks...')
	wav_to_chunks(wav_folder_path)
	print('Finished')