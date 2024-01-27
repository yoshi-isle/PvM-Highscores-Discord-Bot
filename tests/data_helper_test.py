import pytest
import src.hall_of_fame.data_helper as data_helper

def test_sanity():
    data_helper.get_fastest_times([], "")
    assert True == True

@pytest.mark.parametrize("data, expected_result", [
    ("", ""),
    ("", ""),
    ("", ""),
    ("", "")
])
def get_fastest_times_tests(data, expected_result):
    result = data_helper.get_fastest_times(data, "")

    assert (result == expected_result)

    """
    sut:
    import operator
def get_fastest_times(data, boss_name):

    all_pbs_for_boss = (result for result in data if result["boss"] == boss_name)
    return sorted(all_pbs_for_boss, key=operator.itemgetter("pb"))

    """