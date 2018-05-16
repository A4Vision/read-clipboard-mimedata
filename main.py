import sys

import pyperclip
from PyQt5 import QtWidgets
from PyQt5.Qt import QApplication

DEFAULT_FORMAT='text/html'


class ClipboardReader(object):
    def __init__(self):
        self._clipboard = QApplication.clipboard()

    def formats(self):
        all_formats = self._clipboard.mimeData().formats()
        return [f for f in all_formats
                if len(self._clipboard.mimeData().data(f))]

    def get_format(self, format_name):
        return self._clipboard.mimeData().data(format_name)

    def set_text(self, content):
        pyperclip.copy(content)
        pyperclip.paste()


class UI(object):
    def ask_user(self, options_dict, message):
        for options_name, option_value in sorted(options_dict.items()):
            print("{}. {}".format(options_name, option_value))
        return input(message)

    def ask_user_loop(self, options, message):
        options_dict = {i: f for i, f in enumerate(options)}
        selection = -1
        while selection not in options_dict:
            selection_raw = self.ask_user(options_dict, message)
            if selection_raw.isnumeric():
                selection = int(selection_raw)
        return options_dict[selection]


def main():
    clipboard = ClipboardReader()
    formats = clipboard.formats()
    if not formats:
        print("Clipboard is empty")
        return
    ui = UI()
    if DEFAULT_FORMAT in formats:
        selected_format = DEFAULT_FORMAT
    else:
        selected_format = ui.ask_user_loop(formats, "Select clipboard format: ")
    content = clipboard.get_format(selected_format)
    print(content)
    clipboard.set_text(str(content))


if __name__ == "__main__":
    global app
    app = QtWidgets.QApplication(sys.argv)
    main()
