"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import visual, sound, core
import numpy as np

DOT_SIZE = 0.1  # diameter of circle
ECCENTRICITY = 6
ITEM_SIZE = 1

AUDIO_SAMPLE_RATE = 44100


def initialise_all_stimuli(settings):
    cached_sounds = {}

    tone_duration = 0.5  # in seconds
    sample_times = np.linspace(
        0, tone_duration, int(tone_duration * AUDIO_SAMPLE_RATE), endpoint=False
    )

    # Ramp tone up and down
    ramp_ms = 5  # duration in ms
    ramp_samples = int(AUDIO_SAMPLE_RATE * ramp_ms / 1000)
    ramp_up = np.linspace(0, 1, ramp_samples)
    ramp_down = np.linspace(1, 0, ramp_samples)

    # Create zero channel (for left-only and right-only sounds)
    zeros = np.zeros_like(sample_times, dtype=np.float32)

    # Create all 22 possible stereo tones
    for frequency in settings["frequencies"]:
        # Create mono waveform
        waveform = np.sin(2 * np.pi * frequency * sample_times)

        # Apply ramping
        waveform[:ramp_samples] *= ramp_up
        waveform[-ramp_samples:] *= ramp_down

        # Save ramped waveform in right format
        waveform = waveform.astype(np.float32)

        # Create stereo array
        left_stereo = np.stack([waveform, zeros], axis=1)
        right_stereo = np.stack([zeros, waveform], axis=1)

        # Cache sound objects
        cached_sounds[(frequency, "left")] = sound.Sound(
            left_stereo, stereo=True, sampleRate=AUDIO_SAMPLE_RATE
        )
        cached_sounds[(frequency, "right")] = sound.Sound(
            right_stereo, stereo=True, sampleRate=AUDIO_SAMPLE_RATE
        )
        cached_sounds[(frequency, "both")] = sound.Sound(
            waveform, stereo=False, sampleRate=AUDIO_SAMPLE_RATE
        )

    # Make fixation dot
    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](DOT_SIZE),
        pos=(0, 0),
        fillColor="#eaeaea",
    )

    return {
        "sounds": cached_sounds,
        "fixation_dot": fixation_dot,
    }


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Aptos", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()


def draw_fixation_dot(fixation_dot, colour="#eaeaea"):
    fixation_dot.fillColor = colour
    fixation_dot.draw()


def create_cue_frame(target_item, fixation_dot, settings):
    draw_fixation_dot(fixation_dot)
    show_text(target_item, settings["window"], pos=(0, settings["deg2pix"](0.3)))


def create_feedback_frame(main_feedback, fixation_dot, settings):
    draw_fixation_dot(fixation_dot)
    show_text(
        f"{main_feedback}",
        settings["window"],
        (0, settings["deg2pix"](0.3)),
    )
