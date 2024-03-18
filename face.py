import time
import random
import os

#pygame version
import pygame

class RobotFace:
    def __init__(self, queue=None):
        self.screen_width = 1024
        self.queue = queue

        self.clock = pygame.time.Clock()
        self.next_blink_time = pygame.time.get_ticks() + random.randint(2000, 7000)
        self.end_blink_time = 0
        self.blinking = False

        self.lefteyeX = 282
        self.lefteyeY = 270
        self.righteyeX = 742
        self.righteyeY = 270
        self.lefteye_pupilX = self.lefteyeX
        self.lefteye_pupilY = self.lefteyeY
        self.righteye_pupilX = self.righteyeX
        self.righteye_pupilY = self.righteyeY

        self.eye_shift_offset = 40
        self.eye_color = (0, 0, 0)


        self.mouth_size = 256
        self.mouth_height = 525
        self.mouthfirstcoord = (self.screen_width / 2) + (self.mouth_size / 2)
        self.mouthsecondcoord = self.mouthfirstcoord - self.mouth_size
        self.mouth_coords = [self.mouthsecondcoord, self.mouth_height, self.mouthfirstcoord, self.mouth_height]


        self.robot_state = "idle"

    def initialize_pygame(self):
        if not os.getenv('PYGAME_INITIALIZED'):
            pygame.init()
            os.environ['PYGAME_INITIALIZED'] = '1'
        self.screen = pygame.display.set_mode((1024, 600))
        pygame.display.set_caption("ROBs Face")

    def draw_eye(self, x, y, pupilX, pupilY):
        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 162) # eye outline
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 160) #white part
        pygame.draw.circle(self.screen, self.eye_color, (pupilX, pupilY), 60) #pupil

    def blink(self):
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_blink_time:
            self.blinking = True  # start blinking
            self.end_blink_time = current_time + 500  # schedule end of blink
            self.next_blink_time = current_time + random.randint(2000, 7000)  # schedule next blink
        elif current_time >= self.end_blink_time:
            self.blinking = False  # stop blinking

    def animate_eyes(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((255, 255, 255))
            if self.queue is not None:
                if not self.queue.empty():
                    new_state = self.queue.get()
                    self.robot_state = new_state

            if self.robot_state != None:
                self.draw_mouth()
                self.eye_color = (255, 255, 255) if self.blinking else (0, 0, 0)
                self.draw_eye(self.lefteyeX, self.lefteyeY, self.lefteye_pupilX, self.lefteye_pupilY)
                self.draw_eye(self.righteyeX, self.righteyeY, self.righteye_pupilX, self.righteye_pupilY)
                self.blink()
                temp = random.randint(0, 70)
                if temp == 0:
                    self.move_eyes()

            pygame.display.update()
            self.clock.tick(60)

    def move_eyes(self):
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

    def move_left_eye_right(self):
        self.lefteye_pupilX = self.lefteyeX + self.eye_shift_offset

    def move_left_eye_left(self):
        self.lefteye_pupilX = self.lefteyeX - self.eye_shift_offset

    def move_left_eye_center(self):
        self.lefteye_pupilX = self.lefteyeX
        self.lefteye_pupilY = self.lefteyeY

    def move_left_eye_up(self):
        self.lefteye_pupilY = self.lefteyeY - self.eye_shift_offset

    def move_left_eye_down(self):
        self.lefteye_pupilY = self.lefteyeY + self.eye_shift_offset

    def move_right_eye_right(self):
        self.righteye_pupilX = self.righteyeX + self.eye_shift_offset

    def move_right_eye_left(self):
        self.righteye_pupilX = self.righteyeX - self.eye_shift_offset

    def move_right_eye_center(self):
        self.righteye_pupilX = self.righteyeX
        self.righteye_pupilY = self.righteyeY

    def move_right_eye_up(self):
        self.righteye_pupilY = self.righteyeY - self.eye_shift_offset

    def move_right_eye_down(self):
        self.righteye_pupilY = self.righteyeY + self.eye_shift_offset

    def draw_mouth(self):
        if self.robot_state == 'talking':
            if pygame.time.get_ticks() // 500 % 3 == 0:
                pygame.draw.line(self.screen, (0, 0, 0), (self.mouth_coords[0], self.mouth_coords[1]), (self.mouth_coords[2], self.mouth_coords[3]), 2)
            else:
                mouth_surface = pygame.Surface((self.mouth_size, self.mouth_size), pygame.SRCALPHA)
                pygame.draw.ellipse(mouth_surface, (0, 0, 0), pygame.Rect(0, 0, self.mouth_size, self.mouth_size))
                self.screen.blit(mouth_surface, (self.mouthsecondcoord, self.mouth_height), pygame.Rect(0, self.mouth_size/2, self.mouth_size, self.mouth_size/2))
        elif self.robot_state == 'moving':
            pygame.draw.circle(self.screen, (0, 0, 0), (int((self.mouthfirstcoord+(self.screen_width/2))/2), self.mouth_height + 20), int(self.mouth_size // 4))
        else:
            pygame.draw.line(self.screen, (0, 0, 0), (self.mouth_coords[0], self.mouth_coords[1]), (self.mouth_coords[2], self.mouth_coords[3]), 2)

    def set_robot_state(self, new_state):
        self.robot_state = new_state

if __name__ == "__main__":
    robot_face = RobotFace()
    robot_face.animate_eyes()