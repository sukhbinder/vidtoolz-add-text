import sys, os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, vfx
from pathlib import Path

POSITION_MAP = {
    "top-left": ("left", "top"),
    "top-right": ("right", "top"),
    "bottom-left": ("left", "bottom"),
    "bottom-right": ("right", "bottom"),
    "center": ("center", "center"),
    "bottom": ("center", "bottom"),
}


def add_text_to_video(
    input_video_path,
    text,
    start_time,
    end_time,
    position,
    fontsize=50,
    padding=50,
    duration=4,
):
    if end_time is None:
        end_time = start_time + duration
    # Input Validation
    if not Path(input_video_path).exists():
        sys.exit(f"Error: Video file not found: {input_video_path}")
    if not text:
        sys.exit("Error: Text cannot be empty.")
    if start_time < 0 or end_time < 0 or end_time <= start_time:
        sys.exit("Error: Invalid start or end time.")
    if fontsize <= 0:
        sys.exit("Error: Font size must be positive")
    if not position in POSITION_MAP:
        sys.exit("Error: Invalid position specified.")

    try:
        video = VideoFileClip(input_video_path)
    except Exception as e:
        sys.exit(f"Error loading video file: {e}")

    try:
        here = os.path.dirname(__file__)
        font = os.path.join(here, "fonts", "SEASRN.ttf")
        # Create a text clip using a common system font.
        txt_clip = TextClip(
            font=font,
            text=text,
            font_size=fontsize,
            # bg_color=color,
            # size=(wid + 5, text_hight + 10),
            # method="caption",
            stroke_width=2,
            stroke_color="black",
            color="white",
            margin=(padding, padding),
        )
    except Exception as e:
        sys.exit("Error creating text clip: " + str(e))

    # Convert position string to a tuple
    pos_tuple = POSITION_MAP.get(position, ("center", "bottom"))
    try:
        # Set duration and starting time, and position the text
        txt_clip = (
            txt_clip.with_position(pos_tuple)
            .with_duration(end_time - start_time)
            .with_start(start_time)
        )
    except Exception as e:
        sys.exit("Error setting properties on text clip: " + str(e))

    txt_clip = txt_clip.with_effects([vfx.CrossFadeIn(0.5), vfx.CrossFadeOut(0.5)])

    try:
        # Overlay the text clip on the video
        video_with_text = CompositeVideoClip([video, txt_clip])
    except Exception as e:
        sys.exit("Error combining clips: " + str(e))

    return video_with_text, video.fps


def write_file(video_with_text, output_video_path, fps):
    try:
        # Write the result to a file
        video_with_text.write_videofile(
            output_video_path,
            codec="libx264",
            fps=fps,
            audio_codec="aac",
            temp_audiofile="temp_audio.m4a",
            remove_temp=True,
        )
    except Exception as e:
        sys.exit("Error writing video file: " + str(e))
    video_with_text.close()
