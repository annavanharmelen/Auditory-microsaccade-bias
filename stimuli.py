"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import visual, sound, core

DOT_SIZE = 0.1  # diameter of circle
ECCENTRICITY = 6
ITEM_SIZE = 1


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Courier New", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()


def draw_fixation_dot(settings, colour="#eaeaea"):
    # Make fixation dot
    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](DOT_SIZE),
        pos=(0, 0),
        fillColor=colour,
    )

    fixation_dot.draw()


def play_stimulus_frame(item_position, item_pitch, settings):
    draw_fixation_dot(settings)
    tone = sound.Sound(item_pitch, secs=0.5, stereo=True, volume=0.1)
    tone.play()
    core.wait(0.5)


def create_cue_frame(target_item, settings):
    draw_fixation_dot(settings)
    show_text(target_item, settings["window"], pos=(0, settings["deg2pix"](0.3)))


def create_feedback_frame(target_pitch, response_pitch, main_feedback, settings):
    draw_fixation_dot(settings)
    show_text(
        f"Actual: {target_pitch}\nReport: {response_pitch}\n\n{main_feedback}",
        settings["window"],
        (0, settings["deg2pix"](0.65)),
    )
