from collections import deque
from statistics import mode

from pybricks import ev3brick as brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color


class Sensing():
    def __init__(self):
        super().__init__()
        self.__POSSIBLE_COLORS = (Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE, Color.BROWN)
        self.color_samples = 5
        self.color_sensor = ColorSensor(Port.S3)
        self.__col_queue = deque(maxlen=self.color_samples)

    def get_color(self):
        i = 0
        self.__col_queue.append(self.color_sensor.color())
        most_freq_col = mode(self.__col_queue)
        brick.display.text(str(most_freq_col))
        return most_freq_col
