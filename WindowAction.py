from General import *

from tkinter import filedialog

def browse_window(filenames, browse_lstbox):
    browse_lstbox.insert("end", filenames)

def browse(browse_lstbox):
    filenames = filedialog.askopenfilenames(filetypes=[("AVI", ".avi")])
    imported_files = filenames
    browse_window(filenames, browse_lstbox)

def print_filenames():
    print(imported_files)