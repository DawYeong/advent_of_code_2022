from .Rock import Position, Rock


class Long(Rock):
    def __init__(self, start_x: int, start_y: int):
        self._curr_pos = [
            Position(x=start_x, y=start_y),
            Position(x=start_x, y=start_y+1),
            Position(x=start_x, y=start_y+2),
            Position(x=start_x, y=start_y+3),
        ]
