import inspect

import pytest

import biosound


class TestFeatureExtractor:

    @pytest.mark.parametrize(
            'callback, params',
            [
                
                (
                    biosound.feature.sat,
                    None,
                ),
                (
                    biosound.feature.biosound,
                    None,
                )
            ]
    )
    def test___init__(self, callback, params):
        extractor = biosound.FeatureExtractor(callback=callback, params=params)
        assert isinstance(extractor, biosound.FeatureExtractor)
        assert extractor.callback is callback
        if params is None:            
            signature = inspect.signature(callback)
            expected_params = {
                name: param.default
                for name, param in signature.parameters.items()
                if param.default is not inspect._empty
            }
        else:
            expected_params = params
        assert extractor.params == expected_params

    @pytest.mark.parametrize(
            'callback, params, sound_str',
            [
                
                (
                    biosound.feature.sat,
                    None,
                    "a_zebra_finch_song_sound"
                ),
                (
                    biosound.feature.sat,
                    None,
                    "a_list_of_zebra_finch_song_sounds"
                ),
                (
                    biosound.feature.biosound,
                    None,
                    "a_elie_theunissen_2016_sound",
                ),
                (
                    biosound.feature.biosound,
                    None,
                    "a_list_of_elie_theunissen_2016_sounds",
                )

            ]
    )
    def test_extract(self, callback, params, sound_str, request):
        sound = request.getfixturevalue(sound_str)
        extractor = biosound.FeatureExtractor(callback=callback, params=params)
        features = extractor.extract(sound)
        if isinstance(sound, biosound.Sound):
            assert isinstance(features, biosound.Features)
        elif isinstance(sound, list) and all([isinstance(element, biosound.Sound) for element in sound]):
            assert isinstance(features, list)
            assert all([isinstance(element, biosound.Features) for element in features])
