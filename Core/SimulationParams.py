
class SimulationParams:
    def __init__(self, numOfPeople: int, sunAngle: float, addPointsForRecognition: float, decreasePointsPerSec: float, simulationTime: int, pointsDeductedForCollision: float):
        self.numOfPeople: int = numOfPeople
        self.sunAngle: float = sunAngle
        self.addPointsForRecognition: float = addPointsForRecognition
        self.decreasePointsPerSec: float = decreasePointsPerSec
        self.simulationTime: int = simulationTime
        self.pointsDeductedForCollision: float = pointsDeductedForCollision
