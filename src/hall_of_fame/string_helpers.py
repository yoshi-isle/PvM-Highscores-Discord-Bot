async def validate_string_format(usernames_string, group_size) -> int:
    """
    Checks if a string is in the format based on group size given:
    1 -> person1
    2 -> person1, person2
    3 -> person1, person2, person3
    ...
    8 -> person1, person2, person3, person4, person5, person6, person7, person8

    Args:
    usernames_string: The string to validate
    group_size: The group size to evaluate

    Returns:

    true for an correct input, false if bad input
    """

    result = [usernames_string.strip() for x in usernames_string.split(",")]
    if len(result) == group_size:
        return True
    else:
        return False
