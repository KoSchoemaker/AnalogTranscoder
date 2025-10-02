from tkinter import DoubleVar
import re

from General import timecode_to_sec


class Progress:
    def __init__(self):
        self.progress_var = DoubleVar()
        self.progress_var.set(0)

        self.duration = None

        # frame= 119 fps=0.0 q=28.0 size= 0KiB time=00:00:04.68 bitrate= 0.1kbits/s speed=9.11x elapsed=0:00:00.51
        self.progress_pattern = re.compile(
            r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)')

        # "pts_time": "0.000000",
        self.probe_pattern = re.compile(r'\"pts_time\":\s*\"([\d.]+)\"')

    # Inspiration: https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/utils.py#L43
    def parse_process_progress(self, line):
        items = {
            key: value for key, value in self.progress_pattern.findall(line)
        }

        if not items:
            return None

        if 'time' in items and items['time'] != '' and ':' in items['time'] and self.duration != None:
            current_time = timecode_to_sec(items['time'])
            self.__update_progress(current_time)

    def parse_scan_progress(self, line):
        item = self.probe_pattern.search(line)
        if item and self.duration != None:
            current_time = float(item.group(1))
            self.__update_progress(current_time)

    def flush_progress(self):
        self.duration = None
        self.progress_var.set(0)

    def __update_progress(self, current_time: int):
        perc = current_time / self.duration * 100
        if perc > 100.0:
            perc = 100
        self.progress_var.set(perc)
