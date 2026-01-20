import sys, os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, vfx
from pathlib import Path
from moviepy.tools import convert_to_seconds

import subprocess
import shlex

POSITION_MAP = {
    "top-left": ("left", "top"),
    "top-right": ("right", "top"),
    "bottom-left": ("left", "bottom"),
    "bottom-right": ("right", "bottom"),
    "center": ("center", "center"),
    "bottom": ("center", "bottom"),
}


def parse_multitext_args(multitext_list):
    parsed = []
    for item in multitext_list:
        try:
            text, start, duration = item.split(",", 2)
            parsed.append((text.strip(), convert_to_seconds(start), float(duration)))
        except ValueError:
            sys.exit(
                f"Error: Invalid multi-text format: '{item}'. Use -mt \"text,start,duration\""
            )
    return parsed


def make_text_clip(
    text,
    start_time,
    duration,
    font=None,
    fontsize=50,
    padding=50,
    pos_tuple=("center", "bottom"),
    textcolor="white",
):

    if font is None:
        here = os.path.dirname(__file__)
        font = os.path.join(here, "fonts", "SEASRN.ttf")

    try:
        txt_clip = TextClip(
            font=font,
            text=text,
            font_size=fontsize,
            stroke_width=2,
            stroke_color="black",
            color=textcolor,
            margin=(padding, padding),
        )
    except Exception as e:
        sys.exit("Error creating text clip: " + str(e))

    try:
        # Set duration and starting time, and position the text
        txt_clip = (
            txt_clip.with_position(pos_tuple)
            .with_duration(duration)
            .with_start(start_time)
        )
    except Exception as e:
        sys.exit("Error setting properties on text clip: " + str(e))

    txt_clip = txt_clip.with_effects([vfx.CrossFadeIn(0.5), vfx.CrossFadeOut(0.5)])
    return txt_clip


def add_text_to_video(
    input_video_path,
    text,
    start_time,
    end_time,
    position,
    fontsize=50,
    padding=50,
    duration=4,
    multitexts=None,
):
    if end_time is None:
        end_time = start_time + duration
    # Input Validation
    if not Path(input_video_path).exists():
        sys.exit(f"Error: Video file not found: {input_video_path}")
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

    clips = [video]
    # Convert position string to a tuple
    pos_tuple = POSITION_MAP.get(position, ("center", "bottom"))

    if text:
        txt_clip = make_text_clip(
            text,
            start_time,
            end_time - start_time,
            fontsize=fontsize,
            padding=padding,
            pos_tuple=pos_tuple,
        )
        clips.append(txt_clip)

    if multitexts:
        for mtext, mstart, mduration in parse_multitext_args(multitexts):
            txt_clip = make_text_clip(
                mtext, mstart, mduration, fontsize=fontsize, padding=padding, pos_tuple=pos_tuple
            )
            clips.append(txt_clip)

    try:
        # Overlay the text clip on the video
        video_with_text = CompositeVideoClip(clips)
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




POSITION_MAP_FFMPEG = {
    "top-left": ("10", "10"),
    "top-right": ("w-text_w-10", "10"),
    "bottom-left": ("10", "h-text_h-10"),
    "bottom-right": ("w-text_w-10", "h-text_h-10"),
    "center": ("(w-text_w)/2", "(h-text_h)/2"),
    "bottom": ("(w-text_w)/2", "h-text_h-50"),
}


def _alpha_expr(start, duration, fade=0.5):
    end = start + duration
    return (
        f"if(lt(t,{start}),0,"
        f" if(lt(t,{start+fade}),(t-{start})/{fade},"
        f"  if(lt(t,{end-fade}),1,"
        f"   if(lt(t,{end}),({end}-t)/{fade},0))))"
    )


def _drawtext(
    text,
    start,
    duration,
    font,
    fontsize,
    padding,
    pos,
    textcolor,
    stroke_width,
):
    x, y = POSITION_MAP_FFMPEG[pos]
    alpha = _alpha_expr(start, duration)

    return (
        "drawtext="
        f"text='{text}':"
        f"fontfile='{font}':"
        f"fontsize={fontsize}:"
        f"fontcolor={textcolor}:"
        f"borderw={stroke_width}:"
        f"bordercolor=black:"
        f"x={x}:y={y}:"
        f"alpha='{alpha}'"
    )


def add_text_to_video_ffmpeg(
    input_video_path,
    output_video_path,
    text,
    start_time,
    end_time=None,
    position="bottom",
    fontsize=50,
    padding=50,
    duration=4,
    multitexts=None,
    sticker_text=False,
    stroke_width=None,
    font=None,
    textcolor="white",
):
    """
    FFmpeg replacement for MoviePy add_text_to_video()
    """

    input_video_path = Path(input_video_path)
    if not input_video_path.exists():
        raise FileNotFoundError(input_video_path)

    if end_time is None:
        end_time = start_time + duration

    if font is None:
        font = Path(__file__).parent / "fonts" / "SEASRN.ttf"

    if stroke_width is None:
        stroke_width = 10 if sticker_text else 2

    filters = []

    # main text
    if text:
        filters.append(
            _drawtext(
                text=text,
                start=start_time,
                duration=end_time - start_time,
                font=font,
                fontsize=fontsize,
                padding=padding,
                pos=position,
                textcolor=textcolor,
                stroke_width=stroke_width,
            )
        )

    # multitext
    if multitexts:
        for item in multitexts:
            txt, start, dur = item.split(",", 2)
            start = convert_to_seconds(start)
            dur = float(dur)

            filters.append(
                _drawtext(
                    text=txt.strip(),
                    start=start,
                    duration=dur,
                    font=font,
                    fontsize=fontsize,
                    padding=padding,
                    pos=position,
                    textcolor=textcolor,
                    stroke_width=stroke_width,
                )
            )

    vf = ",".join(filters)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video_path),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-c:a",
        "copy",
        str(output_video_path),
    ]

    subprocess.run(cmd, check=True)
