"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

import random
from trial import generate_trial_characteristics
from stimuli import play_stimulus_frame, draw_fixation_dot, show_text
from psychopy.core import wait
from response import get_response, check_quit, wait_for_key
from time import sleep
from trial import single_trial
from numpy import mean


def practice(sounds, eyetracker, settings):
    # Practice response itself
    practice_response(sounds, eyetracker, settings)

    # Practice full trials
    practice_trials(sounds, eyetracker, settings)


def practice_response(sounds, eyetracker, settings):
    # Practice response until participant chooses to stop
    try:
        performance = []

        # Show first screen
        show_text(
            "Welcome!"
            "\nPress SPACE to start practicing how to reproduce tones.",
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
            draw_fixation_dot(settings)
            settings["window"].flip()
            sleep(0.5)

            # Play tone with certain frequency
            freq = random.choice(settings["frequencies"][0:5] + settings["frequencies"][6::])
            play_stimulus_frame("both", freq, sounds, settings)
            settings["window"].flip() # even checken of de toon 500 ms duurt

            # Delay
            draw_fixation_dot(settings)
            settings["window"].flip()
            wait(0.25)

            # Allow response
            report = get_response(
                freq, None, None, None, sounds, settings, True, None
            )

            # Save for post-hoc feedback
            performance.append(int(report["performance_abs"]))

            # Show feedback
            draw_fixation_dot(settings)
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
            draw_fixation_dot(settings)
            settings["window"].flip()
            sleep(random.randint(1500, 2000) / 1000)

            # Check for pressed 'q'
            check_quit(settings["keyboard"])

    except KeyboardInterrupt:
        avg_score = round(mean(performance))

        show_text(
            f"During this practice, your reports were on average off by {avg_score}. "
            "You decided to stop practising the basic response. "
            "Press SPACE to start practicing full trials.",
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


def practice_trials(sounds, eyetracker, settings):
    # Practice full trials until participant chooses to stop
    try:
        performance = []

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
                cached_sounds=sounds,
                settings=settings,
                testing=True,
                eyetracker=None,
            )

            # Save for feedback
            performance.append(int(report["performance_abs"]))

    except KeyboardInterrupt:
        avg_score = round(mean(performance))

        settings["window"].flip()
        show_text(
            f"During this practice, your reports were on average off by {avg_score}. "
            "You decided to stop practicing the trials."
            f"\n\nPress SPACE to start the experiment.",
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
