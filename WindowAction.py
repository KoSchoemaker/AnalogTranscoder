from General import *

from tkinter import filedialog
from tkinter import *
from tkinter import ttk

from Process import Process
from Scan import Scan
from ScanCache import ScanCache


class WindowAction:
    def __init__(self, scan: Scan, process: Process):
        self.scan = scan
        self.process = process

        self.imported_files = None
        self.output_data = None

        self.browse_lstbox = None
        self.output_lstbox = None

    def browse(self):
        filepaths = filedialog.askopenfilenames(filetypes=[("AVI", ".avi")])
        self.imported_files = filepaths
        for path in filepaths:
            if not path.endswith(".avi"):
                log_action(f'Skip {path}, not AVI')
                continue
            self.browse_lstbox.insert("end", path)

    # Takes output_file_dict <dict> {input_path:{output_path_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def set_scan_results(self, output_lstbox, output_file_dict):
        for input_path, item in output_file_dict.items():
            print(input_path, item)
            output_lstbox.insert(
                "end", f"{input_path} : {len(item)} output files")
            for output_path, details in item.items():
                begin = sec_to_timecode(
                    details["start_t"]) if details["start_t"] != None else "BEGIN"
                end = sec_to_timecode(
                    details["end_t"]) if details["end_t"] != None else "END"
                dur = sec_to_timecode(details["duration"])
                gap_dur = sec_to_timecode(
                    details["gap_duration"]) if details["gap_duration"] != None else None
                formatted_string = f"-- {begin} - {end} ({dur})  ||  {output_path}"
                output_lstbox.insert("end", formatted_string)
                if gap_dur != None:
                    formatted_string = f"-- -- GAP ({gap_dur})"
                    output_lstbox.insert("end", formatted_string)

    def on_scan(self):
        output_file_dict = self.scan.run_scan(self.imported_files)

        self.output_data = output_file_dict
        self.set_scan_results(self.output_lstbox, output_file_dict)

    def on_process(self):
        if self.output_data == None:
            log_action("First scan, then process")
            return
        
        log_action("Starting process")
        self.process.run_batch(self.output_data)
        log_action("Process end")

    def generate_window(self):

        root = Tk()

        self.browse_lstbox = Listbox(root, width=100, height=15)
        self.browse_lstbox.grid(row=0, column=1, columnspan=3)

        browse_button = Button(text="Browse", command=lambda: self.browse())
        browse_button.grid(row=0, column=0)

        self.output_lstbox = Listbox(root, width=100, height=15)
        self.output_lstbox.grid(row=1, column=1, columnspan=3)

        scan_button = Button(text="Scan", command=self.on_scan)
        scan_button.grid(row=1, column=0)

        settings_button = Button(
            text="Settings", command=lambda: self.print_filenames())
        settings_button.grid(row=2, column=0)

        output_button = Button(
            text="Output", command=lambda: self.print_filenames())
        output_button.grid(row=2, column=1)

        process_button = Button(
            text="Process", command=self.on_process_batch)
        process_button.grid(row=2, column=2)

        process_progress = ttk.Progressbar(
            root, orient=HORIZONTAL, length=600, mode='determinate')
        process_progress.grid(row=3, column=0, columnspan=4)

        log_lstbox = Listbox(root, width=100, height=5)
        log_lstbox.grid(row=4, column=0, columnspan=4)

        mainloop()

    def print_filenames(self):
        print(self.imported_files)
