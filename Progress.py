from tkinter import DoubleVar
import re
from General import *


class Progress:
    def __init__(self):
        self.progress_var = DoubleVar()
        self.progress_var.set(0)

        self.duration = None

        self.progress_pattern = re.compile(
            r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)')
        
        # "pts_time": "0.000000",
        self.probe_pattern = re.compile(r'\"pts_time\":\s*\"([\d.]+)\"')
        

    # https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/utils.py#L43
    def parse_process_progress(self, line):
        items = {
            key: value for key, value in self.progress_pattern.findall(line)
        }

        if not items:
            return None
        
        if 'time' in items and items['time'] != '' and self.duration != None:
            current_time = timecode_to_sec(items['time'])
            self.update_progress(current_time)

    def parse_scan_progress(self, line):
        item = self.probe_pattern.search(line)
        if item and self.duration != None:
            current_time = float(item.group(1))
            self.update_progress(current_time)
    
    def update_progress(self, current_time: int):
        perc = current_time / self.duration *100
        if perc > 100.0:
            perc = 100
        self.progress_var.set(perc)

    def flush_progress(self):
        self.duration = None
        self.progress_var.set(0)