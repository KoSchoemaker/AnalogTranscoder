from tkinter import *
from tkinter import ttk
import threading

from General import application_name, version
from WindowAction import WindowAction


class WindowBuilder:
    def __init__(self, window_action: WindowAction):
        self.window_action = window_action

        self.browse_lstbox = None
        self.output_lstbox = None

        self.labelframe_pad_x = 20
        self.labelframe_pad_y = 5

        self.listbox_pad_x = 20
        self.listbox_pad_y = 5

    def generate_window(self, master):

        master.geometry('1000x750')
        master.resizable(False, False)
        master.title(application_name + " v." + version)

        master.columnconfigure(0, weight=1)

        self.build_browse(master)
        self.build_scan(master)
        self.build_process(master)
        self.build_progress_bar(master)

        mainloop()

    def build_browse(self, master):

        lf_browse = LabelFrame(master, text='1: Browse files')
        lf_browse.grid(column=0, row=0, padx=self.labelframe_pad_x, pady=self.labelframe_pad_y, sticky="WE")
        lf_browse.columnconfigure(0, weight=1)
        lf_browse.columnconfigure(1, weight=1)

        self.browse_lstbox = Listbox(lf_browse, height=10, width=80)
        self.browse_lstbox.grid(row=0, column=1, padx=self.listbox_pad_x, pady=self.listbox_pad_y, sticky="WE")

        browse_button = Button(lf_browse, text="Browse", command=lambda: self.window_action.browse(self.browse_lstbox))
        browse_button.grid(row=0, column=0, padx=20, pady=20, sticky="WE")

    def build_scan(self, master):

        lf_scan = LabelFrame(master, text='2: Scan selected files')
        lf_scan.grid(column=0, row=1, padx=self.labelframe_pad_x, pady=self.labelframe_pad_y, sticky="WE")
        lf_scan.columnconfigure(0, weight=1)
        lf_scan.columnconfigure(1, weight=1)

        self.build_scan_settings(lf_scan)

        self.output_lstbox = Listbox(lf_scan, width=80, height=12)
        self.output_lstbox.grid(row=0, column=1, padx=self.listbox_pad_x, pady=self.listbox_pad_y, rowspan=2, sticky="WE")

        scan_button = Button(lf_scan, text="Scan", command=lambda: threading.Thread(target= lambda: self.window_action.on_scan(self.output_lstbox)).start())
        scan_button.grid(row=1, column=0, padx=20, pady=20, sticky="WE")

    def build_scan_settings(self, master):
        settings_frame = Frame(master)
        settings_frame.grid(row=0, column=0, padx=20, pady=20, sticky="WE")

        use_cache = Checkbutton(settings_frame, text='Use Cache', var=self.window_action.settings.use_cache)
        use_cache.grid(row=0, column=0, sticky="W")

        save_to_cache = Checkbutton(settings_frame, text='Save to Cache', var=self.window_action.settings.save_to_cache)
        save_to_cache.grid(row=1, column=0, sticky="W")

    def build_process(self, master):
        lf_process = LabelFrame(master, text='3: Process to output')
        lf_process.grid(column=0, row=2, padx=self.labelframe_pad_x, pady=self.labelframe_pad_y, sticky="WE")
        lf_process.columnconfigure(0, weight=1)
        lf_process.columnconfigure(1, weight=1)
        lf_process.columnconfigure(2, weight=1)

        self.build_process_settings(lf_process)
        self.build_process_output_dir(lf_process)

        process_button = Button(lf_process, text="Process", command=lambda: threading.Thread(target=self.window_action.on_process).start())
        process_button.grid(row=0, column=2, padx=20, pady=20, sticky="WE")

    def build_progress_bar(self, master):
        process_progress = ttk.Progressbar(
            master, orient=HORIZONTAL, length=100, mode='determinate', maximum=100, variable=self.window_action.progress.progress_var)
        process_progress.grid(row=3, column=0, padx=20, pady=5, sticky="WE")

    def build_process_settings(self, master):
        settings_frame = Frame(master)
        settings_frame.grid(row=0, column=0, padx=20, pady=20, sticky="WE")

        dry_run = Checkbutton(settings_frame, text='Dryrun (no actions)', var=self.window_action.settings.dry_run)
        dry_run.grid(row=3, column=0, sticky="W")

        test_run = Checkbutton(settings_frame, text='Testrun (quick actions)', var=self.window_action.settings.test_run)
        test_run.grid(row=4, column=0, sticky="W")

        crop_upscale = Checkbutton(settings_frame, text='Crop and upscale from DV', var=self.window_action.settings.crop_upscale, state="disabled")
        crop_upscale.grid(row=0, column=0, sticky="W")

    def build_process_output_dir(self, master):
        output_frame = Frame(master)
        output_frame.grid(row=0, column=1, padx=20, pady=20, sticky="WE")
        output_dir_entry = Entry(output_frame, width=40, textvariable = self.window_action.settings.output_dir, state="disabled")
        output_dir_entry.grid(row=0, column=1, sticky="E", ipadx=4, ipady=4, padx=10)
        output_browse = Button(output_frame, text="Output directory", command=self.window_action.set_output_directory)
        output_browse.grid(row=0, column=0, sticky="E")