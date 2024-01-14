def get_fastest_times(data, boss_name):
    return sorted(
        [result for result in data if result["boss"] == boss_name],
        key=lambda x: x["pb"],
    )