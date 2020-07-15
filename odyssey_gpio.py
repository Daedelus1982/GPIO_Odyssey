"""Odyssey GPIO helper

A module for interacting with the GPIO pins on the Odyssey SBC. Uses the periphery library
as a base module.

The dictionary maps the physical GPIO pin number to the periphery requirements

"""
from threading import Thread
from time import sleep

from periphery import GPIO

# key = physical pin, tuple value = bios number, chip number string, line number
GPIOPINS = {3: (110, "/dev/gpiochip1", 34),
            5: (111, "/dev/gpiochip1", 35),
            7: (161, "/dev/gpiochip2", 5),
            8: (61, "/dev/gpiochip0", 61),
            10: (60, "/dev/gpiochip0", 60),
            11: (88, "/dev/gpiochip1", 12),
            12: (162, "/dev/gpiochip2", 6),
            13: (136, "/dev/gpiochip1", 60),
            15: (137, "/dev/gpiochip1", 61),
            16: (145, "/dev/gpiochip1", 69),
            18: (146, "/dev/gpiochip1", 70),
            19: (83, "/dev/gpiochip1", 7),
            21: (82, "/dev/gpiochip1", 6),
            22: (114, "/dev/gpiochip1", 38),
            23: (79, "/dev/gpiochip1", 3),
            24: (80, "/dev/gpiochip1", 4),
            26: (81, "/dev/gpiochip1", 5),
            27: (112, "/dev/gpiochip1", 36),
            28: (113, "/dev/gpiochip1", 37),
            29: (139, "/dev/gpiochip1", 63),
            31: (140, "/dev/gpiochip1", 64),
            32: (115, "/dev/gpiochip1", 39),
            33: (141, "/dev/gpiochip1", 65),
            35: (163, "/dev/gpiochip2", 7),
            36: (134, "/dev/gpiochip1", 58),
            37: (143, "/dev/gpiochip1", 67),
            38: (164, "/dev/gpiochip2", 8),
            40: (165, "/dev/gpiochip2", 9)}

OUT = "out"
IN = "in"
HIGH = True
LOW = False


def fetch_gpio(pin_num, direction):
    """
    Simplifies the creation of a periphery GPIO object using the physical pin number.
    :param pin_num: The physical pin number of the pin.
    :param direction: IN or OUT.
    :return: The GPIO pin as a periphery type
    """
    return GPIO(GPIOPINS[pin_num][1], GPIOPINS[pin_num][2], direction)


class PWM:
    """
    A software PWM implementation for the GPIO pins on the Odyssey SBC.
    """
    def __init__(self, pin_num, frequency=1000):
        self.gpio = fetch_gpio(pin_num, OUT)
        self.on_time = 0
        self.off_time = 0
        self.frequency = frequency
        self.duty_cycle = 100
        if self.set_frequency(frequency) is None:
            self.set_frequency(1000)
        self.gpio.write(LOW)
        self.cycling = False
        self.pwm_thread = Thread(None, self.pulse, None, (), {})

    @staticmethod
    def calc_duties(dc, freq):
        """Not to be called externally"""
        if 0 <= dc <= 100 and freq >= 1:
            cycle = 1.0 / freq
            cycle_percent = cycle / 100
            on_time = dc * cycle_percent
            off_time = (100 - dc) * cycle_percent
            return on_time, off_time
        return None

    def pulse(self):
        """Not to be called externally"""
        while self.cycling:
            self.gpio.write(HIGH)
            sleep(self.on_time)
            self.gpio.write(LOW)
            sleep(self.off_time)

    def start(self, duty_cycle):
        """
        Kicks off the PWM cycle
        :param duty_cycle: Should be between 0 and 100 inclusive
        """
        if not self.cycling:
            if self.set_duty_cycle(duty_cycle) is not None:
                self.cycling = True
                self.pwm_thread = Thread(None, self.pulse, None, (), {})
                self.pwm_thread.start()

    def stop(self):
        """Ends the PWM thread if it is running"""
        if self.cycling:
            self.cycling = False
            self.pwm_thread.join()
            print("exiting")
            self.gpio.direction = IN
            self.gpio.close()

    def set_frequency(self, frequency):
        """
        Can be used to set the frequency whether the PWM thread is running or not
        :param frequency: must be 1 or higher
        """
        if self.calc_duties(self.duty_cycle, frequency) is not None:
            on, off = self.calc_duties(self.duty_cycle, frequency)
            self.frequency = frequency
            self.on_time = on
            self.off_time = off
            return frequency
        return None

    def set_duty_cycle(self, duty_cycle):
        """
        Can be used to set the duty cycle whether the PWM thread is running or not
        :param duty_cycle: must be between 0 and 100 inclusive
        """
        if self.calc_duties(duty_cycle, self.frequency) is not None:
            on, off = self.calc_duties(duty_cycle, self.frequency)
            self.duty_cycle = duty_cycle
            self.on_time = on
            self.off_time = off
            return duty_cycle
        return None
