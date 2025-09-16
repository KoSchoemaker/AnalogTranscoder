from tkinter import filedialog
from tkinter import *
from tkinter import ttk

def browse_window(filenames):
    browse_lstbox.insert("end", filenames)

def browse_button():
    filenames = filedialog.askopenfilenames(filetypes=[("AVI", ".avi")])
    browse_window(filenames)

def generate():
    root = Tk()

    browse_button = Button(text="Browse", command=browse_button)
    browse_button.grid(row=0, column=0)

    browse_lstbox = Listbox(root)
    browse_lstbox.grid(row=0, column=1, columnspan = 3)

    scan_button = Button(text="Scan", command=browse_button)
    scan_button.grid(row=1, column=0)

    output_lstbox = Listbox(root)
    output_lstbox.grid(row=1, column=1, columnspan = 3)

    settings_button = Button(text="Settings", command=browse_button)
    settings_button.grid(row=2, column=0)

    output_button = Button(text="Output", command=browse_button)
    output_button.grid(row=2, column=1)

    process_button = Button(text="Process", command=browse_button)
    process_button.grid(row=2, column=2)

    process_progress = ttk.Progressbar(root, orient = HORIZONTAL, length = 400, mode = 'determinate')
    process_progress.grid(row=3, column=1)

    log_lstbox = Listbox(root)
    log_lstbox.grid(row=4, column=1, columnspan = 3, rowspan = 3)

    mainloop()