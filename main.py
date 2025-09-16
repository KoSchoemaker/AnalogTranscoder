from General import *

from tkinter import filedialog
from tkinter import *
from tkinter import ttk

import WindowAction
import Process
import Scan

local_dir = True

if local_dir:
    input_directory = r"D:\Capture\raw"
    output_directory = r"D:\Capture\out"
    cache_directory = r"D:\Capture\cache"

else:
    input_directory = r"E:\Capture\raw"
    output_directory = r"E:\Capture\2025\out"
    cache_directory = r"E:\Capture\2025\cache"

# os.makedirs(output_directory, exist_ok=True)
# os.makedirs(cache_directory, exist_ok=True)

imported_files = []

def generate_window():

    root = Tk()

    browse_lstbox = Listbox(root)
    browse_lstbox.grid(row=0, column=1, columnspan=3)

    browse_button = Button(
        text="Browse", command=lambda: WindowAction.browse(browse_lstbox))
    browse_button.grid(row=0, column=0)

    scan_button = Button(
        text="Scan", command=lambda: WindowAction.print_filenames())
    scan_button.grid(row=1, column=0)

    output_lstbox = Listbox(root)
    output_lstbox.grid(row=1, column=1, columnspan=3)

    settings_button = Button(
        text="Settings", command=lambda: WindowAction.print_filenames())
    settings_button.grid(row=2, column=0)

    output_button = Button(
        text="Output", command=lambda: WindowAction.print_filenames())
    output_button.grid(row=2, column=1)

    process_button = Button(
        text="Process", command=lambda: WindowAction.print_filenames())
    process_button.grid(row=2, column=2)

    process_progress = ttk.Progressbar(
        root, orient=HORIZONTAL, length=400, mode='determinate')
    process_progress.grid(row=3, column=1)

    log_lstbox = Listbox(root)
    log_lstbox.grid(row=4, column=1, columnspan=3, rowspan=3)

    mainloop()

generate_window()


# for i, filename in enumerate(os.listdir(input_directory)):
#     # if i == 0:
#     #     continue
#     if i >= limit:
#         log_action('Limit hit, breaking')
#         break
#     # if not filename.endswith(".avi"):
#     #     print(f'Skip {filename}')
#     #     continue

#     input_filepath = os.path.join(input_directory, filename)
#     output_filename = os.path.splitext(filename)[0]
#     output_filepath = os.path.join(output_directory, output_filename)

#     extension_string = ".mp4"

#     # Redirect stderr to a log file
#     log_action(f"Scanning {filename}")
#     if os.path.isfile(output_filepath):
#         log_action(f'{output_filename} already exists, skipping')
#         continue
#     try:
#         a_pts = get_packet_pts(input_filepath, cache_directory)

#         a_cuts = find_discontinuities(a_pts)

#         # add_to_cache(a_cuts)

#         for frame, start_t, end_t, duration in a_cuts:
#             log_action("Audio cut:", sec_to_timecode(start_t), " - ",
#                        sec_to_timecode(end_t), ", duration: ", sec_to_timecode(duration))
#         log_action("Total audio time:", sec_to_timecode(a_pts[-1]))

#         # only audio cuts
#         split_videos(input_filepath, a_cuts, output_filepath, extension_string)

#         print(f"-> Successfully converted {filename} to {output_filename}")

#     # with open(log_filename, 'w') as log_file:
#     #     log_file.write(process[1].decode('utf-8'))
#     #     print('info written to log file')

#     except ffmpeg.Error as e:
#         print(f"Error converting {filename}: {e}")
#         print('stdout:', e.stdout.decode('utf8'))
#         print('stderr:', e.stderr.decode('utf8'))
#     print('---')
print("Completed")
