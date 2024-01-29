import operator


def get_fastest_times(data, boss_name):
    """
    Returns a list of personal best times for the given boss, sorted fastest to slowest.
    """
    print("hi")
    all_pbs_for_boss = (result for result in data if result["boss"] == boss_name)
    print(all_pbs_for_boss)
    return sorted(all_pbs_for_boss, key=operator.itemgetter("pb"))
