from pydub import AudioSegment
from pydub.playback import play


def play_wav(path, intervals):
    alice = AudioSegment.from_wav(path)
    start = intervals[0]
    stop = intervals[-1]
    play(alice[start: stop])


if __name__ == "__main__":
    play_wav()


