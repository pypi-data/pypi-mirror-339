import copy
import os

import numpy as np
from PIL import Image


class FakeCamera():

    def __init__(self, colour_mode: str = "colour",
                       pixel_move: int = 5):
        """
        Library for creating a moving image on the screen simulating a camera feed.

        args:
            colour = "colour" or "grayscale",
            pixel_move = int,  # how many pixels the image will move between polls
        """

        self.GRAYSCALE = "grayscale"
        self.COLOUR = "colour"
        self.colour_mode: str = self.COLOUR if colour_mode == self.COLOUR else self.GRAYSCALE
        self.pixel_move: int = pixel_move
        self._use_noisy_image: bool = False # Do not add noise to the images by default
        self._flip_image_toogle = False # Do not flip the image by default

    def add_foreground_image(self, image_path: str=""):
        """Add main foreground image that will be displayed.
            example:
                image_path = 'image_example.jpg'
        """

        if not image_path:
            default_image_path = "lena_color.jpg"
            current_directory = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_directory, default_image_path)

        self.frame = self._get_image_frame(image_path, colour_mode=self.colour_mode)
        return self

    def _get_image_frame(self, image_path: str, colour_mode: str):
        """Read the image from the given path and return the numpy array representation"""

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        frame = Image.open(image_path)

        if colour_mode == self.GRAYSCALE:
            frame = np.asarray(frame.convert("L"))
            return frame
        elif colour_mode == self.COLOUR:
            frame = np.asarray(frame)[..., [2,1,0]]
            return frame

    def add_background_image(self, background_colour: str = "b", background_size: tuple[int] = (1000, 1000)):
        """Add background image to the video feed.
        Args:
            background_colour: "w" == "white", "b" == "blue", "r" == "red"
            background_size = (1000, 1000)  Size of the background where the image will be shown on
        """

        self.canvas = self.get_background_image(background_colour, background_size, self.colour_mode)
        return self

    def get_background_image(self, background_colour: str, background_size: tuple[int], colour_mode: str):
        """Create and return the background image on top the image will be displayed on"""

        if colour_mode == self.GRAYSCALE:
            if background_colour == "r":
                background_image = np.random.randint(1, 255, size=background_size, dtype="uint8")
            if background_colour == "w":
                background_image = np.ones(background_size, dtype="uint8") * 255
            if background_colour == "b":
                background_image = np.zeros(background_size, dtype="uint8")

        if colour_mode == self.COLOUR:
            if background_colour == "r":
                background_image = np.random.randint(1, 255, size=background_size + (3,), dtype="uint8")
            if background_colour == "w":
                background_image = np.ones(background_size + (3,), dtype="uint8") * 255
            if background_colour == "b":
                background_image = np.zeros(background_size + (3,), dtype="uint8")

        return background_image

    def add_noise(self):
        """Add noise in the shown fake video stream"""

        self._use_noisy_image: bool = True
        self._config_noise()
        return self

    def _config_noise(self):
        """Configure noise metadata"""

        self.mean = 0
        self.var = 0.1
        self.sigma = self.var**0.5

    def add_flip_to_feed(self):
        """Introduce a random in-the-middle flip to the video feed"""

        self._flip_image_toogle = True
        self._flip_sign_probability = 0.03
        self.flip_nr = 0
        return self

    def build(self):
        """Build and return the fully functioning FakeCamera object"""

        self._set_canvas_view()
        return self

    def _set_canvas_view(self):
        """Add the main image in the background and create the canvas view"""

        self.upper_left_point_x = int(self.canvas.shape[0]/4)
        self.upper_left_point_y = int(self.canvas.shape[0]/4)

        self.canvas[self.upper_left_point_x:self.upper_left_point_x + int(self.frame.shape[0]),
                    self.upper_left_point_y:self.upper_left_point_y + int(self.frame.shape[1])] = self.frame

        self.limit_x_start = int(self.upper_left_point_x/2)
        self.limit_x_end = - int(self.upper_left_point_x/2)
        self.limit_y_start = int(self.upper_left_point_x/2)
        self.limit_y_end = - int(self.upper_left_point_x/2)

        self.old_start_x = self.upper_left_point_x
        self.old_start_y = self.upper_left_point_y

        self.canvas[self.limit_x_start:self.limit_x_end, self.limit_y_start:self.limit_y_end]

    def _get_latest_image(self):
        """Get the latest snapshot from the fake camera and return it without modifying it beforehand"""

        self.stepsize_x = np.random.randint(-self.pixel_move, self.pixel_move + 1)
        self.stepsize_y = np.random.randint(-self.pixel_move, self.pixel_move + 1)

        new_start_x = min(max(self.limit_x_start, self.old_start_x + self.stepsize_x), self.limit_x_start * 4)
        new_start_y = min(max(self.limit_y_start, self.old_start_y + self.stepsize_y), self.limit_y_start * 2)

        self.old_start_x, self.old_start_y = new_start_x, new_start_y

        end_x = new_start_x + int(self.frame.shape[0])
        end_y = new_start_y + int(self.frame.shape[1])

        canvas_view = self.canvas[new_start_x:end_x, new_start_y:end_y]
        return canvas_view

    def _add_noise_to_image(self, image):
        """Add noise to the image based on the noise configuration"""

        if len(image.shape) == 2:
            row, col = image.shape
            self.gauss = np.random.normal(self.mean, self.sigma, (row, col)) * 50
            self.gauss = self.gauss.reshape(row, col)

        elif len(image.shape) == 3:
            row, col, ch = image.shape
            self.gauss = np.random.normal( self.mean, self.sigma, (row, col, ch) ) * 50
            self.gauss = self.gauss.reshape(row, col, ch)

        self.gauss = self.gauss.astype("uint8")
        noisy_image = image + self.gauss

        return noisy_image

    def _flip_the_image(self, canvas_view):

        if np.random.uniform(low=0.0, high=1.0) < self._flip_sign_probability:
            self.flip_nr += 1

        if self.flip_nr % 2 == 0:
            return copy.deepcopy(canvas_view)

        elif self.flip_nr % 2 == 1:
            return copy.deepcopy(np.fliplr(canvas_view))

    def get_snapshot(self):
        """Get the latest snapshot from the fake camera and return it after modifying it if necessary"""

        snapshot = self._get_latest_image()

        if self._use_noisy_image:
            snapshot = self._add_noise_to_image(snapshot)

        if self._flip_image_toogle:
            snapshot = self._flip_the_image(snapshot)

        return snapshot
