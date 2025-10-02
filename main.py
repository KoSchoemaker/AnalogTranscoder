from General import *
from WindowAction import WindowAction
from WindowBuilder import WindowBuilder
from Process import Process
from Scan import Scan
from Settings import Settings
from ScanCache import ScanCache
from Progress import Progress
from LogHelper import LogHelper

from tkinter import Tk, scrolledtext, END
import sys

root = Tk()

log_lstbox = scrolledtext.ScrolledText(root, width=100, height=6)
log_lstbox.grid(row=4, column=0, padx=20, pady=5, sticky="WE")


redir = LogHelper(log_lstbox)
progress = Progress()
settings = Settings()
scan = Scan(ScanCache("pts_cache"), settings, progress)
process = Process(settings, progress)

window_action = WindowAction(scan, process, settings, progress)
window_builder = WindowBuilder(window_action)

sys.stdout = redir
sys.stderr = redir

window_builder.generate_window(root)