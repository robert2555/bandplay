import signal
import sys
import time
from os.path import exists

import keyboard
import sounddevice as sd
import soundfile as sf
import threading
import os
import getopt
import config
import prebuild
import numpy as np
from scipy.signal import resample


# Initial play states
class PlayState:
    running = False
    paused = False


def resample_files(entry_path):
    for (paths, dirs, files) in os.walk(entry_path, topdown=True):
        for file in files:
            if file.endswith(".wav"):
                sound_file = os.path.join(paths, file)
                resample_file = sound_file + ".resample"
                # Check samplerate
                sr = sf.SoundFile(sound_file).samplerate
                if sr != 44100:
                    print("Resample file: '" + sound_file + "' (samplerate=" + str(sr), end=") ", flush=True)
                    with sf.SoundFile(sound_file) as f:
                        track_array = f.read(dtype='float32')
                        secs = len(track_array) / f.samplerate
                        samples = int(secs * 44100) + 1
                        rwv = resample(track_array, samples)
                        # Write a new resampled file with 44100 Hz
                        sf.write(resample_file, rwv, format='WAV', samplerate=44100)
                    # Rename resampled file to original file
                    os.rename(resample_file, sound_file)
                    print("done!")


def get_path():
    # Get the passed args
    try:
        opts, args = getopt.getopt(sys.argv[1:3], "d:")
    except getopt.GetoptError:
        print("Usage: bandplay.py -d <path-to-config>")
        sys.exit(2)

    # Check if args are valid
    if not opts or opts[0][0] != "-d":
        print("Usage: bandplay.py -d <path-to-config>")
        sys.exit(2)

    track_dir = opts[0][1]

    # Check if the file exists
    if not exists(track_dir):
        print("Could not find dir: " + track_dir)
        sys.exit(2)

    # Return the config path
    return track_dir


def get_playlist_file():
    playlist_file = ""
    try:
        # Get the passed playlist
        opts, args = getopt.getopt(sys.argv[3:], "p:")

        playlist_file = opts[0][1]
    except:
        pass

    # Return the playlist
    return playlist_file


def choose_track_dir(path):
    counter = 0
    dir_index = []

    # List dirs for user
    for dirs in os.listdir(path):
        if os.path.isdir(path+dirs):
            print(str(counter + 1) + ")", dirs)
            # Save dirs in array
            dir_index.append(dirs)
            counter += 1

    # Get the users input
    try:
        user_input = int(input("Choose track dir: ")) - 1
    except ValueError:
        print("Didnt chose a track? Try again...")
        track_dir = choose_track_dir(path)
        return track_dir

    track_dir = os.path.join(path, dir_index[user_input])

    # check if tracks exist
    if not os.listdir(track_dir):
        print("No files in directory. Exiting.")
        sys.exit(1)

    # return the joined filepath
    return track_dir


def open_stream(device, track_dir):
    if device.song_ch and device.click_ch:
        print("Opened Stream on device: " + device.name + " (Multichannel)")
    else:
        print("Opened Stream on device: ", device.name)

    # Open and start the output stream on device channels
    output = sd.OutputStream(device=device.name, channels=device.channels)
    output.start()
    # Return stream object
    return output


def play_track(device, track_dir, state):
    # Set block size
    block_size = 2048
    # Create the track array with X channels
#    track_array = np.empty((2, device.channels), dtype='float32')
#
#    # Playback on MULTIPLE DEVICES (stereo)
#    # If device is for playing a Song
#    if not device.click_ch:
#        path = os.path.join(track_dir, "song.wav")
#        if os.path.exists(path):
#            with sf.SoundFile(path) as f:
#                # Load track into numpy array
#                track_array = f.read(dtype='float32')
#
#    # If device is for playing a Click
#    if not device.song_ch:
#        path = os.path.join(track_dir, "click.wav")
#        if os.path.exists(path):
#            with sf.SoundFile(path) as f:
#                # Load track into numpy array
#                track_array = f.read(dtype='float32')
#
#    # Playback on MULTI CHANNEL device
    device_track_path = os.path.join(track_dir, "prebuild", str(device.name + ".wav"))
#    # Check if there is a prebuild file
#    if os.path.exists(device_track_path):
#        print("Playing prebuild track...")
#        # Load prebuild device track
#        with sf.SoundFile(device_track_path) as f:
#            print("loadin track")
#            track_array = f.read(dtype='float32')
#
#    print("done")
#    # Get track- and block size
#    play_size = track_array[:, 0].size
#    block_count = play_size / block_size
#
#    start_block = 0
#    end_block = block_size
#
#
#    # Go through track in steps of <block_size>
#    for i in range(int(block_count)):
#        # Save the block of data in block var (block of 2048 lists of X channels)
#        block = track_array[start_block:end_block, :]
#
#        # Set the start/end of the next block
#        start_block += block_size
#        end_block += block_size

    for blocks in sf.blocks(device_track_path, blocksize=block_size,dtype='float32'):
        # Handle Resume/Play
        while state.paused:
            time.sleep(1)
        if state.running:
            # Write current block to output stream
            device.stream.write(blocks)
        if not state.running:
            break

    # Close Output Stream
    device.stream.close()

    state.running = False
    print("stream finished")


def play(track_dir, device_list):
    # Create a state object
    state = PlayState()

    threads = []
    for device in device_list:
        # Open device stream
        device.stream = open_stream(device, track_dir)
        # Open Thread for every device
        threads.append(threading.Thread(target=play_track, args=[device, track_dir, state]))

    try:
        print("Press Ctrl+C to stop")
        print("Starting...")
        # Start all threads
        for thread in threads:
            print("thread started")
            thread.start()

        # Set a running state
        state.running = True

        # Handle Play and Resume
        while thread_is_alive(threads):
            if keyboard.is_pressed("space") and state.paused:
                print("Resume")
                state.paused = False
                time.sleep(0.5)
            if keyboard.is_pressed("space"):
                print("Pause")
                state.paused = True
                time.sleep(0.5)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping...")
        state.running = False
        state.paused = False
        time.sleep(1)
        # Close Output Streams
        for device in device_list:
            device.stream.close()
        time.sleep(1)
        # Hard kill threads if still alive
        if thread_is_alive(threads):
            print("hard kill threads")
            os.kill(os.getpid(), signal.SIGINT)


def thread_is_alive(threads):
    # Check if any thread is still alive
    for thread in threads:
        if thread.is_alive():
            return True
    return False


def main():
    # Create a default device file
    if not config.check_default():
        print("No config file found")
        config.write_default()

    # Read device list from file
    device_list = config.read_default()

    # Get the entry path
    entry_path = get_path()
    # entry_path = r"C:\Users\rhe\Downloads\tracks"

    # Resample files (if necessary)
    resample_files(entry_path)

    # Write/Prebuild track arrays if MULTICHANNEL device
    for track in os.listdir(entry_path):
        path = os.path.join(entry_path, track)
        if os.path.isdir(path):
            for device in device_list:
                # if device is MULTICHANNEL and no prebuild exists
                if device.song_ch and device.click_ch:
                    if not os.path.exists(os.path.join(path, "prebuild", str(device.name + ".wav"))):
                        print("Pre-build files for track '" + track + "' and device '" + device.name + "'...", end="")
                        prebuild.build_soundfiles(path, device)
                        print("done!")

    # Check for given Playlist
    if get_playlist_file():
        # Read playlist file
        playlist = config.read_playlist(entry_path, get_playlist_file())
        # Go through every track in playlist
        for track in playlist:
            input("Press ENTER to play next track")
            print("playing: " + track)
            track_dir = os.path.join(entry_path, track)
            play(track_dir, device_list)
    else:
        try:
            while True:
                print("Press CTRL+C to exit program")
                # Let user choose a track dir
                track_dir = choose_track_dir(entry_path)
                # Play choosen track
                play(track_dir, device_list)
        except KeyboardInterrupt:
            print("")
            return


if __name__ == "__main__":
    main()
