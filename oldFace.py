import tkinter as tk
import threading
import time
import random
import multiprocessing

class RobotFace(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Robot Face")
        self.geometry("800x480")
        self.overrideredirect(True)
        self.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(self, width=800, height=480, bg="white")
        self.canvas.pack()

        # Initialize eye coordinates
        self.lefteyeX = 220
        self.lefteyeY = 180
        self.righteyeX = 580
        self.righteyeY = 180
        self.eye_movement_offset = 40
        self.eye_shift_offset = 10
        self.eye_left = self.create_cartoonish_eye(self.lefteyeX, self.lefteyeY)
        self.eye_right = self.create_cartoonish_eye(self.righteyeX, self.righteyeY)

        self.mouth_coords = [280, 400, 520, 400]
        self.mouth_line = self.canvas.create_line(*self.mouth_coords, fill="black", width=2)


        # Initialize robot state
        self.robot_state = "idle"

        # Start a thread for animations
        self.animation_thread = threading.Thread(target=self.animate_eyes)
        self.animation_thread.start()

        self.bind("<KeyPress-a>", self.set_moving_state)
        self.bind("<KeyPress-s>", self.set_talking_state)
        self.bind("<KeyPress-d>", self.set_idle_state)

    def create_cartoonish_eye(self, x, y):
        eye_outside_offset = 160
        pupil_size_offset = 60
        self.pupil_size_offset = pupil_size_offset
        self.eye_outside_offset = eye_outside_offset
        eye_outer = self.canvas.create_oval(x - eye_outside_offset, y - eye_outside_offset, x + eye_outside_offset, y + eye_outside_offset, fill="white", outline="black", width=2)
        pupil = self.canvas.create_oval(x - pupil_size_offset, y - pupil_size_offset, x + pupil_size_offset, y + pupil_size_offset, fill="black")
        return eye_outer, pupil

    def animate_eyes(self):
        while True:
            if self.robot_state == "idle":
                self.blink_and_move_eyes()
            elif self.robot_state == "talking":
                self.talk_animation()
            elif self.robot_state == "moving":
                self.move_animation()
            time.sleep(0.1)  # Adjust the sleep duration for desired animation speed

    def set_moving_state(self, event):
        self.set_robot_state("moving")

    def set_talking_state(self, event):
        self.canvas.config(bg="white")
        self.reset_face()
        self.set_robot_state("talking")

    def set_idle_state(self, event):
        self.canvas.config(bg="white")
        self.reset_face()
        self.set_robot_state("idle")

    def blink_and_move_eyes(self):
        self.blink()
        time.sleep(0.4)  # Small delay after blinking

        number = random.randint(0, 2)
        if number == 0:
            self.move_left_eye_right()
            self.move_right_eye_right()
        elif number == 1:
            self.move_left_eye_left()
            self.move_right_eye_left()
        elif number == 2:
            self.move_left_eye_center()
            self.move_right_eye_center()
        time.sleep(0.1)

    def animate_mouth(self):
        # Zig-zagging mouth animation
        current_coords = self.mouth_coords
        new_y1 = current_coords[1] + 5 * random.choice([-1, 1])
        new_y2 = current_coords[3] + 5 * random.choice([-1, 1])
        self.mouth_coords = [current_coords[0], new_y1, current_coords[2], new_y2]
        self.canvas.coords(self.mouth_line, *self.mouth_coords)

    def draw_semi_circle(self, x, y, radius, color):
        semi_circle = self.canvas.create_arc(x - radius, y - radius, x + radius, y + radius, start=180, extent=180, fill=color, outline=color, width=2)
        return semi_circle

    def talk_animation(self):
        # self.animate_mouth()
        semi_circle = self.draw_semi_circle((self.mouth_coords[0] + self.mouth_coords[2]) / 2, self.mouth_coords[1], (self.mouth_coords[2] - self.mouth_coords[0]) / 2, "black")
        time.sleep(0.5)
        self.canvas.delete(semi_circle)

    def move_animation(self):
        self.canvas.config(bg="red")  # Change background color to red
        self.angry_eyes()
        time.sleep(.1)  # Adjust the duration for the movement animation

    def angry_eyes(self):
        # Move the eyes upward to give an angry appearance
        number = random.randint(0, 2)
        if number == 0:
            self.move_left_eye_right()
            self.move_right_eye_right()
        elif number == 1:
            self.move_left_eye_left()
            self.move_right_eye_left()
        elif number == 2:
            self.move_left_eye_center()
            self.move_right_eye_center()

    def reset_face(self):
        # Reset the background color and eye positions
        self.canvas.config(bg="white")
        self.canvas.coords(self.eye_left[1], self.lefteyeX - self.pupil_size_offset, self.lefteyeY - self.pupil_size_offset,
                            self.lefteyeX + self.pupil_size_offset, self.lefteyeY + self.pupil_size_offset)
        self.canvas.coords(self.eye_right[1], self.righteyeX - self.pupil_size_offset, self.righteyeY - self.pupil_size_offset,
                            self.righteyeX + self.pupil_size_offset, self.righteyeY + self.pupil_size_offset)

    def blink(self):
        self.canvas.itemconfig(self.eye_left[1], state=tk.HIDDEN)
        self.canvas.itemconfig(self.eye_right[1], state=tk.HIDDEN)
        time.sleep(0.1)
        self.canvas.itemconfig(self.eye_left[1], state=tk.NORMAL)
        self.canvas.itemconfig(self.eye_right[1], state=tk.NORMAL)
        time.sleep(random.uniform(2, 5))  # Randomize blinking intervals

    # Left eyes

    def move_left_eye_right(self):
        new_left_center = [self.lefteyeX + self.eye_movement_offset, self.lefteyeY]  # Adjust the desired center coordinates

        self.move_eye(self.eye_left, new_left_center)

    def move_left_eye_left(self):
        new_left_center = [self.lefteyeX - self.eye_movement_offset, self.lefteyeY]  # Adjust the desired center coordinates

        self.move_eye(self.eye_left, new_left_center)

    def move_left_eye_center(self):
        new_left_center = [self.lefteyeX, self.lefteyeY]

        self.move_eye(self.eye_left, new_left_center)

    def move_left_eye_up(self):
        new_left_center = [self.lefteyeX, self.lefteyeY - self.eye_movement_offset]

        self.move_eye(self.eye_left, new_left_center)

    def move_left_eye_down(self):
        new_left_center = [self.lefteyeX, self.lefteyeY + self.eye_movement_offset]

        self.move_eye(self.eye_left, new_left_center)

    # Right Eyes

    def move_right_eye_right(self):
        new_right_center = [self.righteyeX + self.eye_movement_offset, self.righteyeY]  # Adjust the desired center coordinates

        self.move_eye(self.eye_right, new_right_center)

    def move_right_eye_left(self):
        new_right_center = [self.righteyeX - self.eye_movement_offset, self.righteyeY]  # Adjust the desired center coordinates

        self.move_eye(self.eye_right, new_right_center)

    def move_right_eye_center(self):
        new_right_center = [self.righteyeX, self.righteyeY]

        self.move_eye(self.eye_right, new_right_center)

    def move_right_eye_up(self):
        new_right_center = [self.righteyeX, self.righteyeY - self.eye_movement_offset]

        self.move_eye(self.eye_right, new_right_center)

    def move_right_eye_down(self):
        new_right_center = [self.righteyeX, self.righteyeY + self.eye_movement_offset]

        self.move_eye(self.eye_right, new_right_center)



    def move_eye(self, eye, new_center):
        # Calculate the new bounding box coordinates based on the desired center
        x1, y1, x2, y2 = new_center[0] - self.pupil_size_offset, new_center[1] - self.pupil_size_offset, new_center[0] + self.pupil_size_offset, new_center[1] + self.pupil_size_offset
        self.canvas.coords(eye[1], x1, y1, x2, y2)

    def set_robot_state(self, new_state):
        self.robot_state = new_state

def run_robot_face():
    robot_face = RobotFace()
    robot_face.mainloop()

if __name__ == "__main__":
    robot_process = multiprocessing.Process(target=run_robot_face)
    robot_process.start()