from animations.intersection.constants import LANE_WIDTH
from geometry import Directions
from intersection.intersection import Intersection
from intersection.schemas import CarOnIntersection


# Easy to create another types of intersections, like for example one with signs
# such class would just need to implement poper rules in has_priority function
# and maybe define its own draw method (calling super().draw() and then drawing signs)
# also it's easy to provide priority to some cars (ambulance for example)
class PriorityToTheRightIntersection(Intersection):
    def __init__(self):
        super().__init__(LANE_WIDTH)

    def has_priority(car1: CarOnIntersection, car2: CarOnIntersection) -> bool:
        directions = [Directions.DOWN, Directions.RIGHT, Directions.UP, Directions.LEFT]
        starting_side_index = directions.index(car1["starting_side"])
        direction_index = (starting_side_index + 1) % 4
        while directions[direction_index] != car1["ending_side"]:
            if directions[direction_index] == car2["starting_side"]:
                return False
            direction_index = (direction_index + 1) % 4
        return True
