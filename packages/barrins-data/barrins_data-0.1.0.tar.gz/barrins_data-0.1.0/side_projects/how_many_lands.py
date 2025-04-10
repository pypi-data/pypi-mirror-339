import time
from typing import Literal, Tuple

import numpy as np
import pandas as pd
from scipy.stats import norm

LANDS_IN_DECK = 39  # Change the quantity here
SIMULATIONS = 1_000_000  # Change the quantity here
LANDS_RANGE = range(10, LANDS_IN_DECK + 1)


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f"{func.__name__} took {execution_time:.4f} secondes to run (args: {args})."
        )
        return result

    return wrapper


def compute_uncertainty(
    num_success: int, num_games: int, confidence: float = 0.95
) -> Tuple[float, float]:
    """Calculates the uncertainty of the prediction based on Wilson's formulae.

    Args:
        num_success (int): The number of successes.
        num_games (int): The number of games.
        confidence (float, optional): The confidence level. Defaults to 0.95.

    Returns:
        Tuple[float, float]: The lower and upper bounds of the confidence interval.
    """
    if num_games == 0:
        return (0.0, 1.0)  # Cas extrême où il n'y a aucune partie pertinente

    p = num_success / num_games
    z = norm.ppf(1 - (1 - confidence) / 2)  # Valeur critique de la loi normale

    # Intervalle de Wilson
    denominator = 1 + (z**2 / num_games)
    center = (p + (z**2) / (2 * num_games)) / denominator
    margin = (
        z
        * np.sqrt((p * (1 - p) / num_games) + (z**2) / (4 * num_games**2))
        / denominator
    )

    return center - margin, center + margin


def get_casting_cost(turn: int, color_needed: int) -> str:
    """Gets the string describing the casting cost studied.

    Args:
        turn (int): The current turn
        color_needed (int): The amount needed of the arbitrary color

    Returns:
        str: The mana cost of the spell with good and other color.
    """
    if turn == color_needed:
        return "C" * color_needed
    return str(turn - color_needed) + "C" * color_needed


@timer
def run_simulations(good_lands: int, turn: int, colority: int) -> Tuple[int, int]:
    """Run simulations to determine the successes of the share of good lands
    for specified colority.

    Args:
        good_lands (int): Amount of good lands in the deck
        turn (int): Turn being studied
        colority (int): Amount of good sources needed

    Returns:
        Tuple[int, int]: The number of successes and the number of games
    """
    num_success, num_games = 0, 0

    for _ in range(SIMULATIONS):
        outcome = get_outcome(good_lands, turn, colority)
        num_success += outcome == "Success"
        num_games += outcome != "Irrelevant"

    return num_success, num_games


def get_outcome(
    good_lands: int, turn: int, colority: int
) -> Literal["Success", "Failure", "Irrelevant"]:
    """Simulate a game to determine if the deck has a source.

    Args:
        decklist (np.ndarray): A shuffled decklist.
        turn (int): The turn number.
        spell_colority (int): The colority of the spells in the deck.

    Returns:
        Literal["Success", "Failure", "Irrelevant"]: The outcome of the simulation.
    """
    library = build_library(good_lands)
    for handsize in [7, 6, 5, 4]:  # We keep all 4-card hand
        np.random.shuffle(library)  # Shuffling the library before
        hand = {"Good Land": 0, "Other Land": 0, "Spell": 0}
        unique, counts = np.unique(library[:7], return_counts=True)
        for card_type, quantity in zip(unique, counts):
            hand[card_type] = quantity

        if mulligan_hand(hand, handsize):  # We keep the hand
            break

    for card in library[7 : 7 + turn - 1]:
        hand[card] += 1

    if hand["Good Land"] + hand["Other Land"] < turn:
        return "Irrelevant"
    if hand["Good Land"] < colority:
        return "Failure"
    return "Success"


def build_library(good_lands: int) -> np.ndarray:
    """Build a library with kind of card as key and quantity as value.

    Args:
        good_lands (int): The number of good lands in the deck.

    Returns:
        np.ndarray: A shuffled decklist.
    """
    deck = np.concatenate(
        [
            np.full(good_lands, "Good Land"),
            np.full(LANDS_IN_DECK - good_lands, "Other Land"),
            np.full(99 - LANDS_IN_DECK, "Spell"),
        ]
    )
    return np.random.permutation(deck)


def mulligan_hand(hand: dict[str, int], handsize: int) -> bool:
    """Check if the hand is a mulligan hand.

    A mulligan hand is a hand with less than 3 lands.

    Args:
        hand (dict): A dictionary with the hand.
        handsize (int): The hand size.

    Returns:
        bool: True if the hand is a mulligan hand, False otherwise.
    """
    keephand = False
    nb_lands_in_hand = hand["Good Land"] + hand["Other Land"]

    if handsize == 7:
        keephand = nb_lands_in_hand >= 3 and nb_lands_in_hand <= 5

    if handsize == 6:  # Objective is to keep 3 lands and 3 spells
        if hand["Spell"] > 3:  # Remove a spell if we can
            hand["Spell"] -= 1
        else:
            bottom_a_land(hand, 1)
        keephand = nb_lands_in_hand >= 2 and nb_lands_in_hand <= 4

    if handsize == 5:  # Ideal would be 3 land, 2 spells
        if hand["Spell"] > 3:  # Bottom 2 spells
            hand["Spell"] -= 2
        elif hand["Spell"] == 3:  # Bottom 1 land, 1 spell
            bottom_a_land(hand, 1)
            hand["Spell"] -= 1
        else:
            bottom_a_land(hand, 2)
        keephand = nb_lands_in_hand >= 2 and nb_lands_in_hand <= 4

    if handsize == 4:  # Ideal 3 land and 1 spell
        if hand["Spell"] > 3:  # Bottom 3 spells
            hand["Spell"] -= 3
        elif hand["Spell"] == 3:  # Bottom 1 land, 2 spells
            bottom_a_land(hand, 1)
            hand["Spell"] -= 2
        elif hand["Spell"] == 2:  # Bottom 2 lands, 1 spell
            bottom_a_land(hand, 2)
            hand["Spell"] -= 1
        else:
            bottom_a_land(hand, 3)
        keephand = True  # We keep whatever we get

    return keephand


def bottom_a_land(hand: dict[str, int], lands_to_bottom: int) -> None:
    """Bottom a land from the hand.

    Args:
        hand (dict): A dictionary with the hand.
        lands_to_bottom (int): The number of lands to bottom.
    """
    bottom_other_lands = min(hand["Other Land"], lands_to_bottom)
    hand["Other Land"] -= bottom_other_lands

    bottom_good_lands = min(hand["Good Land"], lands_to_bottom - bottom_other_lands)
    hand["Good Land"] -= bottom_good_lands


if __name__ == "__main__":
    data = []

    # Quantity of good lands after turn 4 has less impact during deckbuilding
    for turn in range(1, 4 + 1):
        # Checking for 0 colors on any turn is just using hypergeometric distribution
        colors_needed = range(1, turn + 1)
        # Let's check for each quantity of colors how the simulations get
        for color_needed in colors_needed:
            casting_cost = get_casting_cost(turn, color_needed)
            for num_good_lands in LANDS_RANGE:
                successes, games = run_simulations(num_good_lands, turn, color_needed)
                lower, upper = compute_uncertainty(successes, games)
                data.append(
                    {
                        "Turn": turn,
                        "Color Needed": color_needed,
                        "Casting Cost": casting_cost,
                        "Good Lands": num_good_lands,
                        "Successes": successes,
                        "Games": games,
                        "Success Rate": successes / games,
                        "Lower Bound": lower,
                        "Upper Bound": upper,
                    }
                )

    df = pd.DataFrame(data)
    csv_path = f"simulation_results_{SIMULATIONS}.csv"
    excel_path = f"simulation_results_{SIMULATIONS}.xlsx"
    df.to_csv(csv_path, index=False)
    df.to_excel(excel_path, index=False)
