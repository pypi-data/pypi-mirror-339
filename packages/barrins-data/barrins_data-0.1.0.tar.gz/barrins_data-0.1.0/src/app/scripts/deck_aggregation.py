"""
Source:
    * Inspiration pour l'agrégation de données de decks Magic: The Gathering:
      https://elvishjerricco.github.io/2015/09/24/automatically-generating-magic-decks.html
"""

import re
from collections import Counter, defaultdict
from itertools import combinations
from typing import List, Tuple

from src.app.models.semantic_models import Decklist


def aggregate_decks(decks: List[Decklist], order: int = 1) -> Decklist:
    """Aggregate a list of decks into a single decklist.

    Args:
        decks (list[Decklist]): The list of decks to aggregate.
        order (int, optional): The order of the aggregation. Defaults to 1.

    Returns:
        Decklist: The aggregated decklist.

    Raises:
        ValueError: If the order is less than 1.
    """
    if order < 1:
        raise ValueError("The order must be greater than 0.")

    min_maindeck_size = min(sum((deck.maindeck or {}).values()) for deck in decks)
    min_sideboard_size = min(sum((deck.sideboard or {}).values()) for deck in decks)
    min_commandzone_size = min(sum((deck.commandzone or {}).values()) for deck in decks)

    aggregated_maindeck = aggregate_zone(decks, "maindeck", min_maindeck_size, order)
    aggregated_sideboard = (
        aggregate_zone(decks, "sideboard", min_sideboard_size, order)
        if min_sideboard_size > 0
        else {}
    )
    aggregated_commandzone = (
        aggregate_zone(decks, "commandzone", min_commandzone_size, 1)
        if min_commandzone_size > 0
        else {}
    )

    return Decklist(
        maindeck=aggregated_maindeck,
        sideboard=aggregated_sideboard,
        commandzone=aggregated_commandzone,
    )


def aggregate_zone(decks: List[Decklist], zone: str, size: int, order: int) -> Counter:
    """Aggregate a specific zone of a list of decks into a Counter object.

    Args:
        decks (List[Decklist]): The list of decks to aggregate.
        zone (str): The zone to aggregate.
        size (int): The size of the zone.
        order (int): The order of the aggregation.

    Returns:
        Counter: The aggregated zone.
    """
    collective = Counter()
    ranking_structure = Counter()

    for deck in decks:
        decklist = convert_deck_to_list(deck, zone)
        collective.update(decklist)
        ranking_structure.update(
            get_combinations(decklist, order)
            if order > 1
            else [(card,) for card in decklist]
        )

    if len(collective) > size:
        collective = remove_cards(collective, ranking_structure, size)

    decklist = Counter([re.sub(r"\d+$", "", line).strip() for line in collective])
    return {card: qty for card, qty in decklist.items()}


def convert_deck_to_list(deck: Decklist, zone: str) -> List[str]:
    """Convert a decklist to a list of card names.

    Args:
        deck (Decklist): The decklist to convert.
        zone (str): The zone to convert.

    Returns:
        List[str]: List of cards in the deck with the exemplar and the zone it comes
        from after its name, ie `Snow-covered Island 10 z_md` for the 11th
        `Snow-covered Island` card in the maindeck.
    """
    return [
        f"{card} {i}" for card, qty in getattr(deck, zone).items() for i in range(qty)
    ]


def get_combinations(lst: list[str], tuple_size: int) -> List[Tuple[str]]:
    """Get all combinations of a list of cards.

    Args:
        list[str]: The list of cards.

    Returns:
        List[Tuple[str]]: The combinations of the cards.
    """
    return [tuple(sorted(comb)) for comb in combinations(lst, tuple_size)]


def remove_cards(structure: Counter, rankings: Counter, target_size: int) -> Counter:
    """Remove the least important cards from a structure.

    Args:
        structure (Counter): The structure to remove cards from.
        rankings (Counter): The rankings of the structure.
        target_size (int): The target size of the structure.

    Returns:
        Counter: The structure with the least important cards removed.
    """
    while len(structure) > target_size:
        scores = calculate_scores(rankings, set(structure.keys()))
        lowest = min(scores.keys())
        lowest_ranked = {k: v for k, v in structure.items() if k in scores[lowest]}
        structure = {k: v for k, v in structure.items() if k not in scores[lowest]}
        if len(structure) < target_size:
            structure.update(
                {
                    item[0]: item[1]
                    for idx, item in enumerate(lowest_ranked.items())
                    if idx < (target_size - len(structure))
                }
            )

    return structure


def calculate_scores(rankings: Counter, keys: set[str]) -> dict[float, set[str]]:
    """Calculate the scores of a structure based on rankings.

    Args:
        rankings (Counter): The rankings of the structure.
        keys (set[str]): The keys of the structure.

    Returns:
        dict[float, set[str]]: The scores of the structure.
    """
    scores = defaultdict(float)
    for comb, count in list(rankings.items()):
        if set(comb).issubset(keys):
            rank = count * (1 / (2 ** len(comb)))
            for card in comb:
                scores[card] += rank

    # Clean ranking in place
    rankings = {k: v for k, v in rankings.items() if k in keys}

    cards_by_score = transpose_dict(scores)

    return cards_by_score


def transpose_dict(dict_to_transpose: dict[str, float]) -> dict[float, list[str]]:
    """
    Transpose a dictionary with cards as keys and scores as values into a
    dictionary with scores as keys and lists of cards as values.

    Args:
        dict_to_transpose (dict[str, float]): Dictionary with cards as keys and
        scores as values to transpose.

    Returns:
        dict[float, list[str]]: Dictionary with scores as keys and lists of cards
        as values.
    """
    output_dict = defaultdict(list)
    for key, value in dict_to_transpose.items():
        output_dict[value].append(key)
    return dict(output_dict)
