import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from rob import rob

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

        ## ...
        ## make the rest of them

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
        print("I am listenign blahdlajsf lsj")

    def bodyturn(self):
        # send value to rob
        print("robs body is turning")

    def headturn(self):
        # send pan value to rob
        print("robs head is turning")

    def headtilt(self):
        # send tilt to rob
        print("Robs head is tilting")

    def robotturn(self):
        print("Rob is turning")

    def movement(self):
        # this is where we send that stuff to rob
        print("There is movement")

## icon instructions as follows
## 0 Motors
## 1 HEADTILT
## 2 HEADTURN
## 3 BODYTURN
## 4 PAUSE
## 5 ROBOTTURN
## 6 TALKING includes waiting for human speed input, type sentence and 4 prebuilt sayings

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


execution_instructions = []

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.icon_images = []  # Initialize icon_images attribute
        self.create_widgets()

        self.icon_options = {
            "icon1": ["Option1", "Option2", "Option3", "Option4"],
            "icon2": ["Option1", "Option2", "Option3"],
            "icon3": ["Option1", "Option2", "Option3"],
            "icon4": ["Option1", "Option2", "Option3"],
            "icon5": ["Option1", "Option2", "Option3"],
            "icon6": ["Option1", "Option2", "Option3"],
            "icon7": ["Option1", "Option2", "Option3"]
        }

    def create_widgets(self):
        # Create the 7 icons on the right side of the screen
        self.icon_frame = tk.Frame(self.master)
        self.icon_frame.pack(side="left", fill="y")

        for i in range(7):
            # Load the icon image
            image = Image.open(f"icon{i+1}.png")
            image_dim = (60, 60)
            photo = ImageTk.PhotoImage(image.resize(image_dim))  # Resize the icon image

            self.icon_images.append(photo)

            icon_label = tk.Label(self.icon_frame, image=photo, width=image_dim[0]+15, height=image_dim[1])
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
            icon_width = image_dim[0]+15
            options_width = 20
            x_coord = icon_width - options_width
            y_coord = image_dim[1] - options_width

            options_label.place(in_=icon_label, x=x_coord, y=y_coord)

            # Bind the left mouse button click event to the options icon
            options_label.bind("<Button-1>", self.options_command)

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
        clear_button = tk.Button(self.master, text="Clear", command=self.clear_command, width=10, height=3)
        clear_button.pack(side="right", padx=5)

        run_button = tk.Button(self.master, text="Run", command=self.run_command, width=10, height=3)
        run_button.pack(side="bottom", padx=5)

        self.square_frame.pack(side="top", expand=True, fill="both")

    def run_command(self):
        # this is where I go through the stuff and execute things
        for i in range(len(execution_instructions)):
            if execution_instructions[i] == "movement":
                icon_instructions[i].movement(icon_instructions[i])
            elif execution_instructions[i] == "robotturn":
                icon_instructions[i].robotturn(icon_instructions[i])
            elif execution_instructions[i] == "headtilt":
                icon_instructions[i].headtilt(icon_instructions[i])
            elif execution_instructions[i] == "headturn":
                icon_instructions[i].headturn(icon_instructions[i])
            elif execution_instructions[i] == "bodyturn":
                icon_instructions[i].bodyturn(icon_instructions[i])
            elif execution_instructions[i] == "humanspeech":
                icon_instructions[i].humanspeech(icon_instructions[i])
            elif execution_instructions[i] == "talk":
                icon_instructions[i].talk(icon_instructions[i])
            else:
                print("Invalid")
        rob.defaults()

    def icon_command(self, i):
        print(f"Icon {i+1} pressed!")
        # Move the icon to the first available square
        for square in self.squares:
            if not square.cget("image"):  # Check if the square is empty
                square.config(image=self.icon_images[i], width=80, height=80)
                execution_instructions.append(icon_description[i])
                icon_instructions.append(BlockInstruction)
                print(execution_instructions)
                break

    def options_command(self, event):
        print("Options icon pressed!")

    def clear_command(self):
        print("Clear button pressed!")
        # Clear all the squares
        print(execution_instructions)
        execution_instructions.clear()
        print(execution_instructions)
        for square in self.squares:
            square.config(image='', width=11, height=5)


class OptionsPopup(tk.Toplevel):
    def __init__(self, parent, icon_name, options):
        super().__init__(parent)
        self.parent = parent
        self.icon_name = icon_name
        self.options = options
        self.selected_option = tk.StringVar()
        self.selected_option.set(options[0] if options else "")

        self.title(f"Options for {self.icon_name}")
        self.geometry("200x150")

        label = ttk.Label(self, text=f"Options for {self.icon_name}")
        label.pack(pady=10)

        options_menu = ttk.OptionMenu(self, self.selected_option, *options)
        options_menu.pack(pady=5)

        apply_button = ttk.Button(self, text="Apply", command=self.apply_options)
        apply_button.pack(pady=5)

    def apply_options(self):
        selected_option = self.selected_option.get()
        print(f"Selected option for {self.icon_name}: {selected_option}")
        # Add your logic to apply the selected option


root = tk.Tk()
app = Application(master=root)
app.mainloop()
