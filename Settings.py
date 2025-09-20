from tkinter import BooleanVar


class Settings:
    def __init__(self):
        self.dry_run = BooleanVar()
        self.test_run = BooleanVar()
        self.use_cache = BooleanVar()
        self.extension_string = ".mp4"

    def get_dry_run(self) -> bool:
        return self.dry_run.get()

    def get_test_run(self) -> bool:
        return self.test_run.get()

    def get_crf(self) -> int:
        if self.test_run.get() == True:
            return 26
        return 20

    def get_preset_mode(self) -> str:
        if self.test_run.get == True:
            return 'ultrafast'
        return 'slow'
