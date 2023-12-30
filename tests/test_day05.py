import pytest

from jonas_aoc.day05 import SourceToDestinationMap, SourceToDestinationMaps


@pytest.mark.parametrize(
    ("seed", "expected_soil"),
    [
        (79, 81),
        (14, 14),
        (55, 57),
        (13, 13),
    ],
)
def test_get_destination(seed: int, expected_soil: int) -> None:
    seed_to_soil_map = SourceToDestinationMaps()
    seed_to_soil_map.append(SourceToDestinationMap(50, 98, 2))
    seed_to_soil_map.append(SourceToDestinationMap(52, 50, 48))
    soil = seed_to_soil_map.get_destination(seed)
    assert soil == expected_soil
