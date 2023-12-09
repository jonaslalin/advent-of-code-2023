from dataclasses import dataclass
from itertools import islice
from typing import Iterable, Iterator, List, TextIO, Tuple, TypeVar


@dataclass
class SourceToDestinationMap:
    destination_range_start: int
    source_range_start: int
    range_length: int

    def __str__(self) -> str:
        return f"{self.destination_range_start} {self.source_range_start} {self.range_length}"


@dataclass
class SourceToDestinationMaps(List[SourceToDestinationMap]):
    def get_destination(self, source: int) -> int:
        destination = source
        for source_to_destination_map in self:
            if (
                source >= source_to_destination_map.source_range_start
                and source <= source_to_destination_map.source_range_start + source_to_destination_map.range_length
            ):
                destination = source_to_destination_map.destination_range_start + (
                    source - source_to_destination_map.source_range_start
                )
                break
        return destination


def read_seeds(f: TextIO) -> List[int]:
    line = f.readline()
    seeds = list(map(int, line.split()[1:]))
    f.readline()
    return seeds


def read_source_to_destination_maps(f: TextIO) -> SourceToDestinationMaps:
    source_to_destination_map = SourceToDestinationMaps()
    f.readline()
    while (line := f.readline()) != "\n" and line != "":
        source_to_destination_map.append(SourceToDestinationMap(*map(int, line.split())))
    return source_to_destination_map


T = TypeVar("T")


def batched(iterable: Iterable[T], n: int) -> Iterator[Tuple[T, ...]]:
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def main(path: str = "input/day05.txt") -> None:
    with open(path) as f:
        seeds = read_seeds(f)
        seed_to_soil_map = read_source_to_destination_maps(f)
        soil_to_fertilizer_map = read_source_to_destination_maps(f)
        fertilizer_to_water_map = read_source_to_destination_maps(f)
        water_to_light_map = read_source_to_destination_maps(f)
        light_to_temperature_map = read_source_to_destination_maps(f)
        temperature_to_humidity_map = read_source_to_destination_maps(f)
        humidity_to_location_map = read_source_to_destination_maps(f)

    def get_lowest_location(seeds: Iterable[int]) -> int:
        soils = map(seed_to_soil_map.get_destination, seeds)
        fertilizers = map(soil_to_fertilizer_map.get_destination, soils)
        water = map(fertilizer_to_water_map.get_destination, fertilizers)
        lights = map(water_to_light_map.get_destination, water)
        temperatures = map(light_to_temperature_map.get_destination, lights)
        humidity = map(temperature_to_humidity_map.get_destination, temperatures)
        locations = map(humidity_to_location_map.get_destination, humidity)
        lowest_location = min(locations)
        return lowest_location

    print(f"Lowest location (part one): {get_lowest_location(seeds)}")

    new_seeds = (seed for start, length in zip(seeds[::2], seeds[1::2]) for seed in range(start, start + length))
    global_lowest_location = -1
    for seed_batch in batched(new_seeds, 1_000_000):
        batch_lowest_location = get_lowest_location(seed_batch)
        print(f"Batch lowest location (part two): {batch_lowest_location}")
        if batch_lowest_location < global_lowest_location or global_lowest_location == -1:
            global_lowest_location = batch_lowest_location
    print(f"Global lowest location (part two): {global_lowest_location}")


if __name__ == "__main__":
    main()
