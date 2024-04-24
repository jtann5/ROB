import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from rob import rob
import time
import functools
import copy

class BlockInstruction:
    def __init__(self):
        self.distance = 0
        self.speed = 0
        self.angle = 0
        self.direction = "forward"
        self.turn_direction = "right"
        self.turn_time = 0
        self.left = 6000
        self.right = 6000

        self.waist_value = 6000
        self.head_pan_value = 6000
        self.head_tilt_value = 6000

        self.talking = False
        self.input = "Im ROB"

    def reset(self):
        self.distance = 0
        self.speed = 0
        self.angle = 0
        self.direction = "forward"
        self.turn_direction = "right"
        self.turn_time = 0
        self.left = 6000
        self.right = 6000

        self.waist_value = 6000
        self.head_pan_value = 6000
        self.head_tilt_value = 6000

        self.talking = False
        self.input = "Im ROB"

    def set_movement(self, speed, distance, direction):
        self.speed = speed
        self.distance = distance
        self.direction = direction

    def set_turn(self, direction, seconds):
        self.turn_direction = direction
        self.turn_time = seconds

    def set_headtilt(self, head_tilt_val):
        self.head_tilt_value = head_tilt_val

    def set_headturn(self, head_pan_val):
        self.head_pan_value = head_pan_val

    def set_bodyturn(self, body_pan_val):
        self.waist_value = body_pan_val

    def set_text(self, input):
        self.input = input

    def talk(self):
        ## TODO RIGHT HERE
        print("rob is talking")

    def humanspeech(self):
        ## TODO RIGHT HERE
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
        ## TODO RIGHT HERE
        print("rob is turning")

    def movement(self):
        ## TODO RIGHT HERE
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
        self.index_value = 0

    def create_widgets(self):
        # Create the 7 icons on the right side of the screen
        self.icon_frame = tk.Frame(self.master)
        self.icon_frame.pack(side="left", fill="y")
        default_BlockInstructions.append(BlockInstruction())
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

        self.execution_label = tk.Label(self.master, text="No function executing", bg="red", fg="white")
        self.execution_label.pack(side="top", fill="x", pady=5)

        self.total_execution_label = tk.Label(self.master, text="Program not executing", bg="red", fg="white")
        self.total_execution_label.pack(side="top", fill="x")

        button_frame = tk.Frame(self.master)
        button_frame.pack(side="bottom", padx=10, pady=10, anchor="se")

        exit_button = tk.Button(button_frame, text="Exit", command=self.master.destroy, width=10, height=3)
        exit_button.pack(side="right", padx=5)

        clear_button = tk.Button(button_frame, text="Clear Last", command=self.clear_previous, width=10, height=3)
        clear_button.pack(side="right", padx=5)

        clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_command, width=10, height=3)
        clear_button.pack(side="right", padx=5)

        run_button = tk.Button(button_frame, text="Run", command=self.run_command, width=10, height=3)
        run_button.pack(side="right", padx=5)

        self.square_frame.pack(side="top", expand=True, fill="both")

    def run_command(self):
        # this is where I go through the stuff and execute things
        self.total_execution_label.config(text="Program Executing", bg="blue")
        for i in range(len(execution_instructions)):
            self.execution_label.config(text=f"Executing: {execution_instructions[i]}", bg="blue")

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
            self.execution_label.config(text=f"{execution_instructions[i]} completed", bg="green")
            self.master.update()
            time.sleep(2)
        self.total_execution_label.config(text="Finished Executing", bg="green")
        rob.defaults()

    def icon_command(self, i):
        print(f"Icon {i + 1} pressed!")
        # Move the icon to the first available square
        for square_index, square in enumerate(self.squares):
            if not square.cget("image"):  # Check if the square is empty
                square.config(width=80, height=80)

                square.config(image=self.icon_images[i])

                def call_options_command(event, idx=i, sq_idx=square_index):
                    self.options_command_not_default(idx, sq_idx)

                # Bind the function to the squarez
                square.bind("<Button-1>", call_options_command)

                execution_instructions.append(icon_description[i])
                self.index_value += 1
                icon_instructions.append(copy.deepcopy(default_BlockInstructions[0]))
                print(execution_instructions)
                if self.index_value > 8:
                    self.index_value = 8
                break

    def options_command_not_default(self, icon_num, box_num):
        print(icon_num)
        print(f"This is the box number {box_num}")
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title(f"{icon_title[icon_num]} Settings")
        self.settings_window.geometry("500x310")
        if icon_description[icon_num].__eq__("movement"):
            initialSpeed = icon_instructions[box_num].speed
            initialDistance = icon_instructions[box_num].distance
            initialDirection = icon_instructions[box_num].direction

            self.speed_slider = tk.Scale(self.settings_window, from_=0, to=100, orient="horizontal", label="Speed %")
            self.speed_slider.set(initialSpeed)
            self.speed_slider.config(length=400)
            self.speed_slider.pack(pady=10)

            self.distance_slider = tk.Scale(self.settings_window, from_=0, to=100, orient="horizontal",
                                            label="Distance (cm):")
            self.distance_slider.set(initialDistance)
            self.distance_slider.config(length=400)
            self.distance_slider.pack(pady=10)

            direction_option = ["forward", "backward"]
            self.direction_fb = tk.StringVar(self.settings_window)
            self.direction_fb.set(initialDirection)
            direction_label = tk.Label(self.settings_window, text="Direction:")
            direction_label.pack(pady=10)
            self.direction_menu = tk.OptionMenu(self.settings_window, self.direction_fb, *direction_option)
            self.direction_menu.pack(pady=10)

            apply_button = tk.Button(self.settings_window, text="Apply", command=lambda: self.apply_movement_settings(box_num))
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("robotturn"):
            initialTime = icon_instructions[box_num].turn_time
            self.turntime_slider = tk.Scale(self.settings_window, from_=0, to=50, orient="horizontal", label="Seconds")
            self.turntime_slider.set(initialTime)
            self.turntime_slider.config(length=400)
            self.turntime_slider.pack(pady=10)
            direction_options = ["left", "right"]
            self.direction_var = tk.StringVar(self.settings_window)
            self.direction_var.set(icon_instructions[box_num].turn_direction)
            direction_label = tk.Label(self.settings_window, text="Direction:")
            direction_label.pack(pady=10)
            self.direction_menu = tk.OptionMenu(self.settings_window, self.direction_var, *direction_options)
            self.direction_menu.pack(pady=10)
            apply_button = tk.Button(self.settings_window, text="Apply", command=lambda: self.apply_turn_settings(box_num))
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("headtilt"):
            initialValue = icon_instructions[box_num].head_tilt_value
            self.headtilt_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
            self.headtilt_slider.set(initialValue)
            self.headtilt_slider.config(length=400)
            self.headtilt_slider.pack(pady=10)
            apply_button = tk.Button(self.settings_window, text="Apply", command=lambda: self.apply_headtilt_settings(box_num))
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("headturn"):
            initialValue = icon_instructions[box_num].head_pan_value
            self.headturn_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
            self.headturn_slider.set(initialValue)
            self.headturn_slider.config(length=400)
            self.headturn_slider.pack(pady=10)
            apply_button = tk.Button(self.settings_window, text="Apply", command=lambda: self.apply_headturn_settings(box_num))
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("bodyturn"):
            initialValue = icon_instructions[box_num].waist_value
            self.waist_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
            self.waist_slider.set(initialValue)
            self.waist_slider.config(length=400)
            self.waist_slider.pack(pady=10)
            apply_button = tk.Button(self.settings_window, text="Apply", command=lambda: self.apply_waist_settings(box_num))
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("humanspeech"):
            option_label = tk.Label(self.settings_window, text="No options for this action!")
            option_label.pack(pady=10)
            exit_button = tk.Button(self.settings_window, text="Exit", command=self.settings_window.destroy)
            exit_button.config(width=15)
            exit_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("talk"):
            option_label = tk.Label(self.settings_window, text="Type output or select output!")
            option_label.pack(pady=10)
            self.text_input = tk.Entry(self.settings_window)
            self.text_input.pack(pady=10)

            # Option menu for choosing from predefined options
            options = ["Im ROB", "Kill all humans", "I support human genocide", "Dont make me mad", "Hello human slave"]
            self.predefined_option_var = tk.StringVar(self.settings_window)
            self.predefined_option_var.set(icon_instructions[box_num].input)  # Set default option
            option_label = tk.Label(self.settings_window, text="Predefined Options:")
            option_label.pack(pady=10)
            self.option_menu = tk.OptionMenu(self.settings_window, self.predefined_option_var, *options)
            self.option_menu.pack(pady=10)

            apply_button = tk.Button(self.settings_window, text="Apply", command=lambda: self.apply_talk_settings(box_num))
            apply_button.config(width=15)
            apply_button.pack(pady=10)

    def options_command(self, icon_num, default=None, box_num=None):
        print(icon_num)
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title(f"{icon_title[icon_num]} Settings")
        self.settings_window.geometry("500x310")
        if icon_description[icon_num].__eq__("movement"):
            initialSpeed = default_BlockInstructions[0].speed
            initialDistance = default_BlockInstructions[0].distance
            initialDirection = default_BlockInstructions[0].direction

            self.speed_slider = tk.Scale(self.settings_window, from_=0, to=100, orient="horizontal", label="Speed %")
            self.speed_slider.set(initialSpeed)
            self.speed_slider.config(length=400)
            self.speed_slider.pack(pady=10)

            self.distance_slider = tk.Scale(self.settings_window, from_=0, to=100, orient="horizontal", label="Distance (cm):")
            self.distance_slider.set(initialDistance)
            self.distance_slider.config(length=400)
            self.distance_slider.pack(pady=10)

            direction_option = ["forward", "backward"]
            self.direction_fb = tk.StringVar(self.settings_window)
            self.direction_fb.set(initialDirection)
            direction_label = tk.Label(self.settings_window, text="Direction:")
            direction_label.pack(pady=10)
            self.direction_menu = tk.OptionMenu(self.settings_window, self.direction_fb, *direction_option)
            self.direction_menu.pack(pady=10)

            apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_movement_settings_default)
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("robotturn"):
            initialTime = default_BlockInstructions[0].turn_time
            self.turntime_slider = tk.Scale(self.settings_window, from_=0, to=50, orient="horizontal", label="Seconds")
            self.turntime_slider.set(initialTime)
            self.turntime_slider.config(length=400)
            self.turntime_slider.pack(pady=10)
            direction_options = ["left", "right"]
            self.direction_var = tk.StringVar(self.settings_window)
            self.direction_var.set(default_BlockInstructions[0].turn_direction)
            direction_label = tk.Label(self.settings_window, text="Direction:")
            direction_label.pack(pady=10)
            self.direction_menu = tk.OptionMenu(self.settings_window, self.direction_var, *direction_options)
            self.direction_menu.pack(pady=10)
            apply_button = tk.Button(self.settings_window, text="Apply",command=self.apply_turn_settings_default)
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("headtilt"):
            initialValue = default_BlockInstructions[0].head_tilt_value
            self.headtilt_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
            self.headtilt_slider.set(initialValue)
            self.headtilt_slider.config(length=400)
            self.headtilt_slider.pack(pady=10)
            apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_headtilt_settings_default)
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("headturn"):
            initialValue = default_BlockInstructions[0].head_pan_value
            self.headturn_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
            self.headturn_slider.set(initialValue)
            self.headturn_slider.config(length=400)
            self.headturn_slider.pack(pady=10)
            apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_headturn_settings_default)
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("bodyturn"):
            initialValue = default_BlockInstructions[0].waist_value
            self.waist_slider = tk.Scale(self.settings_window, from_=4000, to=8000, orient="horizontal")
            self.waist_slider.set(initialValue)
            self.waist_slider.config(length=400)
            self.waist_slider.pack(pady=10)
            apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_waist_settings_default)
            apply_button.config(width=15)
            apply_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("humanspeech"):
            option_label = tk.Label(self.settings_window, text="No options for this action!")
            option_label.pack(pady=10)
            exit_button = tk.Button(self.settings_window, text="Exit", command=self.settings_window.destroy)
            exit_button.config(width=15)
            exit_button.pack(pady=10)
        elif icon_description[icon_num].__eq__("talk"):
            option_label = tk.Label(self.settings_window, text="Type output or select output!")
            option_label.pack(pady=10)
            self.text_input = tk.Entry(self.settings_window)
            self.text_input.pack(pady=10)

            # Option menu for choosing from predefined options
            options = ["Im ROB", "Kill all humans", "I support human genocide", "Dont make me mad", "Hello human slave"]
            self.predefined_option_var = tk.StringVar(self.settings_window)
            self.predefined_option_var.set(default_BlockInstructions[0].input)  # Set default option
            option_label = tk.Label(self.settings_window, text="Predefined Options:")
            option_label.pack(pady=10)
            self.option_menu = tk.OptionMenu(self.settings_window, self.predefined_option_var, *options)
            self.option_menu.pack(pady=10)

            apply_button = tk.Button(self.settings_window, text="Apply", command=self.apply_talk_settings_default)
            apply_button.config(width=15)
            apply_button.pack(pady=10)

    def apply_movement_settings(self, box_num):
        speed = self.speed_slider.get()
        distance = self.distance_slider.get()
        direction = self.direction_fb.get()
        icon_instructions[box_num].set_movement(speed, distance, direction)
        self.settings_window.destroy()

    def apply_talk_settings(self, box_num):
        text_input = self.text_input.get()
        if text_input:
            icon_instructions[box_num].set_text(text_input)
        else:
            selected_option = self.predefined_option_var.get()
            icon_instructions[box_num].set_text(selected_option)
        self.settings_window.destroy()

    def apply_headtilt_settings(self, box_num):
        headtilt_value = self.headtilt_slider.get()
        icon_instructions[box_num].set_headtilt(headtilt_value)
        self.settings_window.destroy()

    def apply_headturn_settings(self, box_num):
        headturn_value = self.headturn_slider.get()
        icon_instructions[box_num].set_headturn(headturn_value)
        self.settings_window.destroy()

    def apply_waist_settings(self, box_num):
        waist_value = self.waist_slider.get()
        icon_instructions[box_num].set_bodyturn(waist_value)
        self.settings_window.destroy()

    def apply_turn_settings(self, box_num):
        direction = self.direction_var.get()
        seconds = self.turntime_slider.get()
        print(direction)
        icon_instructions[box_num].set_turn(direction, seconds)
        self.settings_window.destroy()

    def apply_talk_settings_default(self):
        text_input = self.text_input.get()
        if text_input:
            default_BlockInstructions[0].set_text(text_input)
        else:
            selected_option = self.predefined_option_var.get()
            default_BlockInstructions[0].set_text(selected_option)
        self.settings_window.destroy()

    def apply_movement_settings_default(self):
        speed = self.speed_slider.get()
        distance = self.distance_slider.get()
        direction = self.direction_fb.get()
        default_BlockInstructions[0].set_movement(speed, distance, direction)
        self.settings_window.destroy()

    def apply_headtilt_settings_default(self):
        headtilt_value = self.headtilt_slider.get()
        default_BlockInstructions[0].set_headtilt(headtilt_value)
        self.settings_window.destroy()

    def apply_headturn_settings_default(self):
        headturn_value = self.headturn_slider.get()
        default_BlockInstructions[0].set_headturn(headturn_value)
        self.settings_window.destroy()

    def apply_waist_settings_default(self):
        waist_value = self.waist_slider.get()
        default_BlockInstructions[0].set_bodyturn(waist_value)
        self.settings_window.destroy()

    def apply_turn_settings_default(self):
        direction = self.direction_var.get()
        seconds = self.turntime_slider.get()
        print(direction)
        default_BlockInstructions[0].set_turn(direction, seconds)
        self.settings_window.destroy()

    def clear_command(self):
        print("Clear button pressed!")
        # Clear all the squares
        print(execution_instructions)
        execution_instructions.clear()
        print(execution_instructions)
        for index, square in enumerate(self.squares):
            square.config(image='', width=11, height=5)
            square.unbind("<Button-1>")
            if index < self.index_value:
                icon_instructions[index].reset()
        self.index_value = 0
        self.execution_label.config(text="No function executing", bg="red")
        self.total_execution_label.config(text="Program changed and not running", bg="red")

    def clear_previous(self):
        print("Cleared last command")
        if len(execution_instructions) > 0:
            square = self.squares[self.index_value-1]
            square.config(image='', width=11, height=5)
            icon_instructions[self.index_value-1].reset()
            execution_instructions.pop()
            self.index_value -= 1
            print(execution_instructions)
            square.unbind("<Button-1>")
            self.execution_label.config(text="No function executing", bg="red")
            self.total_execution_label.config(text="Program changed and not running", bg="red")
        else:
            print("Nothing to pop!")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
