from General import *
from ScanCache import ScanCache
import json
import subprocess
import os


class Scan:
    def __init__(self, scan_cache: ScanCache):
        self.scan_cache = scan_cache
        self.extension_string = ".mp4"

    # Returns <dict> {input_path:{output_path_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def run_scan(self, filepaths):
        all_output_file_data = {}
        for path in filepaths:
            a_pts = self.get_packet_pts(path)
            a_cuts = self.find_discontinuities(a_pts)
            output_files = self.calculate_output(a_cuts, a_pts, path)
            all_output_file_data[path] = output_files

        return all_output_file_data

    def get_packet_pts(self, filepath):

        base_filename = self.get_base_filename(filepath)

        cache_pts = self.scan_cache.get_pts_from_external_cache(base_filename)
        if cache_pts:
            return cache_pts

        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_packets", "-of", "json", filepath
        ]
        out = subprocess.check_output(cmd, text=True)
        info = json.loads(out)
        pts = []
        for p in info.get("packets", []):
            if "pts_time" in p:
                pts.append(float(p["pts_time"]))

        self.scan_cache.add_pts_to_external_cache(base_filename, pts)
        return pts

    def find_discontinuities(self, pts_list, gap_threshold=0.2):
        # returns indices where a gap or negative jump occurs
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
        return cuts

    def calculate_output(self, cuts, pts, input_filepath):
        base_filename = self.get_base_filename(input_filepath)

        output_videos = {}
        log_action(
            f"-- {len(cuts)} cut points found, will generate {len(cuts) + 1} video(s).")

        begin = None
        end = None
        addition = 1
        for frame, start_t, end_t, diff in cuts:
            # first video
            if begin == None and end == None:
                output_filename = create_filename(
                    base_filename, addition, self.extension_string)
                output_videos[output_filename] = {'start_t':None, "end_t": start_t, "duration": start_t, "gap_duration": diff}
                begin = end_t
                addition += 1

                continue

            end = start_t

            # subsequent
            output_filename = create_filename(
                base_filename, addition, self.extension_string)
            output_videos[output_filename] = {'start_t':begin, "end_t": end, "duration": end-begin, "gap_duration": diff}

            begin = end_t
            addition += 1

        # last video
        output_filename = create_filename(base_filename, addition, self.extension_string)
        output_videos[output_filename] = {'start_t':begin, "end_t": None, "duration": pts[-1]-begin, "gap_duration": None}

        log_action("Video complete")
        return output_videos

    def get_base_filename(self, filepath):
        return os.path.splitext(os.path.basename(filepath))[0]
