"""
This file contains the functions necessary for
seting up the computer.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import visual, prefs
from psychopy.hardware.keyboard import Keyboard
from math import degrees, atan2, pi


def get_monitor_and_dir(testing: bool):
    prefs.hardware["audioLib"] = ["PTB", "sounddevice", "pyo", "pygame"]

    if testing:
        # laptop
        monitor = {
            "resolution": (2880, 1800),  # in pixels
            "Hz": 120,  # screen refresh rate in Hz
            "width": 30,  # in cm
            "distance": 50,  # in cm
        }

        directory = r"../../Data/test/"

    else:
        # lab
        monitor = {
            "resolution": (1920, 1080),  # in pixels
            "Hz": 239,  # screen refresh rate in Hz
            "width": 53,  # in cm
            "distance": 70,  # in cm
        }

        directory = r"C:\Users\m_bias_duration\Desktop\Duration data"

    return monitor, directory


def get_settings(monitor: dict, directory):
    # Initialise psychopy window
    window = visual.Window(
        color=([-0.5, -0.5, -0.5]),
        size=monitor["resolution"],
        units="pix",
        fullscr=True,
    )

    # Calculate number of visual degrees per pixel on the screen
    degrees_per_pixel = degrees(atan2(0.5 * monitor["width"], monitor["distance"])) / (
        0.5 * monitor["resolution"][0]
    )

    # Create list of used frequencies
    # frequencies = [200, 227, 257, 291, 330, 374, 424, 481, 545, 618, 700]
    # frequencies = [750, 804, 862, 923, 990, 1061, 1137, 1218, 1306, 1400, 1500]
    # frequencies = [750, 772, 794, 818, 841, 866, 891, 917, 944, 972, 1000] # fav so far
    frequencies = [300, 316, 332, 350, 368, 387, 408, 429, 451, 475, 500] # lower so less annoying, but more perceived loudness diff

    return dict(
        window=window,
        deg2pix=lambda deg: round(deg / degrees_per_pixel),
        frequencies=frequencies,
        keyboard=Keyboard(),
        mouse=visual.CustomMouse(win=window, visible=False),
        monitor=monitor,
        directory=directory,
    )
