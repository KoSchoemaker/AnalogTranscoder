from tkinter import *
from Progress import Progress

class LogHelper():

    def __init__(self, text_ctrl):
        self.output = text_ctrl
        self.progress = Progress()
        
    def write(self, line):
        self.output.insert(END, line)
        self.output.yview(END)

        # self.progress.parse_progress(line)

    def flush(self):
        pass