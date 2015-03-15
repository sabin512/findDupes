import findDupes

PATH_TO_PROCESS = '/Music/PunkRock/Lagwagon'

class TextUI:
    def show_message(self, message):
        print(message)
    def show_warning(self, message):
        print('WARNING %s' % message)
    def add_dupe(self, dupe_description):
        print(dupe_description)

finder = findDupes.DupeFinder()
finder.ui = TextUI()
finder.scan(PATH_TO_PROCESS)
finder.list_dict()
