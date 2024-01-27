import pytest
import src.hall_of_fame.data_helper as data_helper
import testdata.boss_data as boss_data


@pytest.mark.parametrize(
    "data, expected_result",
    [(boss_data.get_boss_data(), boss_data.sorted_boss_data())],
)
def test_get_fastest_times(data, expected_result):
    print(data)
    print("-------")
    result = data_helper.get_fastest_times(data, "Zulrah")
    print(result)
    print("~~~~~~~")
    print(expected_result)
    print("@@@@@@@@")

    assert True == True
    assert result == expected_result

    """
    sut:
    import operator
def get_fastest_times(data, boss_name):

    all_pbs_for_boss = (result for result in data if result["boss"] == boss_name)
    return sorted(all_pbs_for_boss, key=operator.itemgetter("pb"))

    """
