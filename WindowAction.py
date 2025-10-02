from General import sec_to_timecode

from tkinter import filedialog
from tkinter import *

from Process import Process
from Scan import Scan
from Settings import Settings
from Progress import Progress


class WindowAction:
    def __init__(self, scan: Scan, process: Process, settings: Settings, progress: Progress):
        self.scan = scan
        self.process = process
        self.settings = settings
        self.progress = progress

        self.imported_files = None
        self.output_data = None

    def browse(self, browse_lstbox: Listbox):
        filepaths = filedialog.askopenfilenames(filetypes=[("AVI", ".avi")])
        self.imported_files = filepaths
        browse_lstbox.delete(0, END)
        for path in filepaths:
            if not path.endswith(".avi"):
                print(f'INFO: Skip {path}, not AVI')
                continue
            browse_lstbox.insert("end", path)

    def on_scan(self, output_lstbox: Listbox):
        if self.imported_files == None or self.imported_files == []:
            print("ACTION: No files selected. First browse")
            return
        output_file_dict = self.scan.run_scan(self.imported_files)

        self.output_data = output_file_dict
        self.__set_scan_results(output_lstbox, output_file_dict)

    def set_output_directory(self):
        if self.output_data == None:
            print("ACTION: First scan, then set dir")
            return
        filedir = filedialog.askdirectory()
        self.settings.output_dir.set(filedir)
        self.scan.scan_output_directory(filedir, self.output_data)

    def on_process(self):
        if self.output_data == None:
            print("ACTION: First scan, then process")
            return

        print("INFO: Processing starts...")
        self.process.run_batch(self.output_data)
        print("INFO: Process ended")

    # Takes output_file_dict <dict> {input_path:{output_path_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def __set_scan_results(self, output_lstbox: Listbox, output_file_dict):
        output_lstbox.delete(0, END)
        for input_path, item in output_file_dict.items():
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
