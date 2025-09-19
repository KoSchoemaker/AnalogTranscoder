from General import *
import ffmpeg


class Process:
    def __init__(self, crf_value: int, preset_mode: str):
        self.crf_value = crf_value
        self.preset_mode = preset_mode

    def process_video(self, input_filepath: str, output_filename: str, begin=None, end=None, dry_run=False):
        kwargs = {}
        if begin is not None:
            kwargs['ss'] = begin
        if end is not None:
            kwargs['to'] = end

        if dry_run == False:
            process = (
                ffmpeg
                .input(input_filepath, **kwargs)
                .output(
                    output_filename,
                    vf='yadif,crop=iw-40:ih-32,scale=960:720',
                    vcodec='libx264',
                    preset=self.preset_mode,
                    crf=self.crf_value,
                    acodec="aac",
                    af="aresample=async=1000",
                    # avoid_negative_ts="make_zero",
                    # reset_timestamps=1
                )
                .global_args('-loglevel', 'info')  # Adjust loglevel as needed
                .run(overwrite_output=False, capture_stdout=True, capture_stderr=True)
            )
            return process

    def split_videos(self, input_filepath, cuts, base_name, extension_string):
        log_action(
            f"-- {len(cuts)} cut points found, will generate {len(cuts) + 1} video(s).")

        begin = None
        end = None
        addition = 1
        for frame, start_t, end_t, duration in cuts:
            # first video
            if begin == None and end == None:
                log_action(
                    f"First video starting: end {sec_to_timecode(start_t)}")

                output_filename = create_filename(
                    base_name, addition, extension_string)
                self.process_video(input_filepath, None,
                                   start_t, output_filename)

                log_action("Video complete")
                begin = end_t
                addition += 1

                continue

            end = start_t
            log_action(
                f"Next video starting: begin {sec_to_timecode(begin)}, end {sec_to_timecode(end)}")

            output_filename = create_filename(
                base_name, addition, extension_string)
            self.process_video(input_filepath, begin, end, output_filename)

            log_action("Video complete")
            begin = end_t
            addition += 1

        # last video
        log_action(
            f"Last or only video starting: begin {sec_to_timecode(begin) if begin != None else sec_to_timecode(0.0)}")

        output_filename = create_filename(
            base_name, addition, extension_string)
        self.process_video(input_filepath, begin, None, output_filename)

        log_action("Video complete")
