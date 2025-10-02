import os

def sec_to_timecode(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"

def timecode_to_sec(time_str: str) -> float:
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def create_filename(base_name: str, addition: int, extension_string: str) -> str:
    return base_name + "_" + str(addition) + extension_string

def get_base_filename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]