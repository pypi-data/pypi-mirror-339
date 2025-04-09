import pytest

import biosound

from .fixtures.audio import BIRDSONGREC_WAV_LIST


@pytest.mark.parametrize(
    'method',
    [
        None,
        'librosa-db',
    ]
)
def test_spectrogram(method, all_wav_paths):
    sound = biosound.Sound.read(all_wav_paths)
    if method is not None:
        spectrogram = biosound.spectrogram(sound, method=method)
    else:
        spectrogram = biosound.spectrogram(sound)
    assert isinstance(spectrogram, biosound.Spectrogram)


def test_input_not_audio_raises():
    """Test :func:`vocalpy.spectrogram` raises ValueError when first arg is not Sound"""
    sound = biosound.Sound.read(BIRDSONGREC_WAV_LIST[0])
    with pytest.raises(TypeError):
        biosound.spectrogram(sound.data)


def test_method_not_valid_raises():
    """Test :func:`vocalpy.spectrogram` raises ValueError when method arg is not valid"""
    sound = biosound.Sound.read(BIRDSONGREC_WAV_LIST[0])
    with pytest.raises(ValueError):
        biosound.spectrogram(sound, method='incorrect-method-name')
