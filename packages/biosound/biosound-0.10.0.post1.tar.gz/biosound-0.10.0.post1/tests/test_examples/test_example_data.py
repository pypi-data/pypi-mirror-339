import pytest

import biosound
from biosound.examples.example_data import ExampleData


class TestExampleData:
    def test_init(self):
        bells = biosound.example("bells.wav")
        samba = biosound.example("samba.wav")
        zb_examples = ExampleData(bells=bells, samba=samba)
        assert isinstance(zb_examples, ExampleData)
        for keyattr, val in zip(
            ("bells", "samba"),
            (bells, samba)
        ):
            assert keyattr in zb_examples
            assert zb_examples[keyattr] == val
            assert hasattr(zb_examples, keyattr)
            assert getattr(zb_examples, keyattr) == val
