import pytest


def test_egg_hatch():
    assert True

def test_egg_before_chicken():
    pytest.fail("This test is designed to fail")
