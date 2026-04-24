"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

import random
from trial import generate_trial_characteristics
from stimuli import draw_fixation_dot, show_text, draw_visual_object
from psychopy.core import wait
from response import (
    get_auditory_response,
    get_visual_response,
    check_quit,
    wait_for_key,
)
from time import sleep
from trial import single_trial
from numpy import mean


def practice(block_type, stimuli, eyetracker, settings):
    # Practice relevant block type response
    if block_type == "auditory":
        practice_trials(stimuli, "auditory", eyetracker, settings)
    elif block_type == "visual":
        practice_trials(stimuli, "visual", eyetracker, settings)


def practice_trials(stimuli, block_type, eyetracker, settings):
    # Practice full trials until participant chooses to stop
    if block_type == "auditory":
        block = "sounds"
    elif block_type == "visual":
        block = "colours"

    try:
        performance = []

        # Show first screen
        show_text(
            f"Welcome!\nPress SPACE to start practicing how to reproduce {block}.",
            settings["window"],
        )
        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()

        while True:
            target_pitch = random.choice(["low", "high"])
            target_position = random.choice(["left", "right"])
            target_item = random.choice([1, 2])

            trial_characteristics = generate_trial_characteristics(
                (target_pitch, target_position, target_item), settings
            )

            # Generate trial
            report = single_trial(
                **trial_characteristics,
                stimuli=stimuli,
                block_type=block_type,
                settings=settings,
                testing=True,
                eyetracker=None,
            )

            # Save for feedback
            performance.append(int(report["performance_abs"]))

    except KeyboardInterrupt:
        settings["window"].flip()
        if len(performance) > 0:
            avg_score = round(mean(performance), 1)
            show_text(
                f"During this practice, your reports were on average off by {avg_score}. "
                f"\n\nPress SPACE to start the experiment.",
                settings["window"],
            )
        else:
            show_text(
                f"You skipped practice 2.\n\nPress SPACE to start the experiment.",
                settings["window"],
            )

        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()


def practice_auditory_response(stimuli, eyetracker, settings):
    # Practice response until participant chooses to stop
    try:
        performance = []

        # Show first screen
        show_text(
            "Welcome!" "\nPress SPACE to start practicing how to reproduce SOUNDS.",
            settings["window"],
        )
        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()

        while True:
            # Show fixation dot in preparation
            draw_fixation_dot(stimuli["fixation_dot"])
            settings["window"].flip()
            sleep(0.5)

            # Play tone with certain frequency
            freq = random.choice(
                settings["frequencies"][0:5] + settings["frequencies"][6::]
            )
            stimuli["sounds"][(freq, "both")].play()
            sleep(0.5)  # wait tone duration + 250 ms

            # Allow response
            report = get_auditory_response(
                freq, None, None, None, stimuli, settings, True, None
            )

            # Save for post-hoc feedback
            performance.append(int(report["performance_abs"]))

            # Show feedback
            draw_fixation_dot(stimuli["fixation_dot"])
            show_text(
                f"{report['performance']}",
                settings["window"],
                (0, settings["deg2pix"](0.3)),
            )

            if report["premature_pressed"] == True:
                show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))

            settings["window"].flip()
            sleep(0.25)

            # Pause before next one
            draw_fixation_dot(stimuli["fixation_dot"])
            settings["window"].flip()
            sleep(random.randint(1500, 2000) / 1000)

            # Check for pressed 'q'
            check_quit(settings["keyboard"])

    except KeyboardInterrupt:
        if len(performance) > 0:
            avg_score = round(mean(performance), 1)
            show_text(
                f"During this practice, your reports were on average off by {avg_score}. "
                "\nPress SPACE to start practicing full trials.",
                settings["window"],
            )
        else:
            show_text(
                "You skipped practice 1.\n\nPress SPACE to practice the next part.",
                settings["window"],
            )

        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from moving to the next part isn't saved
        settings["keyboard"].clearEvents()


def practice_visual_response(stimuli, eyetracker, settings):
    # Practice response until participant chooses to stop
    try:
        performance = []

        # Show first screen
        show_text(
            "Welcome!" "\nPress SPACE to start practicing how to reproduce COLOURS.",
            settings["window"],
        )
        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()

        while True:
            # Show fixation dot in preparation
            draw_fixation_dot(stimuli["fixation_dot"])
            settings["window"].flip()
            sleep(0.25)

            # Show dot with random colour
            colour = random.choice(settings["stimuli_colours"])
            draw_visual_object(stimuli["visual_object"], colour, "middle", settings)
            settings["window"].flip()
            sleep(0.25)

            # Show fixation dot until time to respond
            draw_fixation_dot(stimuli["fixation_dot"])
            settings["window"].flip()
            sleep(0.5)

            # Allow response
            report = get_visual_response(
                colour, None, None, None, stimuli, settings, True, None
            )

            # Save for post-hoc feedback
            performance.append(int(report["performance_abs"]))

            # Show feedback
            draw_fixation_dot(stimuli["fixation_dot"])
            show_text(
                f"{report['performance']}",
                settings["window"],
                (0, settings["deg2pix"](0.3)),
            )

            if report["premature_pressed"] == True:
                show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))

            settings["window"].flip()
            sleep(0.25)

            # Pause before next one
            draw_fixation_dot(stimuli["fixation_dot"])
            settings["window"].flip()
            sleep(random.randint(1500, 2000) / 1000)

            # Check for pressed 'q'
            check_quit(settings["keyboard"])

    except KeyboardInterrupt:
        if len(performance) > 0:
            avg_score = round(mean(performance), 1)
            show_text(
                f"During this practice, your reports were on average off by {avg_score}. "
                "\nPress SPACE to start practicing full trials.",
                settings["window"],
            )
        else:
            show_text(
                "You skipped practice 1.\n\nPress SPACE to practice the next part.",
                settings["window"],
            )

        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from moving to the next part isn't saved
        settings["keyboard"].clearEvents()
