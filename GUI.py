import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from rob import rob
import time

class BlockInstruction:
    def __init__(self):
        self.distance = 0
        self.speed = 0
        self.angle = 0
        self.direction = ""
        self.both_motors = False
        self.left = 6000
        self.right = 6000

        self.waist_value = 6000
        self.head_pan_value = 6000
        self.head_tilt_value = 6000

        self.wait_time = 0

        self.wait_human_speech = False
        self.talking = False
        self.input = ""

    def set_movement(self, distance, speed, angle, direction, both_motors, left, right):
        pass

    def set_headtilt(self, head_tilt_val):
        self.head_tilt_value = head_tilt_val

    def set_headturn(self, head_pan_val):
        self.head_pan_value = head_pan_val

    def set_bodyturn(self, body_pan_val):
        self.waist_value = body_pan_val

    def set_talking(self, talking_val, input):
        self.talking = talking_val
        self.input = input

    def talk(self):
        print("rob is talking")

    def humanspeech(self):
        print("I am listening")

    def bodyturn(self):
        # send value to rob
        print(f"waist is moving {self.waist_value}")
        rob.setMotor(2, self.waist_value)

    def headturn(self):
        # send pan value to rob
        print(f"rob's head is turning {self.head_pan_value}")
        rob.setMotor(4, self.head_pan_value)

    def headtilt(self):
        # send tilt to rob
        print(f"rob's head is tilting {self.head_tilt_value}")
        rob.setMotor(3, self.head_tilt_value)

    def robotturn(self):
        print("rob is turning")

    def movement(self):
        # this is where we send that stuff to rob
        print("There is movement")


icon_instructions = []

icon_description = [
    "movement",
    "robotturn",
    "headtilt",
    "headturn",
    "bodyturn",
    "humanspeech",
    "talk"
]

icon_title = [
    "Robot Movement",
    "Robot Turn",
    "Robot Head Tilt",
    "Robot Head Turn",
    "Robot Waist Turn",
    "Wait for Human Speech",
    "Robot Talking"
]

default_BlockInstructions = []

execution_instructions = []


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.icon_images = []  # Initialize icon_images attribute
        self.create_widgets()

    def create_widgets(self):
        # Create the 7 icons on the right side of the screen
        self.icon_frame = tk.Frame(self.master)
        self.icon_frame.pack(side="left", fill="y")

        for i in range(7):
            # Load the icon image
            image = Image.open(f"icon{i + 1}.png")
            image_dim = (60, 60)
            photo = ImageTk.PhotoImage(image.resize(image_dim))  # Resize the icon image

            self.icon_images.append(photo)

            icon_label = tk.Label(self.icon_frame, image=photo, width=image_dim[0] + 15, height=image_dim[1])
            icon_label.image = photo  # Keep a reference to the image object to prevent it from being garbage collected
            icon_label.pack(side="top", fill="x")

            # Bind the left mouse button click event to the icon
            icon_label.bind("<Button-1>", lambda event, i=i: self.icon_command(i))

            # Add an options icon to the top-right corner of each icon
            options_icon = Image.open("options_icon.png")
            options_icon = options_icon.resize((20, 20))  # Resize the options icon
            options_photo = ImageTk.PhotoImage(options_icon)

            options_label = tk.Label(self.icon_frame, image=options_photo, width=20, height=20)
            options_label.image = options_photo
            default_BlockInstructions.append(BlockInstruction())

            # Calculate the coordinates to position the options icon label at the top-right corner of the icon label
            icon_width = image_dim[0] + 15
            options_width = 20
            x_coord = icon_width - options_width
            y_coord = image_dim[1] - options_width

            options_label.place(in_=icon_label, x=x_coord, y=y_coord)

            # Bind the left mouse button click event to the options icon
            options_label.bind("<Button-1>", lambda event, i=i: self.options_command(i))

        # Create the 8 execution squares in the center of the screen
        self.square_frame = tk.Frame(self.master)
        self.square_frame.pack(side="right", expand=True, fill="both")

        self.squares = []
        for i in range(8):
            square = tk.Label(self.square_frame, bg="white", width=11, height=5)
            square.pack(side="left", padx=5, pady=5)
            self.squares.append(square)

        button_frame = tk.Frame(self.master)
        button_frame.pack(side="bottom", padx=10, pady=10, anchor="se")

        # Create a clear button to clear all the squares
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_command, width=10, height=3)
        clear_button.pack(side="right", padx=5)

        run_button = tk.Button(button_frame, text="Run", command=self.run_command, width=10, height=3)
        run_button.pack(side="right", padx=5)

        self.square_frame.pack(side="top", expand=True, fill="both")

    def run_command(self):
        # this is where I go through the stuff and execute things
        for i in range(len(execution_instructions)):
            if execution_instructions[i] == "movement":
                icon_instructions[i].movement()
            elif execution_instructions[i] == "robotturn":
                icon_instructions[i].robotturn()
            elif execution_instructions[i] == "headtilt":
                icon_instructions[i].headtilt()
            elif execution_instructions[i] == "headturn":
                icon_instructions[i].headturn()
            elif execution_instructions[i] == "bodyturn":
                icon_instructions[i].bodyturn()
            elif execution_instructions[i] == "humanspeech":
                icon_instructions[i].humanspeech()
            elif execution_instructions[i] == "talk":
                icon_instructions[i].talk()
            else:
                print("Invalid")
            time.sleep(2)
        rob.defaults()

    def icon_command(self, i):
        print(f"Icon {i + 1} pressed!")
        # Move the icon to the first available square
        for square in self.squares:
            if not square.cget("image"):  # Check if the square is empty
                square.config(image=self.icon_images[i], width=80, height=80)
                execution_instructions.append(icon_description[i])
                icon_instructions.append(default_BlockInstructions[i])
                print(execution_instructions)
                break

    def options_command(self, icon_num, default=None):
        print(icon_num)
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title(f"{icon_title[icon_num]} Settings")
        if default is not None:
            pass
        else:
            if icon_description[icon_num].__eq__("movement"):
                ## TODO movement
                pass
            elif icon_description[icon_num].__eq__("robotturn"):
                ## TODO robotturn
                pass
            elif icon_description[icon_num].__eq__("headtilt"):
                initialValue = default_BlockInstructions[icon_num].head_pan_value
                self.headtilt_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
                self.headtilt_slider.set(initialValue)
                self.headtilt_slider.pack()
                apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_headtilt_settings_default)
                apply_button.pack()
            elif icon_description[icon_num].__eq__("headturn"):
                initialValue = default_BlockInstructions[icon_num].head_pan_value
                self.headturn_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
                self.headturn_slider.set(initialValue)
                self.headturn_slider.pack()
                apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_headturn_settings_default)
                apply_button.pack()
            elif icon_description[icon_num].__eq__("bodyturn"):
                initialValue = default_BlockInstructions[icon_num].waist_value
                self.waist_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
                self.waist_slider.set(initialValue)
                self.waist_slider.pack()
                apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_waist_settings_default)
                apply_button.pack()
            elif icon_description[icon_num].__eq__("humanspeech"):
                ## TODO humanspeech
                pass
            elif icon_description[icon_num].__eq__("talk"):
                ## TODO talk
                pass

    def apply_headtilt_settings_default(self):
        headtilt_value = self.headtilt_slider.get()
        default_BlockInstructions[2].set_headtilt(headtilt_value)
        self.settings_window.destroy()

    def apply_headturn_settings_default(self):
        headturn_value = self.headturn_slider.get()
        default_BlockInstructions[3].set_headturn(headturn_value)
        self.settings_window.destroy()

    def apply_waist_settings_default(self):
        waist_value = self.waist_slider.get()
        default_BlockInstructions[4].set_bodyturn(waist_value)
        self.settings_window.destroy()

    def clear_command(self):
        print("Clear button pressed!")
        # Clear all the squares
        print(execution_instructions)
        execution_instructions.clear()
        print(execution_instructions)
        for square in self.squares:
            square.config(image='', width=11, height=5)



root = tk.Tk()
app = Application(master=root)
app.mainloop()
