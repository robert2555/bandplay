import numpy as np
import os
import soundfile as sf

samplerate = 44100


def build_soundfiles(track_dir, device):
    # Create the track array with X channels (list of 2 lists consisting of x entries per list)
    track_array = np.empty((2, device.channels), dtype='float32')

    # load files into separate numpy arrays
    path = os.path.join(track_dir, "song.wav")
    if os.path.exists(path):
        with sf.SoundFile(path) as f:
            # Load track into numpy array
            song_array = f.read(dtype='float32')
            song_array_exists = True
    else:
        song_array_exists = False
    path = os.path.join(track_dir, "click.wav")
    if os.path.exists(path):
        with sf.SoundFile(path) as f:
            # Load track into numpy array
            click_array = f.read(dtype='float32')
            click_array_exists = True
    else:
        click_array_exists = False

    # Reshape track_array to length of the longest track (for mono or stereo WAVs)
    if not song_array_exists and click_array[0].size == 1:
        longest_track = click_array[:].size
    elif not song_array_exists and click_array[0].size == 2:
        longest_track = click_array[:,0].size
    elif not click_array_exists and song_array[0].size == 1:
        longest_track = song_array[:].size
    elif not click_array_exists and song_array[0].size == 2:
        longest_track = song_array[:,0].size
    elif song_array[0].size == 1 and click_array[0].size == 1:
        longest_track = max(song_array[:].size, click_array[:].size)
    elif song_array[0].size == 2 and click_array[0].size == 1:
        longest_track = max(song_array[:,0].size, click_array[:].size)
    elif song_array[0].size == 1 and click_array[0].size == 2:
        longest_track = max(song_array[:].size, click_array[:,0].size)
    elif song_array[0].size == 2 and click_array[0].size == 2:
        longest_track = max(song_array[:,0].size, click_array[:,0].size)

    track_array = np.empty((longest_track, device.channels), dtype='float32')

    # Write click to selected output channels
    if song_array_exists:
        # If song is a mono WAV
        if song_array[0].size < 2:
            for channel in device.song_ch:
                for index in range(song_array[:].size):
                    track_array[index][channel] = song_array[index]
        # If song is a stereo WAV
        else:
            # Merge Stereo to mono if only one channel selected
            if len(device.song_ch) == 1:
                for channel in device.song_ch:
                    for index in range(song_array[:, 0].size):
                        # Add both values together to get mono
                        track_array[index][device.song_ch] = song_array[index][0] + song_array[index][1]
            # Stereo processing
            else:
                for channel in device.song_ch:
                    for index in range(song_array[:, 0].size):
                        # Merge Stereo to mono
                        track_array[index][channel] = song_array[index][0] + song_array[index][1]

    # Write click to selected output channels
    if click_array_exists:
        # If click is a mono WAV
        if click_array[1].size < 2:
            for channel in device.click_ch:
                for index in range(click_array[:].size):
                    track_array[index][channel] = click_array[index]
        # if click a stereo wav
        else:
            for channel in device.click_ch:
                for index in range(click_array[:, 0].size):
                    # Merge Stereo to mono
                    track_array[index][channel] = click_array[index][0] + click_array[index][1]

    dir_prebuild = os.path.join(track_dir, "prebuild")
    if not os.path.exists(dir_prebuild):
        os.mkdir(dir_prebuild)
    # Write Soundfile as .wav
    sf.write(os.path.join(dir_prebuild, device.name + ".wav"), track_array, samplerate=samplerate)
