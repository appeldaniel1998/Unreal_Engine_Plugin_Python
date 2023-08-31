import json

if __name__ == '__main__':
    jsonDict = {
        "primitiveControls": {"upAmount": 1,
                              "pitchForwardAmount": 1,
                              "rollRightAmount": 0.5,
                              "yawRightAmount": -0.5},
        "getDroneState": "true",
        "droneGrade": 100,
    }

    json.dump(jsonDict, open("sampleJson.json", "w"))
