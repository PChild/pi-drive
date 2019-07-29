from gpiozero import PWMOutputDevice, DigitalOutputDevice
from xbox import XboxController
from sys import platform

'''Checks platform type, used to achieve different functionality on windows vs pi.'''
WINDOWS = platform == 'win32'

'''Set up gpio outputs if actually on a pi'''
# TODO get real pin values
if not WINDOWS:
    motors = {'left_drive': PWMOutputDevice(pin=1),
              'right_drive': PWMOutputDevice(pin=2),
              'dart': PWMOutputDevice(pin=3),
              'left_shooter': PWMOutputDevice(pin=4),
              'right_shooter': PWMOutputDevice(pin=5)}

    solenoids = {'kicker': DigitalOutputDevice(pin=6),
                 'compressor': DigitalOutputDevice(pin=7)}


def tank_drive(controller, drive_scale=0.6, debug=False):
    """
    Drive logic for 401's 2016 bot.
    Can print duty cycle output values on non-pi hardware.

    :param controller: Gamepad to use, should be a 360 controller currently.
    :param drive_scale: scaling factor for drive, defaults to 0.6 for demo mode
    :param debug: print outputs for debugging instead of running
    """
    left = controller.LeftJoystickY * drive_scale
    right = controller.RightJoystickY * drive_scale

    if controller.RightThumb:
        left = 0
        right = 0

    if not WINDOWS:
        motors['left_drive'].value = left
        motors['right_drive'].value = right
    else:
        if debug:
            print('Left:', left, '\tRight:', right)


def shooter(controller, intake_scale=0.3, shoot_scale=0.8,  debug=False):
    """
    Logic for controlling shooter on 401's 2016 robot.
    Can print duty cycle output values on non-pi hardware.

    :param controller: Gamepad to use, should be a 360 controller currently.
    :param intake_scale: scaling factor for intaking speed
    :param shoot_scale: scaling factor for shooting speed
    :param debug: print outputs for debugging instead of running
    """
    intake_speed = controller.LeftTrigger * -1.0 * intake_scale
    shoot_speed = controller.RightTrigger * shoot_scale
    overall = shoot_speed + intake_speed

    left = -1.0 * overall
    right = overall
    fire_kicker = True if overall > 0 and controller.A else False

    if not WINDOWS:
        motors['left_shooter'].value = left
        motors['right_shooter'].value = right

        if fire_kicker:
            solenoids['kicker'].on()
        else:
            solenoids['kicker'].off()
    else:
        if debug:
            print('Left:', left, '\tRight:', right, '\tKicker:', fire_kicker)


def dart(controller, dart_scale=0.8, debug=False):
    """
    Runs Dart actuator for 401's 2016 bot.
    Can print duty cycle output values on non-pi hardware.

    :param controller: Gamepad to use, should be a 360 controller currently.
    :param dart_scale: scaling factor to use, defaults to 80% power
    :param debug: print outputs for debugging instead of running
    """
    if controller.RightThumb:
        output = controller.RightJoystickY * dart_scale
    else:
        output = 0.0

    if debug:
        print('Dart:', output)
    else:
        if not WINDOWS:
            motors['dart'].value = output


def compressor():
    """
    Keep compressor pwm on full on to work with relay.
    No op on non-pi hardware.
    """
    if not WINDOWS:
        solenoids['compressor'].on()


def main():
    """
    Main function for running robot code, should never exit.
    """

    ''' Currently this ONLY works with an xbox 360 controller'''
    controller = XboxController()

    while True:
        compressor()
        tank_drive(controller)
        shooter(controller)
        dart(controller)


if __name__ == "__main__":
    main()
