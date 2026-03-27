from video_renderer import check_ffmpeg
if check_ffmpeg():
    print("FFmpeg check PASSED")
else:
    print("FFmpeg check FAILED")
