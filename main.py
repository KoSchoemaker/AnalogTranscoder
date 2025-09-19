from General import *

from tkinter import *
from tkinter import ttk

from WindowAction import WindowAction
from Process import Process
from Scan import Scan
from ScanCache import ScanCache

# os.makedirs(output_directory, exist_ok=True)
# os.makedirs(cache_directory, exist_ok=True)

if test_mode:
    crf_value = 26
    preset_mode = 'ultrafast'
else:
    crf_value = 20
    preset_mode = 'slow'

scan = Scan(ScanCache("pts_cache"))
process = Process(crf_value, preset_mode)
window_action = WindowAction()

imported_files = []

root = Tk()

browse_lstbox = Listbox(root, width=100, height=15)
browse_lstbox.grid(row=0, column=1, columnspan=3)

browse_button = Button(
    text="Browse", command=lambda: window_action.browse(browse_lstbox))
browse_button.grid(row=0, column=0)

output_lstbox = Listbox(root, width=100, height=15)
output_lstbox.grid(row=1, column=1, columnspan=3)

scan_button = Button(
    text="Scan", command=lambda: window_action.set_scan_results(output_lstbox, scan.run_scan(window_action.get_imported_files())))
scan_button.grid(row=1, column=0)

settings_button = Button(
    text="Settings", command=lambda: window_action.print_filenames())
settings_button.grid(row=2, column=0)

output_button = Button(
    text="Output", command=lambda: window_action.print_filenames())
output_button.grid(row=2, column=1)

process_button = Button(
    text="Process", command=lambda: window_action.print_filenames())
process_button.grid(row=2, column=2)

process_progress = ttk.Progressbar(
    root, orient=HORIZONTAL, length=600, mode='determinate')
process_progress.grid(row=3, column=0, columnspan=4)

log_lstbox = Listbox(root, width=100, height=5)
log_lstbox.grid(row=4, column=0, columnspan=4)

mainloop()



print("Completed")
