import vidtoolz
import os
from vidtoolz_add_text.add_text import add_text_to_video, write_file


def determine_output_path(input_file, output_file):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_text.mp4")


def create_parser(subparser):
    parser = subparser.add_parser("addtext", description="Add text to a video file")
    parser.add_argument("main_video", help="Path to the main video file.")
    parser.add_argument("text", help="Text to write")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output video file name (default: output.mp4)",
    )
    parser.add_argument(
        "-p",
        "--position",
        choices=[
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "center",
            "bottom",
        ],
        default="bottom",
        help="Position of the text (default: bottom)",
    )
    parser.add_argument(
        "-st",
        "--start-time",
        type=float,
        default=2,
        help="Start time when text should appear",
    )
    parser.add_argument(
        "-et",
        "--end-time",
        type=float,
        default=4,
        help="End time when text should disappear",
    )
    parser.add_argument(
        "-f", "--fontsize", type=int, default=50, help="Fontsize default:50"
    )

    return parser


class ViztoolzPlugin:
    """Add text to a video file"""

    __name__ = "addtext"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):

        output = determine_output_path(args.main_video, args.output)
        clip, fps = add_text_to_video(
            args.main_video,
            args.text,
            args.start_time,
            args.end_time,
            args.position,
            args.fontsize,
        )
        write_file(clip, output, fps)

    def hello(self, args):
        # this routine will be called when "vidtoolz "addtext is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


addtext_plugin = ViztoolzPlugin()
