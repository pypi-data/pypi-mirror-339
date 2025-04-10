import numpy as np

from src.app.models.semantic_models import Decklist


def generate_keys() -> list[str]:
    """
    Generate keys for the modelization of a deck.

    Returns:
        list[str]: A list of keys for the modelization of a deck.
    """
    keys = []

    colors = ["W", "U", "B", "R", "G"]
    for color in colors:
        keys.append(f"has_{color}")

    types = [
        "Creature",
        "Artifact",
        "Enchantment",
        "Planeswalker",
        "Instant",
        "Sorcery",
        "Land",
    ]
    for card_type in types:
        keys.append(f"type_{card_type}")

    mana_values = list(range(16))
    for mana_value in mana_values:
        keys.append(f"mv_{mana_value}")

    return keys


def modelize_deck(decklist: Decklist) -> dict[str, int]:
    """
    Modelize a decklist.

    Args:
        decklist (Decklist): A decklist object.

    Returns:
        dict[str, int]: A dictionary containing the modelized deck.
    """
    keys = generate_keys()
    model = {key: 0 for key in keys}

    card_objects = decklist.all_cards()
    for card, qty in decklist.maindeck.items():
        card_object = card_objects.get(card)

        # Deck colority
        card_colors = [color for color in card_object.color_identity]
        for color in card_colors:
            model[f"has_{color}"] = 1

        # Card types
        card_types = card_object.type.split()
        for card_type in card_types:
            if f"type_{card_type}" in keys:
                model[f"type_{card_type}"] += qty

        # Mana value
        model[f"mv_{int(card_object.mana_value)}"] += qty

    return model


def get_vector_from_decks(decks: list) -> list:
    """Returns a list of vectors representing the decks in the given list.

    Args:
        decks (list): A list of Deck objects.

    Returns:
        np.ndarray: A 2D numpy array where each row is a vector representing a deck.
    """
    models = [modelize_deck(deck.get_decklist()) for deck in decks]
    keys = list(models[0].keys())
    key_index = {key: idx for idx, key in enumerate(keys)}

    vectors = []
    for model in models:
        vector = np.zeros(len(key_index), dtype=int)
        for key, value in model.items():
            vector[key_index[key]] = value
        vectors.append(vector)

    vectors = np.array(vectors)
    return vectors[:, ~np.all(vectors == 0, axis=0)]
