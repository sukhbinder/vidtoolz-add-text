import pytest
import vidtoolz_add_text as w
from unittest.mock import patch

from argparse import ArgumentParser
from vidtoolz_add_text.add_text import add_text_to_video, write_file
import os


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(
        ["video.mp4", "-t", "hello", "-st", "3", "-et", "7", "-f", "100"]
    )
    assert result.main_video == "video.mp4"
    assert result.text == "hello"
    assert result.start_time == 3
    assert result.end_time == 7
    assert result.fontsize == 100
    assert result.position == "bottom"
    assert result.output is None
    assert result.padding == 50
    assert result.duration == 4


def test_plugin(capsys):
    w.addtext_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


HERE = os.path.dirname(__file__)
# Define a test video file path
TEST_VIDEO_FILE = os.path.join(HERE, "test_video.mp4")

# Define a temporary output video file path
TEMP_OUTPUT_VIDEO_FILE = os.path.join(HERE, "temp_output.mp4")


def test_add_text_to_video():
    # Test adding text to a video
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "center"
    )
    assert video_with_text is not None
    assert fps > 0


def test_add_text_to_video_invalid_position():
    # Test adding text to a video with an invalid position
    with pytest.raises(SystemExit):
        video_with_text, fps = add_text_to_video(
            TEST_VIDEO_FILE, "Test text", 0, 5, "invalid-position"
        )


def test_write_file():
    # Test writing the video to a file
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 2, 5, "center"
    )
    write_file(video_with_text, TEMP_OUTPUT_VIDEO_FILE, fps)
    assert os.path.exists(TEMP_OUTPUT_VIDEO_FILE)


def test_write_file_invalid_output_path():
    # Test writing the video to an invalid output path
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "center"
    )
    with pytest.raises(SystemExit):
        write_file(video_with_text, "/invalid/output/path", fps)


def test_add_text_to_video_invalid_video_file():
    # Test adding text to an invalid video file
    with pytest.raises(SystemExit):
        add_text_to_video("invalid_video_file.mp4", "Test text", 0, 5, "center")


def test_add_text_to_video_invalid_fontsize():
    # Test adding text to a video with an invalid font size
    with pytest.raises(TypeError):
        add_text_to_video(
            TEST_VIDEO_FILE, "Test text", 0, 5, "center", fontsize="invalid"
        )


def test_add_text_to_video_invalid_start_time():
    # Test adding text to a video with an invalid start time
    with pytest.raises(TypeError):
        add_text_to_video(TEST_VIDEO_FILE, "Test text", "invalid", 5, "center")


def test_add_text_to_video_invalid_end_time():
    # Test adding text to a video with an invalid end time
    with pytest.raises(TypeError):
        add_text_to_video(TEST_VIDEO_FILE, "Test text", 0, "invalid", "center")


def test_write_file_invalid_video_with_text():
    # Test writing an invalid video to a file
    with pytest.raises(SystemExit):
        write_file(None, TEMP_OUTPUT_VIDEO_FILE, 30)


def test_write_file_invalid_output_video_path():
    # Test writing a video to an invalid output path
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "center"
    )
    with pytest.raises(SystemExit):
        write_file(video_with_text, "/invalid/output/path", fps)


def test_write_file_invalid_fps():
    # Test writing a video with an invalid FPS to a file
    video_with_text, fps = add_text_to_video(
        TEST_VIDEO_FILE, "Test text", 0, 5, "center"
    )
    with pytest.raises(SystemExit):
        write_file(video_with_text, TEMP_OUTPUT_VIDEO_FILE, "invalid")


def teardown_module():
    # Remove the temporary output video file
    if os.path.exists(TEMP_OUTPUT_VIDEO_FILE):
        os.remove(TEMP_OUTPUT_VIDEO_FILE)


@pytest.mark.parametrize(
    "sticker_text, user_stroke_width, expected_stroke_width",
    [
        (False, None, 2),  # Default behavior
        (True, None, 10),  # Sticker mode default
        (False, 5, 5),  # User-defined stroke_width
        (True, 3, 3),  # Sticker mode with user-defined stroke_width
    ],
)
@patch("vidtoolz_add_text.add_text.CompositeVideoClip")
@patch("vidtoolz_add_text.add_text.TextClip")
def test_stroke_width_logic(
    mock_text_clip, mock_composite_clip, sticker_text, user_stroke_width, expected_stroke_width
):
    """Tests the logic for determining the stroke_width."""
    add_text_to_video(
        TEST_VIDEO_FILE,
        "Test text",
        start_time=0,
        end_time=5,
        position="center",
        sticker_text=sticker_text,
        stroke_width=user_stroke_width,
    )

    # Check that TextClip was called with the correct stroke_width
    _, kwargs = mock_text_clip.call_args
    assert kwargs["stroke_width"] == expected_stroke_width
