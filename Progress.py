from tkinter import IntVar

class Progress:
    def __init__(self):
        self.progress_step = IntVar()
        self.progress_step.set(0)

    def update_progress(self, val: int):
        self.progress_step.set(val)