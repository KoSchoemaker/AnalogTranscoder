from tkinter import IntVar
import re
import json
from General import *


class Progress:
    def __init__(self):
        self.progress_var = IntVar()
        self.progress_var.set(0)
        self.progress_pattern = re.compile(
            r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)')
        # self.probe_pattern = re.compile(r'pts_time\=\s*([\d.]+)')
        self.duration_pattern = re.compile(r'Duration:\s*([\d:.]+)')
        self.duration = None

        self.last_update = 0

    # https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/utils.py#L43
    def parse_progress(self, line):
        # print(line)
        # print()
        # if self.duration == None:

            # item = self.duration_pattern.search(line)
            # if item:
                # print(item.group(1))
                # self.duration = timecode_to_sec(item.group(1))

        items = {
            key: value for key, value in self.progress_pattern.findall(line)
        }

        if not items:
            return None
        
        if 'time' in items and items['time'] != '' and ':' in items['time'] and self.duration != None:

            current_time = timecode_to_sec(items['time'])
            perc = current_time / self.duration *100
            if perc > 100.0:
                perc = 100
            # print(current_time, perc)
            self.update_progress(round(perc))

    def set_scan_duration(self):
        pass
    
    def parse_scan_progress(self, line):
        if self.last_update < 10:
            print(line)
            self.last_update += 1
        if self.duration == None:

            item = self.duration_pattern.search(line)
            if item:
                print(item.group(1))
                self.duration = timecode_to_sec(item.group(1))

        try:        
            info = json.loads(line)
        except ValueError:
            return None
        
        if "pts_time" in info and self.duration != None:
            current_time = float(info["pts_time"])
        
            perc = current_time / self.duration *100
            if perc > 100.0:
                perc = 100
            # print(current_time, perc)
            self.update_progress(round(perc))
    
    # val between 0 and 100
    def update_progress(self, val: int):
        self.progress_var.set(val)

    def flush_progress(self):
        self.duration = None
        self.progress_var.set(0)