import json
import tkinter as tk


def finishGui(num_people, angle_sun, recognize_points, decrease_points, totalTime, pointsDeductedForCollision, initialPoints):
    # Your game logic goes here
    print(f"Starting game with {num_people} people and angle of sun {angle_sun}.")
    print(f"For each person recognized you will receive {recognize_points} points")
    print(f"For each second in the game, you will loose {decrease_points} points")
    print(f"The game will last {totalTime} seconds.")
    print(f"If a collision is detected, {pointsDeductedForCollision} points will be deducted.")
    print(f"Initial number of points in the simulation is:, {initialPoints} points will be deducted.")

    # Convert values to a dictionary
    game_data = {
        "numOfPeople": num_people,
        "sunAngle": angle_sun,
        "addPointsForRecognition": recognize_points,
        "decreasePointsPerSec": decrease_points,
        "simulationTime": totalTime,
        "pointsDeductedForCollision": pointsDeductedForCollision,
        "initialPoints": initialPoints
    }

    # json.dumps(game_data)  # Convert dictionary to JSON string
    with open("gradeConfig.json", "w") as file:
        json.dump(game_data, file, indent=4)


class Gui:
    def __init__(self):
        self.popup: tk.Tk = tk.Tk()  # Define popup as a global variable
        self.popup.title("Game Settings")
        self.create_popup()

    def create_popup(self):
        # Label and Entry for Number of People
        people_label = tk.Label(self.popup, text="Number of people:")
        people_label.grid(row=0, column=0)
        people_entry = tk.Entry(self.popup)
        people_entry.grid(row=0, column=1)

        # Label and Entry for Angle of Sun
        angle_label = tk.Label(self.popup, text="Angle of the sun:")
        angle_label.grid(row=1, column=0)
        angle_entry = tk.Entry(self.popup)
        angle_entry.grid(row=1, column=1)

        # Label and Entry for points increase for recognizing people
        recognize_label = tk.Label(self.popup, text="Points added for recognizing a person:")
        recognize_label.grid(row=2, column=0)
        recognize_entry = tk.Entry(self.popup)
        recognize_entry.grid(row=2, column=1)

        # Label and Entry for points decrease per minute
        pdecrease_label = tk.Label(self.popup, text="Points deducted per second:")
        pdecrease_label.grid(row=3, column=0)
        pdecrease_entry = tk.Entry(self.popup)
        pdecrease_entry.grid(row=3, column=1)

        # Label and Entry for simulation total time
        ttime_label = tk.Label(self.popup, text="Simulation total time (seconds):")
        ttime_label.grid(row=4, column=0)
        ttime_entry = tk.Entry(self.popup)
        ttime_entry.grid(row=4, column=1)

        # Label and Entry for Points deducted for collision
        pCollisionLabel = tk.Label(self.popup, text="Points deducted for collision:")
        pCollisionLabel.grid(row=5, column=0)
        pCollisionEntry = tk.Entry(self.popup)
        pCollisionEntry.grid(row=5, column=1)

        # Label and Entry for Points deducted for collision
        initialPointsLabel = tk.Label(self.popup, text="Initial number of points:")
        initialPointsLabel.grid(row=6, column=0)
        initialPointsEntry = tk.Entry(self.popup)
        initialPointsEntry.grid(row=6, column=1)

        # Button to Start Game
        start_button = tk.Button(self.popup,
                                 text="Save & Exit",
                                 command=lambda: self.convertParams(people_entry, angle_entry, recognize_entry, pdecrease_entry, ttime_entry, pCollisionEntry, initialPointsEntry))
        start_button.grid(row=5, columnspan=2)

        self.popup.mainloop()

    def convertParams(self, people_entry, angle_entry, recognize_entry, pDecrease_entry, ttime_entry, pCollisionEntry, initialPointsEntry):
        num_people = int(people_entry.get())
        angle_sun = float(angle_entry.get())
        recognize_points = float(recognize_entry.get())
        decrease_points = float(pDecrease_entry.get())
        totalTime = int(ttime_entry.get())
        pointsDeductedForCollision = float(pCollisionEntry.get())
        initialPoints = float(initialPointsEntry.get())
        finishGui(num_people, angle_sun, recognize_points, decrease_points, totalTime, pointsDeductedForCollision, initialPoints)  # send values to different class - we want it to be json
        self.popup.destroy()  # Close the popup window


if __name__ == '__main__':
    Gui()
