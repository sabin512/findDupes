import threading
from gi.repository import GLib, Gtk
import findDupes

class FindDupesGtk(Gtk.Window):
    def __init__(self, dupe_finder):
        self.dupe_finder = dupe_finder
        Gtk.Window.__init__(self, title='Gtk Front-end for findDupes')

        self.set_default_size(640, 480) #nostalgia sizing
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(main_box)

        top_box = Gtk.Box(spacing=5)
        main_box.pack_start(top_box, False, False, 0)

        chooser_title = 'Pick a directory to scan'
        action = Gtk.FileChooserAction.SELECT_FOLDER
        self.path_chooser_button = Gtk.FileChooserButton.new(chooser_title, action)
        top_box.pack_start(self.path_chooser_button, False, False, 0)
              
        self.scan_button = Gtk.Button('Scan')
        self.scan_button.connect('clicked', self.on_scan_button_clicked)
        top_box.pack_start(self.scan_button, False, False, 0)
        
        self.dupes_liststore = Gtk.ListStore(str)             
        treeview = Gtk.TreeView(self.dupes_liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Possible Duplicates', renderer, text=0)
        treeview.append_column(column)
        scrollable_treelist = Gtk.ScrolledWindow()
        scrollable_treelist.set_vexpand(True)
        scrollable_treelist.set_hexpand(True)
        
        scrollable_treelist.add(treeview)

        main_box.pack_start(scrollable_treelist, True, True, 0)

        console_scrolledwindow = Gtk.ScrolledWindow()
        console_scrolledwindow.set_hexpand(True)
        console_scrolledwindow.set_vexpand(True)
        textview = Gtk.TextView()
        textview.set_editable(False)
        self.textbuffer = textview.get_buffer()
        console_scrolledwindow.add(textview)

        main_box.pack_start(console_scrolledwindow, True, True, 0)
        
        self.show_all()

    def on_scan_button_clicked(self, widget):
        self.dupes_liststore.clear()
        self.scan_button.set_label('Scanning...')
        self.scan_button.set_sensitive(False)
        scan_thread = threading.Thread(target=self.run_scan)
        scan_thread.start()

    def run_scan(self):
        dir_to_scan = self.path_chooser_button.get_filename()
        self.show_message('Scanning %s...' % dir_to_scan)
        self.dupe_finder.scan(dir_to_scan)
        self.dupe_finder.list_dict()
        GLib.idle_add(self.scan_button.set_label, 'Scan')
        GLib.idle_add(self.scan_button.set_sensitive, True)

    def show_message(self, message):
        GLib.idle_add(self.console_append, message)
    def show_warning(self, message):
        GLib.idle_add(self.console_append, 'WARNING %s' % message)
    def add_dupe(self, dupe_description):
        self.dupes_liststore.append([dupe_description])

    def console_append(self, message):
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.insert(end_iter, message + '\n')

#chickens, eggs and bad design
finder = findDupes.DupeFinder()
win = FindDupesGtk(finder)
finder.ui = win

win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
