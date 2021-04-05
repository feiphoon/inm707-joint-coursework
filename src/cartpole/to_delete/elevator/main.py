from environment.building import Building
from environment.elevator import Elevator


def display(building, elevator):
    """
    passengers later
    """
    pass
    # for b in building:
    #     for e in elevator:
    #         z = [" ".join(item) for item in zip(x, y)]

    # This display is flipped, just to keep our calculations simple


NUM_FLOORS = 3
MAX_NUM_PASSENGERS = 10
b = Building(num_floors=NUM_FLOORS, max_num_passengers=MAX_NUM_PASSENGERS)
print(repr(b))

e = Elevator(capacity=1, num_floors=NUM_FLOORS)
print(repr(e))
