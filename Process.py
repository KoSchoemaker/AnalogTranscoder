from General import *
from Settings import Settings
from Progress import Progress
from Command import Command
import os
import time


class Process:
    def __init__(self, settings: Settings, progress: Progress):
        self.settings = settings
        self.progress = progress

    # Takes output_file_dict <dict> {input_path:{output_filename_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def run_batch(self, output_file_dict):
        output_directory = self.settings.get_output_dir()
        for input_path, item in output_file_dict.items():
            for output_filename, details in item.items():
                output_filepath = os.path.join(
                    output_directory, output_filename)
                if os.path.isfile(output_filepath):
                    print(f'INFO: {output_filepath} already exists, skipping')
                    continue
                self.progress.duration = details['duration']
                self.__process_video(input_path, output_filepath,
                                     details["start_t"], details["end_t"])
                self.progress.flush_progress()

    def __process_video(self, input_filepath: str, output_filepath: str, begin=None, end=None):
        if self.settings.get_dry_run() is False:
            start = time.time()
            print(
                f"INFO: Processing video {input_filepath}: {output_filepath} | {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))}")

            full_cmd = self.__build_command(
                input_filepath, output_filepath, begin, end)

            process = Command.run(full_cmd)
            for line in process.stdout:
                self.progress.parse_process_progress(line)

            end = time.time()
            print(
                f"INFO: Processing success | {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end))}, took {(end - start)/60} min")

    def __build_command(self, input_filepath: str, output_filepath: str, begin, end):
        cmd = [
            "ffmpeg",
        ]
        input_cmd = [
            "-i", input_filepath,
        ]
        output_cmd = [
            "-vf", "yadif,crop=iw-40:ih-32,scale=960:720",
            "-vcodec", "libx264",
            "-preset", self.settings.get_preset_mode(),
            "-crf", str(self.settings.get_crf()),
            "-acodec", "aac",
            "-af", "aresample=async=1000",
            "-loglevel", "info",
            output_filepath,
        ]

        if begin is not None:
            input_cmd.extend(['-ss', str(begin)])
        if end is not None:
            input_cmd.extend(['-to', str(end)])

        return cmd + input_cmd + output_cmd
