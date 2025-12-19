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

def render_final_video(images: list, audio_path: str, output_path: str, scene_durations: list):
    """
    Stitches images together with specific durations and combines with a master audio track.
    
    images: list of image file paths
    audio_path: master audio file path
    output_path: final video file path
    scene_durations: list of durations (float) for each image corresponding to input 'images' list
    """
    
    # Check if we have matching lengths
    if len(images) != len(scene_durations):
        raise ValueError("Number of images must match number of scene durations.")

    # Create individual video segments and concatenate them
    # We'll use the 'concat' filter since we are applying different durations
    input_list = []
    for img, dur in zip(images, scene_durations):
        # Input image, loop for duration 'dur' at 25 fps
        input_list.append(ffmpeg.input(img, loop=1, t=dur).filter('scale', 1080, 1920).filter('setsar', 1))

    # Concatenate visual segments
    joined = ffmpeg.concat(*input_list, v=1, a=0).node
    
    # Combined with master audio
    audio_input = ffmpeg.input(audio_path)
    
    try:
        (
            ffmpeg
            .output(joined[0], audio_input, output_path,
                    vcodec='libx264', acodec='aac', pix_fmt='yuv420p',
                    shortest=None)
            .overwrite_output()
            .run(quiet=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        return False
