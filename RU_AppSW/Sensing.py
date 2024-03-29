from collections import deque

from pybricks import ev3brick as brick
from pybricks.ev3devices import ColorSensor, InfraredSensor, TouchSensor
from pybricks.parameters import Port, Color


class Sensing():
    # def __init__(self):
    #     super().__init__()
    #     self.__POSSIBLE_COLORS = (Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE, Color.BROWN)
    #     self.color_samples = 5
    #     self.color_sensor = ColorSensor(Port.S2)
    #     self.__col_queue = deque(maxlen=self.color_samples)

    # @staticmethod
    # def most_frequent(l):
    #     counter = 0
    #     num = [0]

    #     for i in l:
    #         curr_frequency = l.count(i)
    #         if (curr_frequency > counter):
    #             counter = curr_frequency
    #             num = i
    #     return num

    # def get_color(self):
    #     i = 0
    #     self.__col_queue.append(self.color_sensor.color())
    #     most_freq_col = self.most_frequent(self.__col_queue)
    #     brick.display.text(str(most_freq_col))
    #     return most_freq_col
    def __init__(self):
        super().__init__()
        self.__POSSIBLE_COLORS = (Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE, Color.BROWN)
        self.color_samples = 5
        #self.touch_sensor = TouchSensor(Port.S1)
        self.color_sensor = ColorSensor(Port.S2)
<<<<<<< HEAD
        self.infrared_sensor = InfraredSensor(Port.S3)
=======
        #self.infrared_sensor = InfraredSensor(Port.S4)
>>>>>>> ce09e489048ff7f6338ae64597ccfb944901b485
        #self.__col_queue = deque(maxlen=self.color_samples)

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
        #i = 0
        #self.__col_queue.append(self.color_sensor.color())
        #most_freq_col = self.most_frequent(self.__col_queue)
        #brick.display.text(str(most_freq_col))
        #return most_freq_col
        return self.color_sensor.color()

    def get_reflection(self):
        return self.color_sensor.reflection()

    def get_button(self):
        return [self.infrared_sensor.buttons(1),self.infrared_sensor.buttons(2),self.infrared_sensor.buttons(3),self.infrared_sensor.buttons(4)]

    def get_distance(self):
        return self.infrared_sensor.distance()

    def is_pressed(self):
        return self.touch_sensor.pressed()

sensing = Sensing()


def get_sensing():
    return sensing