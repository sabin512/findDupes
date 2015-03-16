import os.path
import os
from collections import defaultdict
from mutagen.mp3 import MP3

MP3_EXTENSION = '.mp3'

def get_song(filename):        
    audio = MP3(filename)
    length = audio.info.length
    size = os.path.getsize(filename)
    return Song(filename, size, length)


class Song:
    def __init__(self, filename, size, length):
        self.filename = filename
        self.size = size
        self.length = length

class DupeFinder:
    song_list = list()
    song_length_dict = defaultdict(list)
                                           
    def scan(self, directory):
        self.song_list = list()
        self.song_length_dict = defaultdict(list)
        self.build_song_list(directory)
        self.find_dupes()

    def add_song(self, filename):
        if not filename.endswith(MP3_EXTENSION):
            self.ui.show_warning('Skipping non-song %s' % os.path.basename(filename))
            return
        self.song_list.append(get_song(filename))

    def build_song_list(self, directory):                
        for root, dirs, files in os.walk(directory):
            self.ui.show_message('Processing %s with %d files' % (root, len(files)))
            for name in files:
                self.add_song(os.path.join(root, name))
                

    def find_dupes(self):
        for song in self.song_list:
            self.song_length_dict[song.length].append(song)

    def list_dict(self):
        for dupe_length, dupe_list in self.song_length_dict.items():
            if len(dupe_list) > 1:
                self.ui.show_message('Found %d songs with length %d' % (len(dupe_list),dupe_length))
                for song in dupe_list:
                    self.ui.add_dupe(song.filename)
	


