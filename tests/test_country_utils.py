from utils.country import load_countries

NUM_COUNTRIES = 193  # number of state members of the United Nations


def test_num_countries():
    assert len(load_countries(True)) == NUM_COUNTRIES
