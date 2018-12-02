def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4


class TestClass():
    def test_one(self):
        x = "herp"
        assert 'e' in x

    def test_two(self):
        x = "derp"
        assert hasattr(x, 'upper')
