from tkinter import *

class LogHelper():

    def __init__(self, text_ctrl):
        self.output = text_ctrl
        
    def write(self, string):
        self.output.insert(END, string)

    def flush(self):
        pass