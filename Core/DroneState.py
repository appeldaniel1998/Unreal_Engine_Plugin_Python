from Core.Coordinate import Coordinate


class DroneState:
    def __init__(self, location: Coordinate, collisionCount: int):
        self.location = location
        self.collisionCount = collisionCount
