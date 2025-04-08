import warnings

import pytest


def test_egg_hatch():
    assert 2 + 2 == 5

def test_egg_before_chicken():
    pytest.fail("This test is designed to fail")

def test_exception():
    with pytest.raises(ValueError):
        raise ValueError("This is an expected error")

@pytest.mark.filterwarnings("error")
def test_warning():
    warnings.warn("This is a warning")