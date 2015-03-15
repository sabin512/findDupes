from gi.repository import Gtk
import findDupes

PATH_TO_PROCESS = '/Music'

class FindDupesGtk(Gtk.Window):
    def __init__(self, dupe_finder):
        self.dupe_finder = dupe_finder
        Gtk.Window.__init__(self, title='Gtk Front-end for findDupes')

        self.set_default_size(640, 480) #nostalgia sizing
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(main_box)

        top_box = Gtk.Box(spacing=5)
        main_box.pack_start(top_box, False, False, 0)
        
        self.path_entry = Gtk.Entry()
        self.path_entry.set_text(PATH_TO_PROCESS)
        top_box.pack_start(self.path_entry, True, True, 0)
        
        self.scan_button = Gtk.Button('Scan')
        self.scan_button.connect('clicked', self.on_scan_button_clicked)
        top_box.pack_start(self.scan_button, False, False, 0)
        
        self.dupes_liststore = Gtk.ListStore(str)             
        self.treeview = Gtk.TreeView(self.dupes_liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Possible Duplicates', renderer, text=0)
        self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        
        self.scrollable_treelist.add(self.treeview)

        main_box.pack_start(self.scrollable_treelist, True, True, 0)
        
        self.show_all()

    def on_scan_button_clicked(self, widget):
        self.show_message('Scanning...')
        self.dupe_finder.scan(self.path_entry.get_text())
        self.dupe_finder.list_dict()

    def show_message(self, message):
        print(message)
    def show_warning(self, message):
        print('WARNING %s' % message)
    def add_dupe(self, dupe_description):
        self.dupes_liststore.append([dupe_description])

#chickens, eggs and bad design
finder = findDupes.DupeFinder()
win = FindDupesGtk(finder)
finder.ui = win

win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
