from typing import List
from typing_extensions import TypedDict

FILE_NAME = "input.txt"

class RockPaperScissorMatchup(TypedDict):
    score: int
    A: int # Rock
    B: int # Paper
    C: int # Scissor

class Matchup(TypedDict):
    first: str
    second: str

PLAYER_SCORES = {
    "X": RockPaperScissorMatchup(score=1, A=3, B=0, C=6),
    "Y": RockPaperScissorMatchup(score=2, A=6, B=3, C=0),
    "Z": RockPaperScissorMatchup(score=3, A=0, B=6, C=3),
}


def get_match_ups(file_name: str) -> List[Matchup]:
    with open(file_name, 'r') as file:
        data = file.read()

    data_lines = data.split('\n')
    match_ups = [make_match_up(match_up) for match_up in data_lines]

    return match_ups
    
def make_match_up(raw_match_up: str) -> Matchup:
    match_up = raw_match_up.split(" ")

    assert len(match_up) == 2

    return Matchup(first=match_up[0], second=match_up[1])

def solve_part_1():
    match_ups = get_match_ups(FILE_NAME)

    sum = 0

    for match_up in match_ups:
        round_value = PLAYER_SCORES[match_up["second"]]["score"] + PLAYER_SCORES[match_up["second"]][match_up["first"]]
        sum += round_value

    print(sum)


if __name__ == "__main__":
    solve_part_1()
