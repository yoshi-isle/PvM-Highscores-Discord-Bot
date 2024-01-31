import operator
from hall_of_fame.autocompletes.autocompletes import AutoComplete


def get_fastest_times(data, boss_name):
    """
    Returns a list of personal best times for the given boss, sorted fastest to slowest.
    """
    all_pbs_for_boss = (result for result in data if result["boss"] == boss_name)
    return sorted(all_pbs_for_boss, key=operator.itemgetter("pb"))


def is_valid_group_members_string(group_members, group_size):
    result = [group_members.strip() for x in group_members.split(",")]
    return len(result) == group_size


def get_tob_raid_name(group_size: int, mode: AutoComplete.TOB_MODES):
    match mode:
        case AutoComplete.TOB_MODES.Normal:
            match group_size:
                case 1:
                    return "Theatre of Blood (Solo)"
                case 2:
                    return "Theatre of Blood (Duo)"
                case 3:
                    return "Theatre of Blood (Trio)"
                case 4:
                    return "Theatre of Blood (4 man)"
                case 5:
                    return "Theatre of Blood (5 man)"
        case AutoComplete.TOB_MODES.Hard:
            match group_size:
                case 1:
                    return "Chambers of Xeric: Challenge Mode (Solo)"
                case 2:
                    return "Chambers of Xeric: Challenge Mode (Duo)"
                case 3:
                    return "Chambers of Xeric: Challenge Mode (Trio)"
                case 4:
                    return "Chambers of Xeric: Challenge Mode (4 man)"
                case 5:
                    return "Chambers of Xeric: Challenge Mode (5 man)"


def get_cox_raid_name(group_size: int, mode: AutoComplete.COX_MODES):
    match mode:
        case AutoComplete.COX_MODES.Normal:
            match group_size:
                case 1:
                    return "Chambers of Xeric (Solo)"
                case 2:
                    return "Chambers of Xeric (Duo)"
                case 3:
                    return "Chambers of Xeric (Trio)"
                case 4:
                    return "Chambers of Xeric (4 man)"
                case 5:
                    return "Chambers of Xeric (5 man)"
        case AutoComplete.COX_MODES.Challenge:
            match group_size:
                case 1:
                    return "Chambers of Xeric: Challenge Mode (Solo)"
                case 2:
                    return "Chambers of Xeric: Challenge Mode (Duo)"
                case 3:
                    return "Chambers of Xeric: Challenge Mode (Trio)"
                case 4:
                    return "Chambers of Xeric: Challenge Mode (4 man)"
                case 5:
                    return "Chambers of Xeric: Challenge Mode (5 man)"


def get_toa_raid_name(group_size: int, mode: AutoComplete.TOA_MODES):
    match mode:
        case AutoComplete.TOA_MODES.Normal:
            match group_size:
                case 1:
                    return "Tombs of Amascut: Normal Mode (Solo)"
                case 2:
                    return "Tombs of Amascut: Normal Mode (Duo)"
                case 3:
                    return "Tombs of Amascut: Normal Mode (Trio)"
                case 4:
                    return "Tombs of Amascut: Normal Mode (4 man)"
                case 5:
                    return "Tombs of Amascut: Normal Mode (5 man)"
        case AutoComplete.TOA_MODES.Expert:
            match group_size:
                case 1:
                    return "Tombs of Amascut: Expert Mode (Solo)"
                case 2:
                    return "Tombs of Amascut: Expert Mode (Duo)"
                case 3:
                    return "Tombs of Amascut: Expert Mode (Trio)"
                case 4:
                    return "Tombs of Amascut: Expert Mode (4 man)"
                case 5:
                    return "Tombs of Amascut: Expert Mode (5 man)"
