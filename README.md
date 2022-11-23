# Bandplay
You need a Click/Track Player for your band, but dont have the money for expensive gear? Your Windows Laptop is crashing if your playing a live show? Or maybe you just want an open source solution to play your clicks and tracks in your rehearsal room. 

Just grab a Linux/Windows device with multiple outputs, insert your tracks and start the program. 
If your device dont have more than one Audio Port, the cheapest solution could be to use the standard AUX Port as Output 1 and a "USB to AUX" Device as Output 2. 

## Usage
Determine the selection of tracks (in track dir) yourself
```
python3 bandplay.py -d tracks
```
Play a list of tracks from a playlist
```
python3 bandplay.py -d tracks -p playlist
```

## Prepare your tracks
The program reads from 2 files
1. Click track -> "click.wav"
2. Backing track -> "song.wav"

Location of your Clicktrack:   
- bandplay/tracks/yourSong/click.wav  

Location of your Backingtrack:   
- bandplay/tracks/yourSong/song.wav

## Config (first start)
You will get asked for which outputs you want to use, at the first start of the program. The settings you enter will then be saved in a file called "config" in the main directory. If you want to change your settings, you can either change the config file or just delete the existing one and start the program again. 
In most cases there will be multiple in and outputs you can choose from and it can be confusing at the first start. If you dont have any clue, just make shure you dont pick any inputs like "microphone XY", trial and error, and if you didnt get the right ones, delete the config and start again. 

## Playlist
To play tracks from a playlist, just create one or more "playlist" file in your tracks dir and set the parameter like explained in the "Usage" section.

The content of a playlist file can look like this:
```
EvacuateTheEarth
Alienation
Observe
```

Just make shure, that these are the exact names of your track directories in your tracks/ dir like this:   
-> bandplay/tracks/EvacuateTheEarth/   
-> bandplay/tracks/Alienation/   
-> bandplay/tracks/Observe/   

## Multichannel Output 
If your using a device with multiple output channels like a Focusrite Scarlett 18i20, start like this:
1. You first need to delete your existing "config" file
3. Plug in your USB Interface
4. Start the program
5. Choose your Output channels (can be either Mono or Stereo)
6. The program will now create prebuild files in "bandplay/tracks/yourSong/prebuild/" (One wav file with multiple channels for your click and song tracks) and it can take a while until it finishes its work. This is neccessary because you can only stream ONE File to your USB Interface. 
7. If you want to change your click/song wav files in the future, dont forget to DELETE the prebuild files!


## How we use it
Initialy I started to wrote this program for my own band, as we hadnt any device to play our clicks plus synths back then. So I grabbed my old netbook and an old Focusrite Scarlet 2i2 that I attached to the netbook via USB so that we could play the click track via the USB Interface and the synth via the AUX Netbook Port.
Today we use this program still with the old Netbook, but with the Focusrite 18i20 as the output device. Its connected via USB and the click and song tracks are played through different Outputs of the Focusrite Interface. 
Just come to our shows to see this setup live in action :)

Check out my Band "Embrace The Light" here: http://embracethelight.de
