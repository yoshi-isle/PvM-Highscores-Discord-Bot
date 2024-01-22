import re
from constants.timezone import Eastern_Standard_Timezone
from datetime import time


async def validate_time_format(time_string) -> int:
    """
    Checks if a string is in the format 00:00.00 (optional third group of period and zeros)

    Args:
    time_string: The string to validate

    Returns:
    True if the string is valid, False otherwise
    """
    minutes_only_pattern = re.compile(r"^([0-9]{1,2}):([0-5][0-9])(?:\.([0-9]{0,2}))?$")
    hours_pattern = re.compile(
        r"^([0-9]):([0-5][0-9]):([0-5][0-9])(?:\.([0-9]{0,2}))?$"
    )
    if minutes_only_pattern.match(time_string):
        return 1
    elif hours_pattern.match(time_string):
        return 2
    else:
        return 0


async def convert_pb_to_time(case: int, time_string: str) -> time:
    """
    Converts a string to a datetime.time object
    Assumes the string has been validated to the format 00:00.00

    Args:
    time_string: The string to convert

    Returns:
    Time object
    """

    hours = 0
    seconds = 0
    milliseconds = 0
    hours_string = ""
    minutes_string = ""
    seconds_string = ""
    milliseconds_string = ""

    if case == 2:
        (
            hours_string,
            minutes_string,
            seconds_and_milliseconds_string,
        ) = time_string.split(":")
        hours = int(hours_string)
    elif case == 1:
        minutes_string, seconds_and_milliseconds_string = time_string.split(":")

    minutes = int(minutes_string)
    if "." in seconds_and_milliseconds_string:
        seconds_string, milliseconds_string = seconds_and_milliseconds_string.split(".")
        seconds = int(seconds_string)
        milliseconds = int(milliseconds_string)
    else:
        seconds = int(seconds_and_milliseconds_string)

    if minutes > 59:
        hours = minutes // 60
        minutes = minutes % 60
    return time(
        hours, minutes, seconds, milliseconds * 1000, tzinfo=None
    )

async def convert_pb_to_display_format(pb:time)->str:
    return f"{pb.minute}:{pb.second}.{str(pb.microseconds).rstrip('0')}"