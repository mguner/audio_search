import speech_recognition as  sr
import  os
from pydub import AudioSegment
from  pydub.silence  import  split_on_silence
from pydub.silence import detect_nonsilent


def silence_based_conversion(path="", min_silence_len=750,
                             silence_thresh=-40, pad=300, start = 27238, end=208329 ):

    """
    This function takes the path of an audio files and chops it into smaller chunks based on silences in the speech.
    Also finds the corresponding text in the chunks. Chunks are saved in a directory "audio_chunks" and the text is
    saved into a txt file, "recognized.txt"
    parameters:
    -----------------
    path: str, local path for the audio file to divide into the chunks

    min_silence_len: int, in miliseconds. The minimum amount of silence to cut the audio file

    silence_thresh: int, in dBFS (Full-Scale Decibels). The threshold for magnitude of the sound so that we count it
    as silence. Here by default anything lower than -40 dBFS will be counted as silence.

    pad: int, in miliseconds. After divide the audio file into the chunks we are adding silent pads for both side of
    the chunks so that the accuracy of the speech increases.

    start: int, in miliseconds. Instead of all the audio file we can start from an arbitrary location to chop the data.

    end: int, in miliseconds.

    returns:
    ---------------------
    text: List of tuples. e.g [(1, (start_of_chunk, end_of_chunk), 'text of the chunk')]
    """
    # open the audio file stored in
    # the local system as a wav file.
    if (start == '-') & (end == '-'):
        alice = AudioSegment.from_mp3(path)
    elif (start == '-') & (end != '-'):
        alice = AudioSegment.from_mp3(path)[:end]
    elif (start != '-') & (end == '-'):
        alice = AudioSegment.from_mp3(path)[start:]
    else:
        alice = AudioSegment.from_mp3(path)[start: end]

    # open a file where we will concatenate
    # and store the recognized text
    fh = open("recognized.txt", "w+")

    ## we will also keep text in a list
    ## we will use this list later on for keyword search
    text = []

    # split track where silence is 0.75 seconds
    # or more and get chunks
    chunks = split_on_silence(alice,
                              # must be silent for at least 0.75 seconds
                              # or 750 ms. adjust this value based on user
                              # requirement. if the speaker stays silent for
                              # longer, increase this value. else, decrease it.
                              min_silence_len=min_silence_len,

                              # consider it silent if quieter than -40 dBFS
                              # adjust this per requirement
                              silence_thresh=silence_thresh,

                              ## pad chunks so that there wouldn't be abrupt cut
                              keep_silence=pad
                              )

    # Detect timestamps that speech starts
    # Note that we used the same parameters with split_on_silence
    ranges = detect_nonsilent(alice, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # create a directory to store the audio chunks.
    try:
        os.mkdir('audio_chunks')
    except(FileExistsError):
        pass

    # move into the directory to
    # store the audio files.
    os.chdir('audio_chunks')

    i = 0
    # process each chunk
    for chunk, rng in zip(chunks, ranges):

        # export audio chunk and save it in
        # the current directory.
        print("saving chunk{0}.wav".format(i))
        # specify the bitrate to be 192 k
        chunk.export("./chunk{0}.wav".format(i), bitrate='192k', format="wav")

        # the name of the newly created chunk
        filename = 'chunk' + str(i) + '.wav'

        #         print("Processing chunk "+str(i))

        # get the name of the newly created chunk
        # in the AUDIO_FILE variable for later use.
        file = filename

        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(file) as source:
            # remove this if it is not working
            # correctly.
            # r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened)
            # write the output to the file.
            fh.write("Recognized Text From chunk_{}\n".format(i) + rec + ".\n")
            text.append((i, rng, rec))

        # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

        i += 1

    os.chdir('../')

    return text
