from typing import Set, Tuple


class RockService:
    @staticmethod
    def jet_move_rock(curr_rock: Set[Tuple[int, int]], jet_dir: bool) -> Set[Tuple[int, int]]:
        # move rock right if jet_dir is True, left if False
        move_rock = 1 if jet_dir else -1

        if (jet_dir and any([x == 6 for (x, _) in curr_rock])) or (
            not jet_dir and any([x == 0 for (x, _) in curr_rock])
        ):
            return curr_rock

        return set([(x+move_rock, y) for (x, y) in curr_rock])

    @staticmethod
    def rock_fall(curr_rock: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        return set([(x, y-1)for (x, y) in curr_rock])
        

