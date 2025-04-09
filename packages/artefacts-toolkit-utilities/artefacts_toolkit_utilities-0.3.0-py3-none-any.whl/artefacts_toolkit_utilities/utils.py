import subprocess
from .exceptions import FFMPEGNotInstalled
from operator import attrgetter


def _get_attribute_name_and_index(attribute_path):
    attribute_name, index = attribute_path.split("[", 1)
    index = int(index.rstrip("]"))
    return attribute_name, index


def _extract_attribute_data(msg, attribute_path):
    """
    Extract data from a message using a dot-notation attribute path.

    Args:
        msg: The message object to extract data from
        attribute_path: A string like 'pose.pose.position.x'
    Attributes can be nested and can also include list indexing, e.g. 'velocity[0]'
    """
    try:
        # TODO: Do we need to handle?
        # 1. Nested indices like attribute[0][1]
        # 2. Accessing object properties after indexing like velocity[0].x
        # Check if the path contains array indexing
        if "[" in attribute_path and "]" in attribute_path:
            attribute_name, index = _get_attribute_name_and_index(attribute_path)
            attribute_data_as_list = attrgetter(attribute_name)(msg)
            # Return the requested index value
            return attribute_data_as_list[index]
        else:
            return attrgetter(attribute_path)(msg)
    except (AttributeError, IndexError) as e:
        raise ValueError(
            f"Error accessing attribute '{attribute_path}': {e}. Does it exist?"
        )


def convert_to_webm(video_name):
    """Convert a video to webm format using ffmpeg and save it under same name with .webm extension"""

    # Fail fast if ffmpeg is not installed
    try:
        subprocess.run(["ffmpeg", "-version"], check=True)
    except FileNotFoundError:
        raise FFMPEGNotInstalled(
            "ffmpeg is not installed. Please install ffmpeg to convert videos to webm format."
        )

    ffmpeg = [
        "ffmpeg",
        "-i",
        video_name,
        "-c:v",
        "libvpx-vp9",
        "-crf",
        "30",
        "-b:v",
        "0",
        "-y",
        video_name.split(".")[0] + ".webm",
    ]
    subprocess.run(ffmpeg)
