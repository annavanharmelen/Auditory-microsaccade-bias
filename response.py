"""
This file contains the functions necessary for
creating the interactive response dial at the end of a trial.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import event, sound, core
from psychopy.hardware.keyboard import Keyboard
from time import time
from eyetracker import get_trigger
from stimuli import draw_fixation_dot
from math import floor


def evaluate_response(target_frequency, response_frequency, freqs):
    freq_diff = response_frequency - target_frequency
    freq_diff_abs = abs(freq_diff)
    performance = freqs.index(response_frequency) - freqs.index(target_frequency)
    sign = "+" if freq_diff > 0 else ""
    return {
        "frequency_offset": round(freq_diff),
        "frequency_diff_abs": round(freq_diff_abs),
        "performance_abs": abs(performance),
        "performance": f"{sign}{performance}",
    }


def get_response(
    target_pitch,
    target_pitch_cat,
    target_item,
    target_position,
    cached_sounds,
    settings,
    testing,
    eyetracker,
):
    keyboard: Keyboard = settings["keyboard"]

    # Check for pressed 'q'
    check_quit(keyboard)

    # Show response can start
    draw_fixation_dot(settings, [-1, -1, -1])
    settings["window"].flip()

    # These timing systems should start at the same time, this is almost true
    idle_reaction_time_start = time()
    keyboard.clock.reset()

    # Check if _any_ keys were prematurely pressed
    prematurely_pressed = [(p.name, p.rt) for p in keyboard.getKeys(waitRelease=False)]
    keyboard.clearEvents()

    # Set initial settings
    freqs = settings["frequencies"]
    idx = floor(len(freqs) / 2)  # use middle index to start
    responded = False

    # Wait for response to start
    keyboard.clock.reset()
    first_keys = keyboard.waitKeys(keyList=["down", "up", "space"], waitRelease=True)
    keys = first_keys  # use first key press for first tone generation
    response_started = time()

    if not testing and eyetracker:
        trigger = get_trigger(
            "response_onset", target_pitch_cat, target_item, target_position
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Let participant change tone frequency until space bar is pressed
    while not responded:

        if "space" in keys:
            responded = True
            response_freq = freqs[idx]
            response_idx = idx

        if "down" in keys:
            idx = max(idx - 1, 0)
            cached_sounds[(freqs[idx], "both")].play()

        if "up" in keys:
            idx = min(idx + 1, len(freqs) - 1)
            cached_sounds[(freqs[idx], "both")].play()

        keys = keyboard.getKeys(keyList=["down", "up", "space"])

        if keys:
            cached_sounds[(freqs[idx], "both")].stop()

    # Compute both reaction times
    response_time = time() - response_started
    idle_reaction_time = response_started - idle_reaction_time_start

    if not testing and eyetracker:
        trigger = get_trigger(
            "response_offset", target_pitch_cat, target_item, target_position
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Make sure keystrokes made during this trial don't influence the next
    keyboard.clearEvents()

    return {
        "idle_reaction_time_in_ms": round(idle_reaction_time * 1000, 2),
        "response_time_in_ms": round(response_time * 1000, 2),
        "first_key_pressed": first_keys[0].name,
        "response_freq": response_freq,
        "response_idx": response_idx,
        "premature_pressed": True if prematurely_pressed else False,
        "premature_key": prematurely_pressed[0][0] if prematurely_pressed else None,
        "premature_timing": (
            round(prematurely_pressed[0][1] * 1000, 2) if prematurely_pressed else None
        ),
        **evaluate_response(target_pitch, response_freq, freqs),
    }


def wait_for_key(key_list, keyboard):
    keyboard: Keyboard = keyboard
    keyboard.clearEvents()
    keys = keyboard.waitKeys(keyList=key_list)

    return keys


def check_quit(keyboard):
    if keyboard.getKeys("q"):
        raise KeyboardInterrupt()
