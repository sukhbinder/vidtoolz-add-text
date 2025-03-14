import sys
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

POSITION_MAP = {
    "top-left": ("left", "top"),
    "top-right": ("right", "top"),
    "bottom-left": ("left", "bottom"),
    "bottom-right": ("right", "bottom"),
    "center": ("center", "center"),
    "bottom": ("center", "bottom"),
}


def add_text_to_video(input_video_path, text, start_time, end_time, position, fontsize=50):
    try:
        # Load the original video
        video = VideoFileClip(input_video_path)
    except Exception as e:
        sys.exit("Error loading video file: " + str(e))
        
    try:
        # Create a text clip using a common system font.
        txt_clip = TextClip(text, fontsize=fontsize, color='white', font='Arial')
    except Exception as e:
        sys.exit("Error creating text clip: " + str(e))
    
    # Convert position string to a tuple
    pos_tuple = POSITION_MAP.get(position, ("center", "bottom"))
    try:
        # Set duration and starting time, and position the text
        txt_clip = (txt_clip
                    .set_position(pos_tuple)
                    .set_duration(end_time - start_time)
                    .set_start(start_time))
    except Exception as e:
        sys.exit("Error setting properties on text clip: " + str(e))
    
    try:
        # Overlay the text clip on the video
        video_with_text = CompositeVideoClip([video, txt_clip])
    except Exception as e:
        sys.exit("Error combining clips: " + str(e))
    
    return video_with_text, video.fps


def write_file(video_with_text, output_video_path, fps):
    try:
        # Write the result to a file
        video_with_text.write_videofile(output_video_path, codec='libx264', fps=fps, audio_codec="aac")
    except Exception as e:
        sys.exit("Error writing video file: " + str(e))
    video_with_text.close()