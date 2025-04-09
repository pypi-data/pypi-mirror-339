import pathlib
import socket
import unittest.mock

import pytest

import biosound.examples._examples


def test_EXAMPLE():
    assert isinstance(
        biosound.examples._examples.EXAMPLES, list
    )
    assert len(biosound.examples._examples.EXAMPLES) > 0
    assert all(
        [isinstance(
            example, biosound.examples._examples.Example
        ) for example in biosound.examples._examples.EXAMPLES]
    )


@pytest.fixture(params=[False, True])
def return_path(request):
    return request.param


@pytest.mark.parametrize(
    'example',
    biosound.examples._examples.EXAMPLES
)
def test_example(example, return_path):
    out = biosound.examples._examples.example(example.name, return_path=return_path)
    if example.type == biosound.examples._examples.ExampleTypes.ExampleData:
        assert isinstance(out, biosound.examples._examples.ExampleData)
        if return_path:
            for val in out.values():
                assert isinstance(val, (pathlib.Path, list))
                if isinstance(val, list):
                    assert all([isinstance(el, pathlib.Path) for el in val])
    else:
        if return_path:
            assert isinstance(out, pathlib.Path)
        else:
            if example.type == biosound.examples._examples.ExampleTypes.Sound:
                assert isinstance(out, biosound.Sound)
            elif example.type == biosound.examples._examples.ExampleTypes.Spectrogram:
                assert isinstance(out, biosound.Spectrogram)
            elif example.type == biosound.examples._examples.ExampleTypes.Annotation:
                assert isinstance(out, biosound.Annotation)


def test_show(capsys):
    biosound.examples._examples.show()
    captured = capsys.readouterr()
    for example in biosound.examples._examples.EXAMPLES:
        assert example.name in captured.out
        assert example.description in captured.out


@pytest.mark.parametrize(
    'name',
    [
        example.name
        for example in biosound.examples._examples.EXAMPLES
        if example.requires_download
    ]
)
def test_example_raises(name):
    with unittest.mock.patch(
        'urllib3.connection.connection.create_connection',
        side_effect=socket.gaierror
    ):
        with pytest.raises(ConnectionError):
            biosound.example(name)
