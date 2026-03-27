import ffmpeg
import os
import shutil

def check_ffmpeg():
    """Checks if ffmpeg is available."""
    if shutil.which("ffmpeg"):
        return True
    
    winget_path = r"C:\Users\Dhile\AppData\Local\Microsoft\WinGet\Links"
    if os.path.exists(os.path.join(winget_path, "ffmpeg.exe")):
        os.environ["PATH"] += os.pathsep + winget_path
        return True
    
    return False

def get_audio_duration(audio_path: str) -> float:
    """Probes audio file to get its duration in seconds."""
    probe = ffmpeg.probe(audio_path)
    return float(probe['format']['duration'])

def render_final_video(images: list, audio_path: str, output_path: str, scene_durations: list, bgm_path: str = None, srt_path: str = None):
    """
    Stitches images together with specific durations, mixes audio, and burns subtitles.
    """
    if len(images) != len(scene_durations):
        raise ValueError("Number of images must match number of scene durations.")

    # Get master duration
    master_dur = get_audio_duration(audio_path)

    # 1. Create Video Stream
    input_list = []
    for img, dur in zip(images, scene_durations):
        input_list.append(ffmpeg.input(img, loop=1, t=dur).filter('scale', 1080, 1920).filter('setsar', 1))

    video_stream = ffmpeg.concat(*input_list, v=1, a=0)

    # 2. Apply Subtitles if provided
    if srt_path and os.path.exists(srt_path):
        # Using relative path to avoid complex Windows escaping
        rel_srt_path = os.path.relpath(srt_path).replace('\\', '/')
        
        video_stream = video_stream.filter('subtitles', rel_srt_path, force_style='Alignment=2,FontSize=28,PrimaryColour=&H00000000,BackColour=&H80FFFFFF,OutlineColour=&H80FFFFFF,BorderStyle=3,Outline=1,Shadow=0,MarginV=30')

    # 3. Process Narration Audio
    narration = ffmpeg.input(audio_path)

    # 3. Process BGM if provided
    if bgm_path and os.path.exists(bgm_path):
        # Loop the BGM and trim to master duration
        # We use stream_loop -1 for infinite loop, then trim to duration
        bgm = ffmpeg.input(bgm_path, stream_loop=-1).filter('atrim', duration=master_dur)
        # Apply volume reduction to BGM (e.g., 15% volume)
        bgm = bgm.filter('volume', 0.15)
        
        # Mix Narration and BGM
        # amix: inputs=2, duration=first (keeps master duration)
        final_audio = ffmpeg.filter([narration, bgm], 'amix', inputs=2, duration='first')
    else:
        final_audio = narration

    try:
        (
            ffmpeg
            .output(video_stream, final_audio, output_path,
                    vcodec='libx264', acodec='aac', pix_fmt='yuv420p',
                    shortest=None, t=master_dur)
            .overwrite_output()
            .run(quiet=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        return False
