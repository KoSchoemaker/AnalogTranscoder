from General import *

from WindowAction import WindowAction
from Process import Process
from Scan import Scan
from Settings import Settings
from ScanCache import ScanCache

# os.makedirs(output_directory, exist_ok=True)
# os.makedirs(cache_directory, exist_ok=True)

if test_mode:
    crf_value = 26
    preset_mode = 'ultrafast'
else:
    crf_value = 20
    preset_mode = 'slow'

settings = Settings()
scan = Scan(ScanCache("pts_cache"))
process = Process(settings)

window_action = WindowAction(settings, scan, process)

window_action.generate_window()

print("Completed")
