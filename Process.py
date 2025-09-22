from General import *
from Settings import Settings
import ffmpeg
import os


class Process:
    def __init__(self, settings: Settings):
        self.settings = settings

    # Takes output_file_dict <dict> {input_path:{output_filename_N:{'start_t', "end_t", "duration", "gap_duration"}...}...}
    def run_batch(self, output_file_dict):
        output_directory = self.settings.get_output_dir()
        for input_path, item in output_file_dict.items():
            for output_filename, details in item.items():
                output_filepath = os.path.join(output_directory, output_filename)
                if os.path.isfile(output_filepath):
                    print(f'{output_filepath} already exists, skipping')
                    continue
                self.process_video(input_path, output_filepath, details["start_t"], details["end_t"])

    def process_video(self, input_filepath: str, output_filepath: str, begin=None, end=None):
        kwargs = {}
        if begin is not None:
            kwargs['ss'] = begin
        if end is not None:
            kwargs['to'] = end

        if self.settings.get_dry_run() is False:
            try:
                process = (
                    ffmpeg
                    .input(input_filepath, **kwargs)
                    .output(
                        output_filepath,
                        vf='yadif,crop=iw-40:ih-32,scale=960:720',
                        vcodec='libx264',
                        preset=self.settings.get_preset_mode(),
                        crf=self.settings.get_crf(),
                        acodec="aac",
                        af="aresample=async=1000",
                        # avoid_negative_ts="make_zero",
                        # reset_timestamps=1
                    )
                    .global_args('-loglevel', 'info')  # Adjust loglevel as needed
                    .run(overwrite_output=False, capture_stdout=True, capture_stderr=True)
                )
            except ffmpeg.Error as e:
                print(f"Error converting {input_filepath} into {output_filepath}: {e}")
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
            return process

    # def split_videos(self, input_filepath, cuts, base_name, extension_string):
    #     print(
    #         f"-- {len(cuts)} cut points found, will generate {len(cuts) + 1} video(s).")

    #     begin = None
    #     end = None
    #     addition = 1
    #     for frame, start_t, end_t, duration in cuts:
    #         # first video
    #         if begin == None and end == None:
    #             print(
    #                 f"First video starting: end {sec_to_timecode(start_t)}")

    #             output_filename = create_filename(
    #                 base_name, addition, extension_string)
    #             self.process_video(input_filepath, None,
    #                                start_t, output_filename)

    #             print("Video complete")
    #             begin = end_t
    #             addition += 1

    #             continue

    #         end = start_t
    #         print(
    #             f"Next video starting: begin {sec_to_timecode(begin)}, end {sec_to_timecode(end)}")

    #         output_filename = create_filename(
    #             base_name, addition, extension_string)
    #         self.process_video(input_filepath, begin, end, output_filename)

    #         print("Video complete")
    #         begin = end_t
    #         addition += 1

    #     # last video
    #     print(
    #         f"Last or only video starting: begin {sec_to_timecode(begin) if begin != None else sec_to_timecode(0.0)}")

    #     output_filename = create_filename(
    #         base_name, addition, extension_string)
    #     self.process_video(input_filepath, begin, None, output_filename)

    #     print("Video complete")
