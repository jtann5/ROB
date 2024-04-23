import tkinter as tk
from PIL import Image, ImageTk

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
            square = tk.Label(self.square_frame, bg="white", width=15, height=8)
            square.pack(side="left", padx=5, pady=5)
            self.squares.append(square)

        # Create a clear button to clear all the squares
        clear_button = tk.Button(self.master, text="Clear", command=self.clear_command)
        clear_button.pack(side="bottom")

    def icon_command(self, i):
        print(f"Icon {i+1} pressed!")
        # Move the icon to the first available square
        for square in self.squares:
            if not square.cget("text"):  # Check if the square is empty
                square.config(text=f"Icon {i+1}")
                break

    def options_command(self, event):
        print("Options icon pressed!")

    def clear_command(self):
        print("Clear button pressed!")
        # Clear all the squares
        for square in self.squares:
            square.config(text="")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
