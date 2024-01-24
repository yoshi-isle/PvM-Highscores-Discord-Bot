import re
from datetime import time
from enum import Enum


class TimeInput(Enum):
    BAD_INPUT = 0
    INPUT_AS_MINUTES_ONLY = 1
    INPUT_WITH_HOURS = 2


async def validate_time_format(time_string) -> int:
    """
    Checks if a string is in the format 00:00.00 (optional third group of period and zeros)

    Args:
    time_string: The string to validate

    Returns:

    0 for a bad input.

    1 for an input with only minutes.

    2 for an input with hours.
    """
    minutes_only_pattern = re.compile(r"^([0-9]{1,2}):([0-5][0-9])(?:\.([0-9]{0,2}))?$")
    hours_pattern = re.compile(
        r"^([0-9]):([0-5][0-9]):([0-5][0-9])(?:\.([0-9]{0,2}))?$"
    )
    if minutes_only_pattern.match(time_string):
        return TimeInput.INPUT_AS_MINUTES_ONLY
    elif hours_pattern.match(time_string):
        return TimeInput.INPUT_WITH_HOURS
    else:
        return TimeInput.BAD_INPUT


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

    if case == TimeInput.INPUT_WITH_HOURS:
        (
            hours_string,
            minutes_string,
            seconds_and_milliseconds_string,
        ) = time_string.split(":")
        hours = int(hours_string)
    elif case == TimeInput.INPUT_AS_MINUTES_ONLY:
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
    return time(hours, minutes, seconds, milliseconds * 1000)


async def convert_pb_to_display_format(pb: time) -> str:
    """
    Take a pb time object and return a string in 00:00.00 format
    Args:
    pb: a time object that represents the pb
    Returns:
    str
    """

    minutes = int(pb.minute)

    # check if record is longer than a hour, if so convert and add the hours to minutes
    if pb.hour > 0:
        minutes += int(pb.hour) * 60
    return f"{minutes}:{pb.second}.{str(pb.microsecond)[0]}"


async def convert_time_to_microseconds(time: time) -> float:
    return (
        time.hour * 3600000000
        + time.minute * 60000000
        + time.second * 1000000
        + time.microsecond
    )
