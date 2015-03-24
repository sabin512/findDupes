import argparse
import findDupes

class TextUI:
    dupe_list = list()
    def __init__(self, verbose, output):
        self.verbose = verbose
        self.output = output
    def show_message(self, message):
        print(message)
    def show_warning(self, message):
        if self.verbose:
            print('Warning %s' % message)
    def show_error(self, message):
        print('ERROR %s' % message)
    def add_dupe(self, dupe_description):
        self.dupe_list.append(dupe_description)
    def produce_list(self):
        if self.output:
            with open(self.output, 'w') as f:
                for dupe in self.dupe_list:
                    f.write(dupe + '\n')
            print('Wrote possible duplicates to %s' % self.output)
        else:
            for dupe in self.dupe_list:
                print(dupe)
            

parser = argparse.ArgumentParser()
parser.add_argument('path', help='path to scan for duplicate MP3s')
parser.add_argument('-v', '--verbose', help='be more verbose',
                    action='store_true')
parser.add_argument('-o', '--output',
                    help='store the dupe scan result into a given file')
args = parser.parse_args()

ui = TextUI(args.verbose, args.output)
finder = findDupes.DupeFinder()
finder.ui = ui
finder.scan(args.path)
finder.list_dict()

ui.produce_list()
