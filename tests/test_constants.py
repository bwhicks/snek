from snek.constants import ValueStringMixin

class TestValueStringMixin:

    def test___str__(self):
        value = ValueStringMixin()
        value.value = "foo"
        assert str(value) == "foo"
