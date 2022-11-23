import os.path
from os.path import exists
import sys
import sounddevice as sd
import devices


class UserInput:
    device = 0
    name = ""
    song_ch = 0
    click_ch = 0


def check_default():
    if exists("default.ini"):
        return True
    return False


def read_default():
    print("Reading device config from file...", end="")

    device_list = []
    # Read config from file
    try:
        with open("default.ini", "r") as file:
            for line in file.read().splitlines():
                # Get all values for one device object
                device_name = line.split(";")[1]
                # Get device channels
                device_channels = line.split(";")[2]
                song_ch = []
                click_ch = []
                for channels in line.split(";")[3:4]:
                    for channel in channels.split(","):
                        if channel:
                            song_ch.append(int(channel))
                for channels in line.split(";")[4:5]:
                    for channel in channels.split(","):
                        if channel:
                            click_ch.append(int(channel))

                # Append a new object to device list
                device_list.append(devices.OutputDevice(device_name, device_channels, song_ch, click_ch))
        print("done!")
    except IndexError:
        print("Syntax error in file!")
        sys.exit(1)

    # Return array of device names
    return device_list


def read_playlist(entry_path, playlist_file):
    playlist = []
    # Read config from file
    try:
        with open(os.path.join(entry_path,playlist_file), "r") as file:
            for line in file.read().splitlines():
                # Get the track name
                playlist.append(line)
    except IndexError:
        print("Syntax error in file!")
        sys.exit(1)

    # Return array of device names
    return playlist


def write_default():
    input("Press enter to get a list of devices")
    counter = 0
    device_index = []

    # Create user input array
    user_input = []

    # List dirs for user
    for device in sd.query_devices():
        print(str(counter) + ")", device["name"])
        # Save dirs in array
        device_index.append(device["name"])
        counter += 1
    # Get the users input
    user_input_device = [int(x) for x in input("Choose your output devices: ").split(",")]

    user_inputs = []
    # Set channels for all devices
    for device in user_input_device:
        # Create user input object
        user_select = UserInput()
        # Save name to object
        user_select.name = sd.query_devices(device=device)["name"]

        print("\nChannel selection for Device: '" + str(device_index[device]) + "'")
        # Get the number of channels and safe it
        channel_range = sd.query_devices(device=device)["max_output_channels"]
        user_select.channels = channel_range	
        # Choose Track channels
        for ch in range(0, channel_range):
            print(str(ch) + ") channel " + str(ch))
        user_select.song_ch = input("Choose your main(song) channels: ").split(",")
        # Choose Click channels
        for ch in range(0, channel_range):
            print(str(ch) + ") channel " + str(ch))
        user_select.click_ch = input("Choose your click channels: ").split(",")

        # Save selected items in object
        user_inputs.append(user_select)

    print("Writing default config to file...", end="")
    counter = 1
    # Open ini file
    with open("default.ini", "w") as file:
        for device in user_inputs:
            # Extract the channels as strings
            song_channels = ",".join(str(x) for x in device.song_ch)
            click_channels = ",".join(str(x) for x in device.click_ch)
            # Get the number of channels
            channels = str(device.channels)
            # Write every object as a new line in file
            file.write(str(counter) + ";" + device.name + ";" + channels + ";" + song_channels + ";" + click_channels)
            # Insert a line break
            if counter + 1 <= len(user_inputs):
                file.write("\n")

            counter += 1

    print("done!")

