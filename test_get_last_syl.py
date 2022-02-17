from reconstruct_pub_wise import get_last_syl


def test_get_last_syl():
    test_cases = [
        "མཐོ་བཙུན་གྲུབ་རྗེས་མཛད་པ་རྫོགས་སོ།། །།",
        "བསྲེགས། །ལྷ་ཆེན་གྱིས་ནི་འདོད་པ་དག །བསྲེགས་",
        "བཅད་བསྲེགས་ནས་བཏོན། །ལྷ་ཆེན་ཐིག་ལེའི་",
        "བཅད་བསྲེགས་ནས་བཏོན།",
    ]
    expected_results = [
        "།།",
        "བསྲེགས་",
        "ལེའི་",
        "བཏོན།"
    ]
    for test_case, expected_syl in zip(test_cases, expected_results):
        last_syl = get_last_syl(test_case)
        assert last_syl == expected_syl


if __name__ == "__main__":
    test_get_last_syl()