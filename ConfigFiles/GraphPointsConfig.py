import json

if __name__ == "__main__":
    toJsonDict = {
        # points on th graph. 0 is x, 1 is y, 2 is z values
        "0": [19715, 33581, 206],
        "1": [19715, 33063, 322],
        "2": [20258, 32629, 194],
        "3": [20258, 32629, 651],
        "4": [0, 0, 0],
        "5": [0, 0, 0],
        "6": [0, 0, 0],
        "7": [0, 0, 0],
        "8": [0, 0, 0],
        "9": [0, 0, 0],
    }

    with open("graphPointsConfig.json", "w") as file:
        json.dump(toJsonDict, file, indent=4)
