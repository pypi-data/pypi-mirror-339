import inspect

import pytest

import biosound

from .fixtures.audio import BIRDSONGREC_WAV_LIST
from .fixtures.spect import SPECT_LIST_NPZ


@pytest.mark.parametrize(
    "sound",
    [
        biosound.Sound.read(BIRDSONGREC_WAV_LIST[0]),
        biosound.AudioFile(path=BIRDSONGREC_WAV_LIST[0]),
        [biosound.Sound.read(path) for path in BIRDSONGREC_WAV_LIST[:3]],
        [biosound.AudioFile(path=path) for path in BIRDSONGREC_WAV_LIST[:3]],
    ],
)
def test_validate_sound(sound):
    assert biosound.spectrogram_maker.validate_sound(sound) is None


@pytest.mark.parametrize(
    "not_audio, expected_exception",
    [
        (biosound.Spectrogram.read(SPECT_LIST_NPZ[0]), TypeError),
        (dict(), TypeError),
        ([biosound.Spectrogram.read(path) for path in SPECT_LIST_NPZ[:3]], TypeError),
        (
            [biosound.Sound.read(path) for path in BIRDSONGREC_WAV_LIST[:3]]
            + [biosound.AudioFile(path=path) for path in BIRDSONGREC_WAV_LIST[:3]],
            TypeError,
        ),
    ],
)
def test_validate_sound_not_audio_raises(not_audio, expected_exception):
    with pytest.raises(expected_exception=expected_exception):
        biosound.spectrogram_maker.validate_sound(not_audio)


class TestSpectrogramMaker:
    @pytest.mark.parametrize(
        "callback, params, expected_callback, expected_params",
        [
            (None,
             None,
             biosound.spectrogram,
             biosound.spectrogram_maker.DEFAULT_SPECT_PARAMS
             ),
            (biosound.spectrogram,
             None,
             biosound.spectrogram,
             {name: param.default
              for name, param in inspect.signature(biosound.spectrogram).parameters.items()
              if param.default is not inspect._empty}
             )
        ],
    )
    def test_init(self, callback, params, expected_callback, expected_params):
        spect_maker = biosound.SpectrogramMaker(callback=callback, params=params)
        assert isinstance(spect_maker, biosound.SpectrogramMaker)
        assert spect_maker.callback is expected_callback
        assert spect_maker.params == expected_params

    @pytest.mark.parametrize(
        "sound",
        [
            biosound.Sound.read(BIRDSONGREC_WAV_LIST[0]),
            biosound.AudioFile(path=BIRDSONGREC_WAV_LIST[0]),
            [biosound.Sound.read(path) for path in BIRDSONGREC_WAV_LIST[:3]],
            [biosound.AudioFile(path=path) for path in BIRDSONGREC_WAV_LIST[:3]],
        ],
    )
    def test_make(self, sound, parallel):
        spect_maker = biosound.SpectrogramMaker()

        out = spect_maker.make(sound, parallelize=parallel)

        if isinstance(sound, (biosound.Sound, biosound.AudioFile)):
            assert isinstance(out, biosound.Spectrogram)
        elif isinstance(sound, list):
            assert all([isinstance(spect, biosound.Spectrogram) for spect in out])
