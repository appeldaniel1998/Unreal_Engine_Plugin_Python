import json

x = """{"CollisionCount":0,"positionXVal":19452.971715351981,"positionYVal":33532.626349985774,"positionZVal":799.30230280677222,
       "simulationTime":2, "initializedScore":100000,"collisionCost":5}"""
# cost for delay is how many points to decrease each 1 sec during the simulation
# parse x:
y = json.loads(x)
if __name__ == '__main__':
   pass

    # jsonDict = {
    #     "primitiveControls": {"upAmount": 1,
    #                           "pitchForwardAmount": 1,
    #                           "rollRightAmount": 0.5,
    #                           "yawRightAmount": -0.5},
    #     "getDroneState": "true",
    # }
    #
    # json.dump(jsonDict, open("sampleJson.json", "w"))

    # Multi-line string -i.e the string we want to save

