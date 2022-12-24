from typing import Set, Tuple


class RockFactory:
    @staticmethod
    def create(
        curr_num_of_shapes: int, start_x: int, start_y: int
    ) -> Set[Tuple[int, int]]:
        pick_shape = curr_num_of_shapes % 5

        if pick_shape == 0:
            return set(
                [
                    (start_x, start_y),
                    (start_x + 1, start_y),
                    (start_x + 2, start_y),
                    (start_x + 3, start_y),
                ]
            )
        elif pick_shape == 1:
            return set(
                [
                    (start_x, start_y + 1),
                    (start_x + 1, start_y),
                    (start_x + 1, start_y + 1),
                    (start_x + 1, start_y + 2),
                    (start_x + 2, start_y + 1),
                ]
            )
        elif pick_shape == 2:
            return set(
                [
                    (start_x, start_y),
                    (start_x + 1, start_y),
                    (start_x + 2, start_y),
                    (start_x + 2, start_y + 1),
                    (start_x + 2, start_y + 2),
                ]
            )
        elif pick_shape == 3:
            return set(
                [
                    (start_x, start_y),
                    (start_x, start_y + 1),
                    (start_x, start_y + 2),
                    (start_x, start_y + 3),
                ]
            )

        elif pick_shape == 4:
            return set(
                [
                    (start_x, start_y),
                    (start_x, start_y + 1),
                    (start_x + 1, start_y),
                    (start_x + 1, start_y + 1),
                ]
            )
        else:
            raise Exception("Unexpected create path")
