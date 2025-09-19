from General import *

from tkinter import filedialog

class WindowAction:
    def __init__(self):
        self.imported_files = []

    def get_imported_files(self):
        return self.imported_files

    def browse(self, browse_lstbox):
        filepaths = filedialog.askopenfilenames(filetypes=[("AVI", ".avi")])
        self.imported_files = filepaths
        for path in filepaths:
            browse_lstbox.insert("end", path)

    # Takes output_file_dict <dict> {input_path:{output_path_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def set_scan_results(self, output_lstbox, output_file_dict):
        for input_path, item in output_file_dict.items():
            print(input_path, item)
            output_lstbox.insert("end", f"{input_path} : {len(item)} output files")
            for output_path, details in item.items():
                begin = sec_to_timecode(details["start_t"]) if details["start_t"]!= None else "BEGIN"
                end = sec_to_timecode(details["end_t"]) if details["end_t"]!= None else "END"
                dur = sec_to_timecode(details["duration"])
                gap_dur = sec_to_timecode(details["gap_duration"]) if details["gap_duration"]!= None else None
                formatted_string = f"-- {begin} - {end} ({dur})  ||  {output_path}"
                output_lstbox.insert("end", formatted_string)
                if gap_dur != None:
                    formatted_string = f"-- -- GAP ({gap_dur})"
                    output_lstbox.insert("end", formatted_string)

    def print_filenames(self):
        print(self.imported_files)