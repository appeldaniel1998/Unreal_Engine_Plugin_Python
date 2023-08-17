import json

if __name__ == '__main__':
    jsonDict = {
        "primitiveControls": {"upAmount": 1,
                              "pitchForwardAmount": 1,
                              "rollRightAmount": 0.5,
                              "yawRightAmount": -0.5},
        "getDroneState": "true",
    }

    json.dump(jsonDict, open("sampleJson.json", "w"))
