#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget

failure_list = []
success_list = []
verbose = False

global_modules_to_test = ["PyQt5", "matplotlib", "mplfinance", "numpy", "sqlite3", "pytz"]
windows_modules_to_test = ["win32gui", "win32api", "win32con", "win32process", "win32event", "win32console", "winpaths"]
linux_modules_to_test = ["xcffib", "xcffib.xproto"]
mac_modules_to_test = []
posix_modules_to_test = []

def qt_output(message):
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("FPDB")
    window.setGeometry(100, 100, 600, 400)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout()
    central_widget.setLayout(layout)
    
    listbox = QListWidget()
    for item in message:
        listbox.addItem(item)
    layout.addWidget(listbox)
    
    window.show()
    sys.exit(app.exec_())

def try_import(modulename):
    try:
        module = __import__(modulename)
        success(module)
    except:
        failure(f'File not found: {modulename}')
        if modulename == "win32console":
            failure("We appear to be running in Windows, but the Windows Python Extensions are not loading. Please install the PYWIN32 package from http://sourceforge.net/projects/pywin32/")
        if modulename == "pytz":
            failure("Unable to import PYTZ library. Please install PYTZ from http://pypi.python.org/pypi/pytz/")
        return False

    if modulename == "matplotlib":
        try:
            module.use('qt5agg')
            success("matplotlib/qt5agg")
            return False
        except:
            failure("matplotlib/qt5agg")
            return False

    return True

def success(message):
    if verbose:
        print(message)
    success_list.append(str(message))

def failure(message):
    if verbose:
        print("Error:", message)
    failure_list.append(message)

class ChooseLanguage(QMainWindow):
    def __init__(self, language_dict):
        super().__init__()
        self.setWindowTitle("Choose a language for FPDB")
        self.setGeometry(100, 100, 350, 350)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.listbox = QListWidget()
        self.listbox.addItem("Use the system language settings")
        self.listbox.addItem("en -- Always use English for FPDB")
        for key in sorted(language_dict.keys()):
            self.listbox.addItem(f"{key} -- {language_dict[key]}")
        layout.addWidget(self.listbox)
        
        self.listbox.setCurrentRow(0)
        self.selected_language = ""
        
        self.listbox.itemDoubleClicked.connect(self.callbackLanguage)

    def callbackLanguage(self, item):
        if self.listbox.currentRow() == 0:
            self.selected_language = ""
        else:
            self.selected_language = item.text()
        self.close()

    def getLanguage(self):
        return self.selected_language.split(" -- ", 1)[0]

if __name__ == "__main__":
    try:
        module = __import__("sys")
    except:
        failure("python failure - could not import sys module")
        qt_output(failure_list)
        sys.exit(1)
    
    try:
        module = __import__("L10n")
    except:
        failure("fpdb modules cannot be loaded, check that fpdb is installed in an English path")
        qt_output(failure_list)
        sys.exit(1)

    try:
        if sys.argv[1] == "-v":
            verbose = True
    except:
        pass

    import Configuration
    config = Configuration.Config()

    for i in global_modules_to_test:
        try_import(i)
    if config.os_family in ("XP", "Win7"):
        for i in windows_modules_to_test:
            try_import(i)
    elif config.os_family == "Linux":
        for i in linux_modules_to_test:
            try_import(i)
    elif config.os_family == "Mac":
        for i in mac_modules_to_test:
            try_import(i)
    if config.posix:
        for i in posix_modules_to_test:
            try_import(i) 

    if len(failure_list):
        qt_output(failure_list)

    if config.install_method == "exe":
        if len(failure_list):
            sys.exit(1)
    
    if len(failure_list):
        if config.os_family in ("XP", "Win7"):
            sys.exit(1)
        else:
            sys.exit(failure_list)

    if config.example_copy:
        import L10n
        language_dict, null = L10n.get_installed_translations()
        app = QApplication(sys.argv)
        chooser = ChooseLanguage(language_dict)
        chooser.show()
        app.exec_()
        chosen_lang = chooser.getLanguage()

        if chosen_lang:
            conf = Configuration.Config()
            conf.set_general(lang=chosen_lang)
            conf.save()

        initial_run = "-i"
    else:
        initial_run = ""

    if config.install_method == "exe":
        if initial_run:
            sys.exit(2)
        else:
            sys.exit(0)

    import os
    os.chdir(os.path.join(config.fpdb_root_path, ""))
    if config.os_family in ("XP", "Win7"):
        os.execvpe('pythonw.exe', list(('pythonw.exe', 'fpdb.pyw', initial_run, '-r'))+sys.argv[1:], os.environ)
    else:
        os.execvpe('python', list(('python', 'fpdb.pyw', initial_run, '-r'))+sys.argv[1:], os.environ)