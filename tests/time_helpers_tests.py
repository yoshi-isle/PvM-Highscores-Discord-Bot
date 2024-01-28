import asyncio
import pytest
import datetime
import src.hall_of_fame.time_helpers as time_helpers

pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pb, expected",
    [
        ("0:00.0", time_helpers.TimeInput.INPUT_AS_MINUTES_ONLY),
        ("47", time_helpers.TimeInput.BAD_INPUT),
        # ("0:00.6", datetime.time(hour=0, minute=0, second=0, microsecond=6000)),
        # ("0:05.0", datetime.time(hour=0, minute=0, second=5, microsecond=0000)),
        # ("0:05.6", datetime.time(hour=0, minute=0, second=5, microsecond=6000)),
        # ("0:12.0", datetime.time(hour=0, minute=0, second=12, microsecond=0000)),
        # ("0:12.6", datetime.time(hour=0, minute=0, second=12, microsecond=6000)),
        # ("0:47.4", datetime.time(hour=0, minute=0, second=47, microsecond=4000)),
        # ("0:59.4", datetime.time(hour=0, minute=0, second=59, microsecond=4000)),
        # ("1:00.0", datetime.time(hour=0, minute=1, second=0, microsecond=0000)),
        # ("1:01.2", datetime.time(hour=0, minute=1, second=1, microsecond=2000)),
        # ("1:22.2", datetime.time(hour=0, minute=1, second=22, microsecond=2000)),
        # ("1:40.2", datetime.time(hour=0, minute=1, second=40, microsecond=2000)),
        # ("5:48.6", datetime.time(hour=0, minute=5, second=48, microsecond=6000)),
        # ("12:58.8", datetime.time(hour=0, minute=12, second=58, microsecond=8000)),
        # ("20:00.0", datetime.time(hour=0, minute=20, second=0, microsecond=0000)),
        # ("30:20.0", datetime.time(hour=0, minute=30, second=20, microsecond=0000)),
        # ("60:00.0", datetime.time(hour=1, minute=0, second=0, microsecond=0000)),
        # ("61:00.0", datetime.time(hour=1, minute=1, second=0, microsecond=0000)),
        # ("132:34.4", datetime.time(hour=2, minute=12, second=34, microsecond=4000)),
        # ("180:00.2", datetime.time(hour=3, minute=0, second=0, microsecond=2000)),
        # ("760:40.4", datetime.time(hour=12, minute=40, second=40, microsecond=4000)),
    ],
)
async def test_validate_time_format(pb, expected):
    actual = await time_helpers.validate_time_format(pb)
    assert actual == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pb, expected",
    [
        (datetime.time(hour=0, minute=0, second=0, microsecond=0), "0:00.0"),
        (datetime.time(hour=0, minute=0, second=0, microsecond=6000), "0:00.6"),
        (datetime.time(hour=0, minute=0, second=5, microsecond=0000), "0:05.0"),
        (datetime.time(hour=0, minute=0, second=5, microsecond=6000), "0:05.6"),
        (datetime.time(hour=0, minute=0, second=12, microsecond=0000), "0:12.0"),
        (datetime.time(hour=0, minute=0, second=12, microsecond=6000), "0:12.6"),
        (datetime.time(hour=0, minute=0, second=47, microsecond=4000), "0:47.4"),
        (datetime.time(hour=0, minute=0, second=59, microsecond=4000), "0:59.4"),
        (datetime.time(hour=0, minute=1, second=0, microsecond=0000), "1:00.0"),
        (datetime.time(hour=0, minute=1, second=1, microsecond=2000), "1:01.2"),
        (datetime.time(hour=0, minute=1, second=22, microsecond=2000), "1:22.2"),
        (datetime.time(hour=0, minute=1, second=40, microsecond=2000), "1:40.2"),
        (datetime.time(hour=0, minute=5, second=48, microsecond=6000), "5:48.6"),
        (datetime.time(hour=0, minute=12, second=58, microsecond=8000), "12:58.8"),
        (datetime.time(hour=0, minute=20, second=0, microsecond=0000), "20:00.0"),
        (datetime.time(hour=0, minute=30, second=20, microsecond=0000), "30:20.0"),
        (datetime.time(hour=1, minute=0, second=0, microsecond=0000), "60:00.0"),
        (datetime.time(hour=1, minute=1, second=0, microsecond=0000), "61:00.0"),
        (datetime.time(hour=2, minute=12, second=34, microsecond=4000), "132:34.4"),
        (datetime.time(hour=3, minute=0, second=0, microsecond=2000), "180:00.2"),
        (datetime.time(hour=12, minute=40, second=40, microsecond=4000), "760:40.4"),
    ],
)
async def test_convert_pb_to_display_format(pb, expected):
    actual = await time_helpers.convert_pb_to_display_format(pb)
    assert actual == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pb, expected",
    [
        ("0:00.0", datetime.time(hour=0, minute=0, second=0, microsecond=0)),
        ("0:00.6", datetime.time(hour=0, minute=0, second=0, microsecond=6000)),
        ("0:05.0", datetime.time(hour=0, minute=0, second=5, microsecond=0000)),
        ("0:05.6", datetime.time(hour=0, minute=0, second=5, microsecond=6000)),
        ("0:12.0", datetime.time(hour=0, minute=0, second=12, microsecond=0000)),
        ("0:12.6", datetime.time(hour=0, minute=0, second=12, microsecond=6000)),
        ("0:47.4", datetime.time(hour=0, minute=0, second=47, microsecond=4000)),
        ("0:59.4", datetime.time(hour=0, minute=0, second=59, microsecond=4000)),
        ("1:00.0", datetime.time(hour=0, minute=1, second=0, microsecond=0000)),
        ("1:01.2", datetime.time(hour=0, minute=1, second=1, microsecond=2000)),
        ("1:22.2", datetime.time(hour=0, minute=1, second=22, microsecond=2000)),
        ("1:40.2", datetime.time(hour=0, minute=1, second=40, microsecond=2000)),
        ("5:48.6", datetime.time(hour=0, minute=5, second=48, microsecond=6000)),
        ("12:58.8", datetime.time(hour=0, minute=12, second=58, microsecond=8000)),
        ("20:00.0", datetime.time(hour=0, minute=20, second=0, microsecond=0000)),
        ("30:20.0", datetime.time(hour=0, minute=30, second=20, microsecond=0000)),
        ("60:00.0", datetime.time(hour=1, minute=0, second=0, microsecond=0000)),
        ("61:00.0", datetime.time(hour=1, minute=1, second=0, microsecond=0000)),
        ("132:34.4", datetime.time(hour=2, minute=12, second=34, microsecond=4000)),
        ("180:00.2", datetime.time(hour=3, minute=0, second=0, microsecond=2000)),
        ("760:40.4", datetime.time(hour=12, minute=40, second=40, microsecond=4000)),
    ],
)
async def test_convert_pb_to_time(pb, expected):
    actual = await time_helpers.convert_pb_to_time(
        time_helpers.TimeInput.INPUT_AS_MINUTES_ONLY,
        pb,
    )
    assert actual == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pb, expected",
    [
        (datetime.time(hour=0, minute=0, second=0, microsecond=0000), 0),
        (datetime.time(hour=0, minute=0, second=0, microsecond=6000), 6000),
        (datetime.time(hour=0, minute=0, second=6, microsecond=0000), 6000000),
        (datetime.time(hour=0, minute=6, second=0, microsecond=0000), 360000000),
        (datetime.time(hour=6, minute=0, second=0, microsecond=0000), 21600000000),
        (datetime.time(hour=0, minute=0, second=5, microsecond=0000), 5000000),
        (datetime.time(hour=0, minute=0, second=52, microsecond=5000), 52005000),
        (datetime.time(hour=22, minute=6, second=0, microsecond=5000), 79560005000),
        (datetime.time(hour=22, minute=23, second=52, microsecond=5000), 80632005000),
        (datetime.time(hour=23, minute=59, second=59, microsecond=59000), 86399059000),
    ],
)
async def test_convert_time_to_microseconds(pb, expected):
    actual = await time_helpers.convert_time_to_microseconds(pb)
    assert actual == expected
