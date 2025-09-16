from General import log_action, sec_to_timecode, create_filename
import ffmpeg


def process_video(input_filepath, begin, end, output_filename):
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
                preset=preset_mode,
                crf=crf_value,
                acodec="aac",
                af="aresample=async=1000",
                # avoid_negative_ts="make_zero",
                # reset_timestamps=1
            )
            .global_args('-loglevel', 'info')  # Adjust loglevel as needed 
            .run(overwrite_output=False, capture_stdout=True, capture_stderr=True)
        )
        return process
    

def split_videos(input_filepath, cuts, base_name, extansion_string):
    print(f"-- {len(cuts)} cut points found, will generate {len(cuts) + 1} video(s).")

    begin = None
    end = None
    addition = 1
    for frame, start_t, end_t, duration in cuts:
        #first video
        if begin == None and end == None:
            print(f"First video starting: end {sec_to_timecode(start_t)}")
        
            output_filename = create_filename(base_name, addition, extension_string)
            process_video(input_filepath, None, start_t, output_filename)
        
            print("Video complete")
            begin = end_t
            addition += 1

            continue

        end = start_t
        print(f"Next video starting: begin {sec_to_timecode(begin)}, end {sec_to_timecode(end)}")
        
        output_filename = create_filename(base_name, addition, extension_string)
        process_video(input_filepath, begin, end, output_filename)
        
        print("Video complete")
        begin = end_t
        addition += 1

    #last video
    print(f"Last or only video starting: begin {sec_to_timecode(begin) if begin != None else sec_to_timecode(0.0)}")
    
    output_filename = create_filename(base_name, addition, extension_string)
    process_video(input_filepath, begin, None, output_filename)
    
    print("Video complete")