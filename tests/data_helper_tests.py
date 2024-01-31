import pytest

import src.hall_of_fame.data_helper as data_helper
from src.hall_of_fame.autocompletes.autocompletes import AutoComplete


@pytest.mark.parametrize(
    "group_members, group_size, expected",
    [
        # Solo
        ("Player", 1, True),
        ("Player, Player2", 1, False),
        ("Player, Player2, Player3", 1, False),
        ("Player, Player2, Player3, Player4", 1, False),
        ("Player, Player2, Player3, Player4, Player5", 1, False),
        # Duo
        ("Player", 2, False),
        ("Player, Player2", 2, True),
        ("Player, Player2, Player3", 2, False),
        ("Player, Player2, Player3, Player4", 2, False),
        ("Player, Player2, Player3, Player4, Player5", 2, False),
        # Trio
        ("Player", 3, False),
        ("Player, Player2", 3, False),
        ("Player, Player2, Player3", 3, True),
        ("Player, Player2, Player3, Player4", 3, False),
        ("Player, Player2, Player3, Player4, Player5", 3, False),
        # 4
        ("Player", 4, False),
        ("Player, Player2", 4, False),
        ("Player, Player2, Player3", 4, False),
        ("Player, Player2, Player3, Player4", 4, True),
        ("Player, Player2, Player3, Player4, Player5", 4, False),
        # 5
        ("Player", 5, False),
        ("Player, Player2", 5, False),
        ("Player, Player2, Player3", 5, False),
        ("Player, Player2, Player3, Player4", 5, False),
        ("Player, Player2, Player3, Player4, Player5", 5, True),
        ("player1, player2", 4, False),
    ],
)
def test_is_valid_group_members_string(group_members, group_size, expected):
    actual = data_helper.is_valid_group_members_string(group_members, group_size)
    assert actual == expected


@pytest.mark.parametrize(
    "group_size, mode, expected",
    [
        (1, AutoComplete.TOB_MODES.Normal, "Theatre of Blood (Solo)"),
        (2, AutoComplete.TOB_MODES.Normal, "Theatre of Blood (Duo)"),
        (3, AutoComplete.TOB_MODES.Normal, "Theatre of Blood (Trio)"),
        (4, AutoComplete.TOB_MODES.Normal, "Theatre of Blood (4 man)"),
        (5, AutoComplete.TOB_MODES.Normal, "Theatre of Blood (5 man)"),
        (1, AutoComplete.TOB_MODES.Hard, "Theatre of Blood: Hard Mode (Solo)"),
        (2, AutoComplete.TOB_MODES.Hard, "Theatre of Blood: Hard Mode (Duo)"),
        (3, AutoComplete.TOB_MODES.Hard, "Theatre of Blood: Hard Mode (Trio)"),
        (4, AutoComplete.TOB_MODES.Hard, "Theatre of Blood: Hard Mode (4 man)"),
        (5, AutoComplete.TOB_MODES.Hard, "Theatre of Blood: Hard Mode (5 man)"),
        (1, AutoComplete.COX_MODES.Normal, "Chambers of Xeric (Solo)"),
        (2, AutoComplete.COX_MODES.Normal, "Chambers of Xeric (Duo)"),
        (3, AutoComplete.COX_MODES.Normal, "Chambers of Xeric (Trio)"),
        (4, AutoComplete.COX_MODES.Normal, "Chambers of Xeric (4 man)"),
        (5, AutoComplete.COX_MODES.Normal, "Chambers of Xeric (5 man)"),
        (1, AutoComplete.COX_MODES.Hard, "Chambers of Xeric: Challenge Mode (Solo)"),
        (2, AutoComplete.COX_MODES.Hard, "Chambers of Xeric: Challenge Mode (Duo)"),
        (3, AutoComplete.COX_MODES.Hard, "Chambers of Xeric: Challenge Mode (Trio)"),
        (4, AutoComplete.COX_MODES.Hard, "Chambers of Xeric: Challenge Mode (4 man)"),
        (5, AutoComplete.COX_MODES.Hard, "Chambers of Xeric: Challenge Mode (5 man)"),
        (1, AutoComplete.TOA_MODES.Normal, "Tombs of Amascut: Normal Mode (Solo)"),
        (2, AutoComplete.TOA_MODES.Normal, "Tombs of Amascut: Normal Mode (Duo)"),
        (3, AutoComplete.TOA_MODES.Normal, "Tombs of Amascut: Normal Mode (Trio)"),
        (4, AutoComplete.TOA_MODES.Normal, "Tombs of Amascut: Normal Mode (4 man)"),
        (5, AutoComplete.TOA_MODES.Normal, "Tombs of Amascut: Normal Mode (5 man)"),
        (1, AutoComplete.TOA_MODES.Hard, "Tombs of Amascut: Expert Mode (Solo)"),
        (2, AutoComplete.TOA_MODES.Hard, "Tombs of Amascut: Expert Mode (Duo)"),
        (3, AutoComplete.TOA_MODES.Hard, "Tombs of Amascut: Expert Mode (Trio)"),
        (4, AutoComplete.TOA_MODES.Hard, "Tombs of Amascut: Expert Mode (4 man)"),
        (5, AutoComplete.TOA_MODES.Hard, "Tombs of Amascut: Expert Mode (5 man)"),
    ],
)
def test_get_tob_raid_name(group_size, mode, expected):
    actual = data_helper.get_tob_raid_name(group_size, mode)
    assert actual == expected
