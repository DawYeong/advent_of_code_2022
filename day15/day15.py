from dataclasses import dataclass
from itertools import combinations
import os
from typing import List, Optional, Tuple, Set


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False


@dataclass(frozen=True)
class Range:
    start: int
    end: int


class BeaconZone:
    _signal: Position
    _closest_beacon: Position
    _beacon_distance: int

    def __init__(
        self,
        signal: Position,
        closest_beacon: Position,
    ):
        self._signal = signal
        self._closest_beacon = closest_beacon
        self._beacon_distance = abs(signal.x - closest_beacon.x) + abs(
            signal.y - closest_beacon.y
        )

    def get_block_range_at_level(
        self,
        y: int,
        part_2: bool,
        max_range: int = 0,
    ) -> Optional[Range]:
        distance_required = abs(y - self._signal.y)
        if distance_required > self._beacon_distance:
            return None

        remaining_x_dist = self._beacon_distance - distance_required
        return Range(
            start=self._signal.x - remaining_x_dist
            if not part_2
            else max(self._signal.x - remaining_x_dist, 0),
            end=self._signal.x + remaining_x_dist
            if not part_2
            else min(self._signal.x + remaining_x_dist, max_range),
        )

    def is_beacon_on_level(
        self,
        y: int,
    ) -> bool:
        return self._closest_beacon.y == y

    def is_beacon_in_range(
        self,
        blocked_range: Range,
    ) -> bool:
        return blocked_range.start <= self._closest_beacon.x <= blocked_range.end

    def get_beacon(self):
        return self._closest_beacon


def get_beacon_zones(file_name: str) -> List[BeaconZone]:
    beacon_zones = []
    with open(file_name, "r") as file:
        while True:
            data_line = file.readline()
            if not data_line:
                break

            position_string = (
                data_line.strip()
                .replace("x=", "")
                .replace("y=", "")
                .replace(",", "")
                .replace(":", "")
                .split(" ")
            )

            signal = Position(
                x=int(position_string[2]),
                y=int(position_string[3]),
            )

            beacon = Position(
                x=int(position_string[8]),
                y=int(position_string[9]),
            )

            beacon_zones.append(
                BeaconZone(
                    signal=signal,
                    closest_beacon=beacon,
                )
            )
    return beacon_zones


def find_overlapping_ranges(ranges: List[Range]) -> Optional[Tuple[Range, Range]]:
    for item1, item2 in combinations(ranges, 2):
        if item1.start > item2.end or item1.end < item2.start:
            continue
        else:
            return item1, item2

    return None


def combine_overlapping_ranges(ranges: List[Range]):
    while True:
        overlaps = find_overlapping_ranges(ranges)
        if not overlaps:
            break

        ranges.remove(overlaps[0])
        ranges.remove(overlaps[1])

        ranges.append(
            Range(
                start=min(overlaps[0].start, overlaps[1].start),
                end=max(overlaps[0].end, overlaps[1].end),
            )
        )


def get_blocked_ranges(
    beacon_zones: List[BeaconZone],
    row: int,
    part_2: bool = False,
    max_range: int = 0,
) -> List[Range]:
    blocked_ranges = []
    for beacon_zone in beacon_zones:
        ranges = beacon_zone.get_block_range_at_level(
            y=row,
            part_2=part_2,
            max_range=max_range,
        )
        if ranges:
            blocked_ranges.append(ranges)

    combine_overlapping_ranges(blocked_ranges)

    return blocked_ranges


def get_blocked_positions(
    beacon_zones: List[BeaconZone],
    row: int,
    blocked_ranges: List[Range],
    part_2: bool = False,
) -> int:
    num_beacons = len(
        set(
            [
                beacon_zone.get_beacon()
                for beacon_zone in beacon_zones
                if beacon_zone.is_beacon_on_level(row)
            ]
        )
        if not part_2
        else []
    )

    total_blocked_positions = 0
    for blocked_range in blocked_ranges:
        total_blocked_positions += blocked_range.end - blocked_range.start + 1

    return total_blocked_positions - num_beacons


def find_missing_number(
    max_number: int,
    ranges: List[Range],
) -> Set[int]:
    check_range = set(
        list(
            range(
                0,
                max_number + 1,
            )
        )
    )
    # print(check_range)
    for r in ranges:
        check_range = check_range - set(
            list(
                range(
                    max(0, r.start),
                    min(max_number + 1, r.end + 1),
                )
            )
        )
        # updating range according to min and max
    return check_range


def solve_part_1(file_name: str):
    beacon_zones = get_beacon_zones(file_name)
    check_row = 2000000
    blocked_ranges = get_blocked_ranges(
        beacon_zones=beacon_zones,
        row=check_row,
    )
    total_block_positions = get_blocked_positions(
        beacon_zones=beacon_zones,
        row=check_row,
        blocked_ranges=blocked_ranges,
    )
    print(total_block_positions)


# hacky solution and pretty slow ~ 1.5 mins
# we loop through all the possible rows and find one with an unblocked position
# since every possible position is 0 to 4000000 => there should 1 row with 4000000 blocked positions while others have 4000001
# then take the differences between the ranges => create sets using range and subtract from each other (very inefficient)
def solve_part_2(file_name: str):
    beacon_zones = get_beacon_zones(file_name)
    tuning_constant = 4000000
    tuning_freq = 0
    for i in range(tuning_constant + 1):
        blocked_ranges = get_blocked_ranges(
            beacon_zones=beacon_zones,
            row=i,
            part_2=True,
            max_range=tuning_constant,
        )
        total_block_positions = get_blocked_positions(
            beacon_zones=beacon_zones,
            row=i,
            blocked_ranges=blocked_ranges,
            part_2=True,
        )

        if total_block_positions == tuning_constant:
            missing_number = find_missing_number(
                max_number=tuning_constant,
                ranges=blocked_ranges,
            )
            if missing_number:
                tuning_freq = next(iter(missing_number)) * tuning_constant + i
                break

    print(f"Tuning Frequency: {tuning_freq}")


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
