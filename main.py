from General import *
from WindowAction import WindowAction
from Process import Process
from Scan import Scan
from Settings import Settings
from ScanCache import ScanCache

from tkinter import Tk

root = Tk()

settings = Settings()
scan = Scan(ScanCache("pts_cache"), settings)
process = Process(settings)

window_action = WindowAction(scan, process, settings)
window_action.generate_window(root)

print("Completed")
