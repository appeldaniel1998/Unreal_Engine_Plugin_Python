import json

if __name__ == "__main__":
    toJsonDict = {
        "pointsAtStartOfGame": 100,
        "simulationTime": 10,  # In seconds (minutes * 60)
        "pointsForTargetDetection": 10,  # The number of points the agent receives upon detecting correctly an Aruco QR code
        "costPointsPerSec": 1,
        "costPointsPerCollision": 50,
    }

    with open("gradeConfig.json", "w") as file:
        json.dump(toJsonDict, file, indent=4)
