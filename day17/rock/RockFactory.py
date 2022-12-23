from rock.models.Rock import Rock
from rock.models.Cross import Cross
from rock.models.Flat import Flat
from rock.models.Long import Long
from rock.models.LShape import LShape
from rock.models.Square import Square


class RockFactory:
    @staticmethod
    def create(curr_num_of_shapes: int, start_x: int, start_y: int) -> Rock:
        pick_shape = curr_num_of_shapes % 5

        if pick_shape == 0:
            return Flat(start_x=start_x, start_y=start_y,)
        elif pick_shape == 1:
            return Cross(start_x=start_x, start_y=start_y,)
        elif pick_shape == 2:
            return LShape(start_x=start_x, start_y=start_y,)
        elif pick_shape == 3:
            return Long(start_x=start_x, start_y=start_y,)
        elif pick_shape == 4:
            return Square(start_x=start_x, start_y=start_y,)
        else:
            raise Exception("Unexpected create path")
