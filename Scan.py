from General import create_filename, timecode_to_sec, get_base_filename
from ScanCache import ScanCache
from Settings import Settings
from Progress import Progress
from Command import Command
import json
import os
import re


class Scan:
    def __init__(self, scan_cache: ScanCache, settings: Settings, progress: Progress):
        self.scan_cache = scan_cache
        self.settings = settings
        self.progress = progress

        self.duration_pattern = re.compile(r'Duration:\s*([\d:.]+)')

    # Returns <dict> {input_path:{output_filename_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def run_scan(self, filepaths):
        output_file_dict = {}
        for path in filepaths:
            self.progress.duration = self.get_duration(path)

            a_pts = self.__get_packet_pts(path)
            a_cuts = self.__find_discontinuities(a_pts)
            output_files = self.__calculate_output(a_cuts, a_pts, path)
            output_file_dict[path] = output_files

        return output_file_dict
    
    # Takes output_file_dict <dict> {input_path:{output_filename_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def scan_output_directory(self, output_filepath: str, output_file_dict):
        output_filenames = [det for _, details in output_file_dict.items()
                            for det in details.keys()]
        for filename in output_filenames:
            if os.path.isfile(os.path.join(output_filepath, filename)):
                print(
                    "ERROR: One or more files already exist in output dir. Select other dir or remove files.")
                return False
        print("INFO: output directory does not yet contain desired file names")
        return True

    def get_duration(self, filepath: str) -> float:
        cmd = ["ffprobe", "-i", filepath]
        process = Command.run(cmd)

        out, _ = process.communicate()
        item = self.duration_pattern.search(out)
        if item:
            return timecode_to_sec(item.group(1))

    def __get_packet_pts(self, filepath: str):

        base_filename = get_base_filename(filepath)

        if self.settings.get_use_cache() is True:
            cache_pts = self.scan_cache.get_pts_from_external_cache(
                base_filename)
            if cache_pts:
                return cache_pts

        print(f"INFO: Running ffprobe for {filepath}")
        pts = []
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_packets", "-of", "json", filepath
        ]

        process = Command.run(cmd)

        out = ""
        for line in process.stdout:
            self.progress.parse_scan_progress(line)
            out += line

        _, err = process.communicate()

        if process.returncode != 0:
            print(f'ERROR: ffprobe: {err}')
        print(f"INFO: ffprobe finished for {filepath}")
        self.progress.flush_progress()

        info = json.loads(out)
        for p in info.get("packets", []):
            if "pts_time" in p:
                pts.append(float(p["pts_time"]))

        if self.settings.get_save_to_cache() is True:
            print(f"INFO: Saving result for {filepath} to cache")
            self.scan_cache.add_pts_to_external_cache(base_filename, pts)
        return pts

    def __find_discontinuities(self, pts_list, gap_threshold=0.2):
        cuts = []
        prev = None
        for i, t in enumerate(pts_list):
            if prev is None:
                prev = t
                continue
            diff = t - prev
            if diff < -0.001 or diff > gap_threshold:  # negative = reset, large = gap
                cuts.append((i, prev, t, diff))
            prev = t

        if len(cuts) == 0:
            print(
                f"INFO: No cuts found, biggest frame diff: {diff} (threshold: {gap_threshold})")
        return cuts

    def __calculate_output(self, cuts, pts, input_filepath: str):
        base_filename = get_base_filename(input_filepath)

        output_videos = {}
        print(
            f"INFO: {len(cuts)} cut points found, will generate {len(cuts) + 1} video(s).")

        begin = None
        end = None
        addition = 1
        for frame, start_t, end_t, diff in cuts:
            # First video
            if begin == None and end == None:
                output_filename = create_filename(
                    base_filename, addition, self.settings.extension_string)
                output_videos[output_filename] = {
                    'start_t': None, "end_t": start_t, "duration": start_t, "gap_duration": diff}
                begin = end_t
                addition += 1

                continue

            end = start_t

            # Subsequent
            output_filename = create_filename(
                base_filename, addition, self.settings.extension_string)
            output_videos[output_filename] = {
                'start_t': begin, "end_t": end, "duration": end-begin, "gap_duration": diff}

            begin = end_t
            addition += 1

        # Last video
        output_filename = create_filename(
            base_filename, addition, self.settings.extension_string)
        output_videos[output_filename] = {'start_t': begin, "end_t": None,
                                          "duration": pts[-1]-(begin if begin != None else 0), "gap_duration": None}

        print(f"INFO: {input_filepath} completely scanned")
        return output_videos
