from tkinter import scrolledtext, END

class LogHelper():

    def __init__(self, master):

        log_lstbox = scrolledtext.ScrolledText(master, width=100, height=6)
        log_lstbox.grid(row=4, column=0, padx=20, pady=5, sticky="WE")

        self.output = log_lstbox

    def write(self, line):
        self.output.insert(END, line)
        self.output.yview(END)

    def flush(self):
        pass
