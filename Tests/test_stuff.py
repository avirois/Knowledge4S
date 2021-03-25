import pytest
import random


def test_maybe_pass():
    assert random.random() > 0.5

def test_pass():
    assert True

def test_fail():
    assert False
