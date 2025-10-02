from tkinter import Tk
import sys

from WindowAction import WindowAction
from WindowBuilder import WindowBuilder
from Process import Process
from Scan import Scan
from Settings import Settings
from ScanCache import ScanCache
from Progress import Progress
from LogHelper import LogHelper

root = Tk()

redir = LogHelper(root)
progress = Progress()
settings = Settings()
scan = Scan(ScanCache("pts_cache"), settings, progress)
process = Process(settings, progress)

window_action = WindowAction(scan, process, settings, progress)
window_builder = WindowBuilder(window_action)

sys.stdout = redir
sys.stderr = redir

window_builder.generate_window(root)