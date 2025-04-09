import inspect

import pytest

import biosound

from .fixtures.audio import BIRDSONGREC_WAV_LIST


class TestSegmenter:
    @pytest.mark.parametrize(
        "callback, params, expected_callback, expected_params",
        [
            (None,
             None,
             biosound.segment.meansquared,
             biosound.segmenter.DEFAULT_SEGMENT_PARAMS),
            (biosound.segment.meansquared,
             None,
             biosound.segment.meansquared,
             {name: param.default
              for name, param in inspect.signature(biosound.segment.meansquared).parameters.items()
              if param.default is not inspect._empty}
             ),
            (biosound.segment.meansquared,
             {"smooth_win": 2},
             biosound.segment.meansquared,
             {"smooth_win": 2}
             ),
            (biosound.segment.meansquared,
             biosound.segment.MeanSquaredParams(threshold=1500),
             biosound.segment.meansquared,
             {**biosound.segment.MeanSquaredParams(threshold=1500)}),
            (biosound.segment.ava,
             None,
             biosound.segment.ava,
             {name: param.default
              for name, param in inspect.signature(biosound.segment.ava).parameters.items()
              if param.default is not inspect._empty},
             ),
            (biosound.segment.ava,
             biosound.segment.AvaParams(thresh_min=3.0),
             biosound.segment.ava,
             {**biosound.segment.AvaParams(thresh_min=3.0)}
             )
        ],
    )
    def test_init(self, callback, params, expected_callback, expected_params):
        segmenter = biosound.Segmenter(callback=callback, params=params)
        assert isinstance(segmenter, biosound.Segmenter)
        assert segmenter.callback is expected_callback
        assert segmenter.params == expected_params

    @pytest.mark.parametrize(
        "sound",
        [
            biosound.Sound.read(BIRDSONGREC_WAV_LIST[0]),
            biosound.AudioFile(path=BIRDSONGREC_WAV_LIST[0]),
            [biosound.Sound.read(path) for path in BIRDSONGREC_WAV_LIST[:3]],
            [biosound.AudioFile(path=path) for path in BIRDSONGREC_WAV_LIST[:3]],
        ],
    )
    def test_segment(self, sound, parallel):
        # have to use different segment params from default for these .wav files
        params = {
            "threshold": 5e-05,
            "min_dur": 0.02,
            "min_silent_dur": 0.002,
        }
        segmenter = biosound.Segmenter(params=params)

        out = segmenter.segment(sound, parallelize=parallel)

        if isinstance(sound, (biosound.Sound, biosound.AudioFile)):
            assert isinstance(out, biosound.Segments)
        elif isinstance(sound, list):
            assert isinstance(out, list)
            assert len(sound) == len(out)
            for segments in out:
                assert isinstance(segments, biosound.Segments)
