import operator

from constants.channels import ChannelIds
from hall_of_fame.autocompletes.autocompletes import AutoComplete


def get_fastest_times(data, boss_name):
    """
    Returns a list of personal best times for the given boss, sorted fastest to slowest.
    """
    all_pbs_for_boss = (result for result in data if result["boss"] == boss_name)
    return sorted(all_pbs_for_boss, key=operator.itemgetter("pb"))


async def is_valid_group_members_string(group_members, group_size):
    result = [group_members.strip() for x in group_members.split(",")]
    return len(result) == group_size


# TODO - reduce complexity
def valid_boss_name(boss, forum_data):
    is_valid = False
    for data in forum_data:
        if boss == data["boss_name"]:
            is_valid = True
    return is_valid


# TODO - bad
def get_highscore_channel_from_pb(ctx, text):
    result = [x.strip() for x in text.split(",")]

    # TODO - extra bad. no.
    match result[0]:
        case "TOB":
            return ctx.bot.get_channel(ChannelIds.tob_pbs)
        case "COX":
            return ctx.bot.get_channel(ChannelIds.cox_pbs)
        case "TOA":
            return ctx.bot.get_channel(ChannelIds.toa_pbs)
        case "T":
            return ctx.bot.get_channel(ChannelIds.tzhaar_pbs)
        case "DT":
            return ctx.bot.get_channel(ChannelIds.dt2_pbs)
        case "M":
            return ctx.bot.get_channel(ChannelIds.misc_pbs)
        case "B":
            return ctx.bot.get_channel(ChannelIds.boss_pbs)


def get_raid_name(raid_type: str, group_size: int, mode) -> str:
    modes = {
        "TOB": {"Normal": "Theatre of Blood", "Hard": "Theatre of Blood: Hard Mode"},
        "COX": {
            "Normal": "Chambers of Xeric",
            "Challenge": "Chambers of Xeric: Challenge Mode",
        },
        "TOA": {
            "Normal": "Tombs of Amascut: Normal Mode",
            "Expert": "Tombs of Amascut: Expert Mode",
        },
    }

    group_sizes = {1: "Solo", 2: "Duo", 3: "Trio", 4: "4 man", 5: "5 man"}

    raid_type = raid_type.upper()

    if raid_type not in modes:
        return f"Invalid raid type: {raid_type}"

    if mode not in modes[raid_type]:
        return f"Invalid mode: {mode} for raid type {raid_type}"

    raid_name = f"{modes[raid_type][mode]} ({group_sizes[group_size]})"
    return raid_name
