from gpiozero import PWMOutputDevice, DigitalOutputDevice
from sys import platform
import inputs
import xbox

if platform == "linux" or platform == "linux2":
    motors = {'left_drive': PWMOutputDevice(pin=1),
              'right_drive': PWMOutputDevice(pin=2),
              'dart': PWMOutputDevice(pin=3),
              'left_shooter': PWMOutputDevice(pin=4),
              'right_shooter': PWMOutputDevice(pin=5)}

    solenoids = {'kicker': DigitalOutputDevice(pin=6)}
else:
    motors = {}
    solenoids = {}


def e_stop():
    for m in motors:
        motors[m].off()

    for s in solenoids:
        solenoids[s].off()


def main():
    while True:
        try:
            for event in inputs.get_gamepad():
                print(event.ev_type, event.code, event.state)

                if event.code == xbox.A:
                    print('pew')
        except inputs.UnpluggedError:
            e_stop()


if __name__ == "__main__":
    main()
