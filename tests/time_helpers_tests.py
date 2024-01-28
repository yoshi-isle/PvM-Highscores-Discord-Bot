import asyncio
import pytest
import datetime
import src.hall_of_fame.time_helpers as time_helpers

pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pb, expected",
    [
        # Small (second) times
        (datetime.time(hour=0, minute=0, second=0, microsecond=6), "0:00.6"),
        (datetime.time(hour=0, minute=0, second=5, microsecond=0), "0:05.0"),
        (datetime.time(hour=0, minute=0, second=5, microsecond=6), "0:05.6"),
        (datetime.time(hour=0, minute=0, second=12, microsecond=0), "0:12.0"),
        (datetime.time(hour=0, minute=0, second=12, microsecond=6), "0:12.6"),
        (datetime.time(hour=0, minute=0, second=47, microsecond=4), "0:47.4"),
        (datetime.time(hour=0, minute=0, second=59, microsecond=4), "0:59.4"),
        # Meidum (minute) times
        (datetime.time(hour=0, minute=1, second=0, microsecond=0), "1:00.0"),
        (datetime.time(hour=0, minute=1, second=1, microsecond=2), "1:01.2"),
        (datetime.time(hour=0, minute=1, second=22, microsecond=2), "1:22.2"),
        (datetime.time(hour=0, minute=1, second=40, microsecond=2), "1:40.2"),
        (datetime.time(hour=0, minute=5, second=48, microsecond=6), "5:48.6"),
        (datetime.time(hour=0, minute=12, second=58, microsecond=8), "12:58.8"),
        (datetime.time(hour=0, minute=20, second=0, microsecond=0), "20:00.0"),
        (datetime.time(hour=0, minute=30, second=20, microsecond=0), "30:20.0"),
        # Large (hour) times
        (datetime.time(hour=1, minute=0, second=0, microsecond=0), "60:00.0"),
        (datetime.time(hour=1, minute=1, second=0, microsecond=0), "61:00.0"),
        (datetime.time(hour=2, minute=12, second=34, microsecond=4), "132:34.4"),
        (datetime.time(hour=3, minute=0, second=0, microsecond=2), "180:00.2"),
        (datetime.time(hour=12, minute=40, second=40, microsecond=40), "760:40.4"),
    ],
)
async def test_convert_pb_to_display_format(pb, expected):
    actual = await time_helpers.convert_pb_to_display_format(pb)
    assert actual == expected
