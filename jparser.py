import json
import logging

x = """{"CollisionCount":2,"positionXVal":19452.971715351981,"positionYVal":33532.626349985774,"positionZVal":799.30230280677222,
       "simulationTime":4, "pointsAtStartOfGame":100000,"collisionCost":200, "pointsForHumanDetected":100}"""
# cost for delay is how many points to decrease each 1 sec during the simulation
# parse x:
gradeConfig = json.loads(x)


def setup_logger(log_filename):
    # Create a logger
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the level to DEBUG
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and attach it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    return logger

# if __name__ == '__main__':
#    pass

# jsonDict = {
#     "primitiveControls": {"upAmount": 1,
#                           "pitchForwardAmount": 1,
#                           "rollRightAmount": 0.5,
#                           "yawRightAmount": -0.5},
#     "getDroneState": "true",
# }
#
# json.dump(jsonDict, open("sampleJson.json", "w"))

# Multi-line string -i.e the string we want to save
