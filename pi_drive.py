from gpiozero import Servo, DigitalOutputDevice
from xbox import XboxController
from sys import platform

'''Checks platform type, used to achieve different functionality on windows vs pi.'''
WINDOWS = platform == 'win32'

'''Set up gpio outputs if actually on a pi'''
if not WINDOWS:
    motors = {'left_drive': Servo(pin='WPI30'),
              'right_drive': Servo(pin='WPI21'),
              'dart': Servo(pin='WPI22'),
              'left_shooter': Servo(pin='WPI23'),
              'right_shooter': Servo(pin='WPI24')}

    solenoids = {'kicker': DigitalOutputDevice(pin='WPI25')}


def clamp(value, min_val, max_val):
    """
    Clamps a number between a min and a max value.

    :param value: the value to be clamped
    :param min_val: the minimum
    :param max_val: the maximum
    :return the clamped value
    """
    return max(min(value, max_val), min_val)


def arcade_drive(controller, drive_scale=0.6, debug=False):
    """
    Implements an arcade drive for the 2016 robot.

    :param controller: the gamepad to use
    :param drive_scale: scaling factor for the drive
    :param debug: whether or not to debug and print values
    """
    trans = -1.0 * controller.LeftJoystickY * drive_scale
    rot = controller.RightJoystickX
    left = clamp(trans + rot, -1.0, 1.0)
    right = clamp(trans - rot, -1.0, 1.0)

    if controller.RightThumb:
        left = 0
        right = 0

    if debug or WINDOWS:
        print('Left:', left, '\tRight', right)
    else:
        motors['left_drive'] = left
        motors['right_drive'] = right


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

    if debug or WINDOWS:
        print('Left:', left, '\tRight:', right)
    else:
        motors['left_drive'].value = left
        motors['right_drive'].value = right


def shooter(controller, intake_scale=0.3, shoot_scale=0.8, debug=False):
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

    fire_kicker = True if overall > 0 and controller.A else False

    if debug or WINDOWS:
        print('Speed:', overall, '\tKicker:', fire_kicker)
    else:
        motors['left_shooter'].value = overall
        motors['right_shooter'].value = overall

        if fire_kicker:
            solenoids['kicker'].on()
        else:
            solenoids['kicker'].off()


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

    if debug or WINDOWS:
        print('Dart:', output)
    else:
        motors['dart'].value = output


def main():
    """
    Main function for running robot code, should never exit.
    Currently this ONLY works with an xbox 360 controller.
    """
    controller = XboxController()

    while True:
        arcade_drive(controller, debug=True)
        shooter(controller, debug=True)
        dart(controller)


if __name__ == "__main__":
    main()
