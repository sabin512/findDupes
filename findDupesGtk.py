from gi.repository import Gtk
import findDupes

PATH_TO_PROCESS = '/Music/PunkRock/Lagwagon'

class FindDupesGtk(Gtk.Window):
    def __init__(self, dupe_finder):
        self.dupe_finder = dupe_finder
        Gtk.Window.__init__(self, title='Gtk Front-end for findDupes')
        
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.scan_button = Gtk.Button('Scan')
        self.scan_button.connect('clicked', self.on_scan_button_clicked)
        
        self.dupes_liststore = Gtk.ListStore(str)             
        self.treeview = Gtk.TreeView(self.dupes_liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Possible Duplicates', renderer, text=0)
        self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)

        self.grid.attach(self.scan_button, 0, 0, 100, 24)
        self.grid.attach_next_to(self.scrollable_treelist, self.scan_button, Gtk.PositionType.BOTTOM, 640, 200)
        
        self.scrollable_treelist.add(self.treeview)
        self.show_all()

    def on_scan_button_clicked(self, widget):
        self.show_message('Scanning...')
        self.dupe_finder.scan(PATH_TO_PROCESS)
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
