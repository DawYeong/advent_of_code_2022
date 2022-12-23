from .Rock import Position, Rock


class Square(Rock):
    def __init__(self, start_x: int, start_y: int):
        self._curr_pos = [
            Position(x=start_x, y=start_y),
            Position(x=start_x, y=start_y+1),
            Position(x=start_x+1, y=start_y),
            Position(x=start_x+1, y=start_y+1),
        ]
