from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks import ev3brick as brick


class Sensing():
    def __init__(self) -> None:
        super().__init__()
        self.__POSSIBLE_COLORS = (Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW)

        self.color_sensor = ColorSensor(Port.S3)

    def get_color(self):
        col = self.color_sensor.color()
        brick.display.text(str(col))
        return
