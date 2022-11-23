# Bandplay
You need a Click/Track Player for your band, but dont have the money for expensive gear? Your Windows Laptop is crashing if your playing a live show (Hello Whitechapel :D)? Or maybe you just want an open source solution to play your clicks and tracks in your rehearsal room. 

## Usage
Determine the selection of tracks (in track dir) yourself
```
python3 bandplay.py -d tracks
```
Play a list of tracks from a playlist
```
python3 bandplay.py -d tracks -p playlist
```

## Playlist
To play tracks from a playlist, just create a "playlist" file in your tracks dir and set the parameter like explained in the "Usage" section.

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


## How we use it
Initialy I started to wrote this program for my own band, as we hadnt any device to play our clicks plus synths back then. So I grabbed my old netbook and an old Focusrite Scarlet 2i2 that I attached to the netbook via USB so that we could play the click track via the USB Interface and the synth via the AUX Netbook Port.
Today we use this program still with the old Netbook, but with the Focusrite 18i20 as the output device. Its connected via USB and the click and song tracks are played through different Outputs of the Focusrite Interface. 
Just come to our shows to see this setup live in action :)

Check out my Band "Embrace The Light" here: http://embracethelight.de
