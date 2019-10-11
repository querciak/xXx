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

    @staticmethod
    def most_frequent(l):
        counter = 0
        num = [0]

        for i in l:
            curr_frequency = l.count(i)
            if (curr_frequency > counter):
                counter = curr_frequency
                num = i
        return num

    def get_color(self):
        i = 0
        self.__col_queue.append(self.color_sensor.color())
        most_freq_col = mode(self.__col_queue)
        brick.display.text(str(most_freq_col))
        return most_freq_col
