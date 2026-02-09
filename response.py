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


def evaluate_response(target_frequency, response_frequency):
    freq_diff = response_frequency - target_frequency
    freq_diff_abs = abs(freq_diff)
    performance = round(freq_diff)
    sign = "+" if freq_diff > 0 else ""
    return {
        "frequency_offset": round(freq_diff),
        "frequency_diff_abs": round(freq_diff_abs),
        "performance": f"{sign}{performance}",
    }


def get_response(
    target_pitch,
    positions,
    target_item,
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
    freq = 450
    freq_step = 50
    chunk_duration = 2
    keys_held = set()
    responded = False

    # Start playing initial tone
    current_tone = sound.Sound(
        freq, secs=chunk_duration, loops=-1, stereo=True, volume=0.1
    )
    current_tone.play()

    # Wait for response to start
    keyboard.clock.reset()
    key = keyboard.waitKeys(keyList=["down", "up", "space"], waitRelease=False)
    response_started = time()

    if not testing and eyetracker:
        trigger = get_trigger("response_onset", positions, target_item)
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Let participant change tone frequency until space bar is pressed
    while not responded:
        [down_pressed, up_pressed, space_pressed] = settings["keyboard"].getState(
            ["down", "up", "space"]
        )

        if space_pressed:
            responded = True
            response_freq = freq
        if down_pressed:
            freq = max(200, freq - freq_step)
            new_tone = sound.Sound(
                freq, secs=chunk_duration, loops=-1, stereo=True, volume=0.1
            )
            new_tone.play()
            core.wait(0.05)
            current_tone.stop()
            current_tone = new_tone
        if up_pressed:
            freq = min(700, freq + freq_step)
            new_tone = sound.Sound(
                freq, secs=chunk_duration, loops=-1, stereo=True, volume=0.1
            )
            new_tone.play()
            core.wait(0.05)
            current_tone.stop()
            current_tone = new_tone

        core.wait(0.1)  # reduce CPU load

    current_tone.stop()

    # Compute both reaction times
    response_time = time() - response_started
    idle_reaction_time = response_started - idle_reaction_time_start

    if not testing and eyetracker:
        trigger = get_trigger("response_offset", positions, target_item)
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Make sure keystrokes made during this trial don't influence the next
    keyboard.clearEvents()

    return {
        "idle_reaction_time_in_ms": round(idle_reaction_time * 1000, 2),
        "response_time_in_ms": round(response_time * 1000, 2),
        "first_key_pressed": key[0].name,
        "response_freq": response_freq,
        "premature_pressed": True if prematurely_pressed else False,
        "premature_key": prematurely_pressed[0][0] if prematurely_pressed else None,
        "premature_timing": (
            round(prematurely_pressed[0][1] * 1000, 2) if prematurely_pressed else None
        ),
        **evaluate_response(target_pitch, response_freq),
    }


def wait_for_key(key_list, keyboard):
    keyboard: Keyboard = keyboard
    keyboard.clearEvents()
    keys = keyboard.waitKeys(keyList=key_list)

    return keys


def check_quit(keyboard):
    if keyboard.getKeys("q"):
        raise KeyboardInterrupt()
