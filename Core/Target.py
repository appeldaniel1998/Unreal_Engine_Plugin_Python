from Core.Coordinate import Coordinate


class Target:
    def __init__(self, displayName: str, className: str, position: Coordinate):
        self.displayName = displayName
        self.className = className
        self.position = position
