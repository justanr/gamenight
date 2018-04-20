from gamenight import __version__, all_odd


def test_it_works():
    assert __version__ == '0.0.1'


def test_all_are_odd():
    assert all_odd(1, 3, 5)
