"""
This script is used to test random aspects of
the 'microsaccade bias duration' experiment.
To run the experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from set_up import get_monitor_and_dir, get_settings
from practice import practice
from psychopy.sound import Sound
from psychopy import prefs, core
import psychtoolbox as ptb
import psychopy
from pprint import pprint
import psychtoolbox.audio
from block import create_trial_list


monitor, directory = get_monitor_and_dir(True)
settings = get_settings(monitor, directory)

freq = 300
chunk_duration = 2

keys_held = set()

current_tone = Sound(freq, secs=chunk_duration, loops=-1, stereo=True, volume=0.1)
current_tone.play()

clock = core.Clock()
duration = 10.0

while clock.getTime() < duration:
    [z_pressed, m_pressed] = settings["keyboard"].getState(["z", "m"])

    if z_pressed:
        freq = max(100, freq - 10)
        new_tone = Sound(freq, secs=chunk_duration, loops=-1, stereo=True, volume=0.1)
        new_tone.play()
        core.wait(0.05)
        current_tone.stop()
        current_tone = new_tone
    if m_pressed:
        freq = min(720, freq + 10)
        new_tone = Sound(freq, secs=chunk_duration, loops=-1, stereo=True, volume=0.1)
        new_tone.play()
        core.wait(0.05)
        current_tone.stop()
        current_tone = new_tone

    core.wait(0.1)

current_tone.stop()
