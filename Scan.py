from General import *

import os
import subprocess
import json

def get_external_cache_filepath(cache_directory, filename) -> str:
    return os.path.join(cache_directory, filename) + '.json'

def get_pts_from_external_cache(cache_directory, filename):
    cache_filepath = get_external_cache_filepath(cache_directory, filename)

    if os.path.isfile(cache_filepath):
        log_action(f'INFO: cache file exists for {filename}, using that')

        with open(os.path.join(cache_directory, filename) + '.json', 'r') as file:
            return json.load(file)
    
    log_action(f'INFO: no cache file exists for {filename}')
    return False

def add_pts_to_external_cache(cache_directory, filename, pts) -> bool:    
    cache_filepath = get_external_cache_filepath(cache_directory, filename)
    if os.path.isfile(cache_filepath):
        log_action(f'INFO: cache file already exists for {filename}, overwriting')
    with open(cache_filepath, 'w') as file:
        json.dump(pts, file)

def get_packet_pts(filename, cache_directory):

    cache_pts = get_pts_from_external_cache(cache_directory, filename)
    if cache_pts:
        return cache_pts

    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a:0",
        "-show_packets", "-of", "json", filename
    ]
    out = subprocess.check_output(cmd, text=True)
    info = json.loads(out)
    pts = []
    for p in info.get("packets", []):
        if "pts_time" in p:
            pts.append(float(p["pts_time"]))
            
    add_pts_to_external_cache(cache_directory, filename, pts)
    return pts

def find_discontinuities(pts_list, gap_threshold=0.2):
    # returns indices where a gap or negative jump occurs
    cuts = []
    prev = None
    for i, t in enumerate(pts_list):
        if prev is None:
            prev = t; continue
        diff = t - prev
        if diff < -0.001 or diff > gap_threshold:  # negative = reset, large = gap
            cuts.append((i, prev, t, diff))
        prev = t
    return cuts