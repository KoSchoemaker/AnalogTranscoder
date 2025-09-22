from General import *

from tkinter import filedialog
from tkinter import *
from tkinter import ttk

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
        for path in filepaths:
            if not path.endswith(".avi"):
                print(f'Skip {path}, not AVI')
                continue
            browse_lstbox.insert("end", path)

    def set_output_directory(self):
        if self.output_data == None:
            print("First scan, then set dir")
            return
        filedir = filedialog.askdirectory()
        self.settings.output_dir.set(filedir)
        self.scan.scan_output_directory(filedir, self.output_data)


    # Takes output_file_dict <dict> {input_path:{output_path_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def set_scan_results(self, output_lstbox: Listbox, output_file_dict):
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

    def on_scan(self, output_lstbox: Listbox):
        if self.imported_files == None or self.imported_files == []:
            print("No files selected. First browse")
            return
        output_file_dict = self.scan.run_scan(self.imported_files)

        self.output_data = output_file_dict
        self.set_scan_results(output_lstbox, output_file_dict)

    def on_process(self):
        if self.output_data == None:
            print("First scan, then process")
            return
        
        print("Starting process")
        self.process.run_batch(self.output_data)
        print("Process end")

    # def generate_window(self, root):

    #     self.build_browse(root)
    #     self.build_scan(root)
    #     self.build_process(root)

    #     mainloop()

    # def build_browse(self, root):

    #     lf_browse = LabelFrame(root, text='1: Browse files')
    #     lf_browse.grid(column=0, row=0, padx=20, pady=20)

    #     self.browse_lstbox = Listbox(lf_browse, width=100, height=15)
    #     self.browse_lstbox.grid(row=0, column=2)

    #     browse_button = Button(lf_browse, text="Browse", command=lambda: self.browse())
    #     browse_button.grid(row=0, column=0)

    # def build_scan(self, root):

    #     lf_scan = LabelFrame(root, text='2: Scan selected files')
    #     lf_scan.grid(column=0, row=1, padx=20, pady=20)

    #     settings_frame = Frame(lf_scan)
    #     settings_frame.grid(row=0, column=1, sticky="N")

    #     use_cache = Checkbutton(settings_frame, text='Use Cache', var=self.settings.use_cache)
    #     use_cache.grid(row=0, column=0, sticky="W")

    #     save_to_cache = Checkbutton(settings_frame, text='Save to Cache', var=self.settings.save_to_cache)
    #     save_to_cache.grid(row=1, column=0, sticky="W")

    #     dry_run = Checkbutton(settings_frame, text='dryrun (no actions)', var=self.settings.dry_run)
    #     dry_run.grid(row=3, column=0, sticky="W")

    #     test_run = Checkbutton(settings_frame, text='testrun (quick actions)', var=self.settings.test_run)
    #     test_run.grid(row=4, column=0, sticky="W")

    #     self.output_lstbox = Listbox(lf_scan, width=100, height=15)
    #     self.output_lstbox.grid(row=0, column=2)

    #     scan_button = Button(lf_scan, text="Scan", command=self.on_scan)
    #     scan_button.grid(row=0, column=0)

    # def build_process(self, root):
    #     pass
    #     # settings_button = Button(
    #     #     text="Settings", command=lambda: self.print_filenames())
    #     # settings_button.grid(row=2, column=0)

    #     # output_button = Button(
    #     #     text="Output", command=lambda: self.print_filenames())
    #     # output_button.grid(row=2, column=1)

    #     # process_button = Button(
    #     #     text="Process", command=self.on_process)
    #     # process_button.grid(row=2, column=2)

    #     # process_progress = ttk.Progressbar(
    #     #     root, orient=HORIZONTAL, length=600, mode='determinate')
    #     # process_progress.grid(row=3, column=0, columnspan=4)

    #     # log_lstbox = Listbox(root, width=100, height=5)
    #     # log_lstbox.grid(row=4, column=0, columnspan=4)

    def print_filenames(self):
        print(self.imported_files)
