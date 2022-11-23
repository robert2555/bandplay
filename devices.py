
class OutputDevice:
    def __init__(self, name, channels, song_ch, click_ch):
        self.name = name
        self.channels = int(channels)
        self.song_ch = song_ch
        self.click_ch = click_ch
    stereo = True
    stream = []
