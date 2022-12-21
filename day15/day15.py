from dataclasses import dataclass
from itertools import combinations
import os
from typing import List, Optional, Tuple


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
    ) -> Optional[Range]:
        distance_required = abs(y - self._signal.y)
        if distance_required > self._beacon_distance:
            return None

        remaining_x_dist = self._beacon_distance - distance_required
        return Range(
            start=self._signal.x - remaining_x_dist,
            end=self._signal.x + remaining_x_dist,
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
) -> List[Range]:
    blocked_ranges = []
    for beacon_zone in beacon_zones:
        ranges = beacon_zone.get_block_range_at_level(y=row)
        if ranges:
            blocked_ranges.append(ranges)

    combine_overlapping_ranges(blocked_ranges)

    return blocked_ranges


def get_blocked_positions(
    beacon_zones: List[BeaconZone],
    row: int,
    blocked_ranges: List[Range],
) -> int:
    num_beacons = len(
        set(
            [
                beacon_zone.get_beacon()
                for beacon_zone in beacon_zones
                if beacon_zone.is_beacon_on_level(row)
            ]
        )
    )

    total_blocked_positions = 0
    for blocked_range in blocked_ranges:
        total_blocked_positions += blocked_range.end - blocked_range.start + 1

    return total_blocked_positions - num_beacons


def solve_part_1(file_name: str):
    beacon_zones = get_beacon_zones(file_name)
    check_row = 2000000
    blocked_ranges = get_blocked_ranges(beacon_zones=beacon_zones, row=check_row)
    total_block_positions = get_blocked_positions(
        beacon_zones=beacon_zones,
        row=check_row,
        blocked_ranges=blocked_ranges,
    )
    print(total_block_positions)


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
