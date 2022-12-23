from .Rock import Position, Rock


class Flat(Rock):
    def __init__(self, start_x: int, start_y: int):
        self._curr_pos = [
            Position(x=start_x, y=start_y),
            Position(x=start_x + 1, y=start_y),
            Position(x=start_x + 2, y=start_y),
            Position(x=start_x + 3, y=start_y),
        ]
