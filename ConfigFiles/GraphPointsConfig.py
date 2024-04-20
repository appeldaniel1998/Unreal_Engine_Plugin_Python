import json

if __name__ == "__main__":
    toJsonDict = {  # points on th graph. 0 is x, 1 is y, 2 is z values
        "0": [2260.0, 7380.0, 1680.0],
        "1": [-4020.0, 7380.0, 1680.0],
        "2": [-4020.0, 2260.0, 1680.0],
        "3": [5000.0, 2260.0, 1680.0],
        "4": [5000.0, -1650.0, 1680.0],
        "5": [-4070.0, -1650.0, 1680.0],
        "6": [-4070.0, -4780.0, 1680.0],
        "7": [4080.0, -4780.0, 1680.0]
    }

    with open("graphPointsConfig.json", "w") as file:
        json.dump(toJsonDict, file, indent=4)
