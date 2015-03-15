import os.path
import os
from collections import defaultdict
from mutagen.mp3 import MP3
from gi.repository import Gtk

MP3_EXTENSION = '.mp3'
PATH_TO_PROCESS = '/Music'

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

class TextUI:
    def show_message(self, message):
        print(message)
    def show_warning(self, message):
        print('WARNING %s' % message)
    def add_dupe(self, dupe_description):
        print(dupe_description)

class FindDupesGtk(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Gtk Front-end for findDupes')
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)
        self.dupes_liststore = Gtk.ListStore(str)             
        self.treeview = Gtk.TreeView(self.dupes_liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Possible Duplicates', renderer, text=0)
        self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 600, 400)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()

    def show_message(self, message):
        print(message)
    def show_warning(self, message):
        print('WARNING %s' % message)
    def add_dupe(self, dupe_description):
        self.dupes_liststore.append([dupe_description])

class DupeFinder:
    song_list = list()
    song_length_dict = defaultdict(list)
                                           
    def __init__(self, ui):
        self.ui = ui

    def scan(self, directory):
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
	

#ui = TextUI()
#finder = DupeFinder(ui)
#finder.scan(PATH_TO_PROCESS)
#finder.list_dict()

win = FindDupesGtk()
finder = DupeFinder(win)
finder.scan(PATH_TO_PROCESS)
finder.list_dict()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()

