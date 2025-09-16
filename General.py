def sec_to_timecode(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"

def log_action(text: str):
    print(text)

def create_filename(base_name: str, addition: int, extension_string: str) -> str:
    return base_name + "_" + str(addition) + extension_string