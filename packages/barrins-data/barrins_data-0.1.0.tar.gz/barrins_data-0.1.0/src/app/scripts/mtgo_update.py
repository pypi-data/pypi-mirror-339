import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import Thread

from src.app.config.logger import logger
from src.app.models import CARD_DATABASE
from src.app.models.tables import Card
from src.app.mtg_formats import FORMATS
from src.app.utils import GithubUtils

GIT_REPOSITORY = "https://github.com/Badaro/MTGODecklistCache.git"
ROOT_PATH = Path(__file__).parent.parent.parent.parent.parent
DESTINATION_PATH = ROOT_PATH / "MTGODecklistCache"


def find_format_files(data_queue: Queue, num_threads: int) -> None:
    """
    Find all files in the repository that match one of the format defined in setting file.

    Args:
        data_queue (Queue): A queue to store the file paths.
        num_threads (int): Number of opened threads to process `data_queue`.
    """
    for mtg_format in FORMATS.keys():
        mtg_format = mtg_format.lower()
        logger.debug(f"MTG Format files searched: {mtg_format}")
        for filepath in DESTINATION_PATH.rglob(
            f"*{'*'.join(mtg_format.split())}*", case_sensitive=False
        ):
            with open(filepath, "r", encoding="utf-8") as file:
                data_queue.put((mtg_format, json.load(file)))

    for _ in range(num_threads):
        data_queue.put((None, None))  # Signal that scrapping has ended
        logger.debug("Signal value inserted in queue.")


def data_converter(data: dict, mtg_format: str) -> dict:
    """Convert data from JSON file to be usable by all tournament-related class constructors.

    Args:
        data (dict): A dictionary containing all data from a tournament.

    Returns:
        dict: A dictionary with the data converted to be usable by all tournament-related class constructors.
    """
    conversion = {
        "tournament_data": {},
        "decks_data": [],
        "players_data": [],
        "rounds_data": [],
        "standings_data": [],
    }

    if "Tournament" in data and data["Tournament"]:
        data_date = datetime.strptime(data["Tournament"]["Date"], "%Y-%m-%dT%H:%M:%SZ")
        conversion["tournament_data"] = {
            "name": data["Tournament"]["Name"],
            "date": data_date.date(),
            "url": data["Tournament"]["Uri"],
            "size": (
                0
                if "league" in data["Tournament"]["Name"]
                else 0 if "Decks" not in data else len(data["Decks"])
            ),
        }

    if "Decks" in data and data["Decks"]:
        for deck_data in data["Decks"]:
            conversion["players_data"].append(deck_data["Player"])

            # Handling cases where a player won 2+ leagues in the same day
            player_occurrences = conversion["players_data"].count(deck_data["Player"])
            player_url = (deck_data["AnchorUri"] or "") + (
                str(player_occurrences) if player_occurrences > 1 else ""
            )

            conversion["decks_data"].append(
                {
                    "player": deck_data["Player"],
                    "result": deck_data["Result"],
                    "decklist": build_decklist_from_mtgo(deck_data, mtg_format),
                    "url": player_url,
                }
            )

    if "Rounds" in data and data["Rounds"]:
        for round_data in data["Rounds"]:
            round = {"round": "", "pairings": []}
            round["round"] = round_data["RoundName"]
            for match_data in round_data["Matches"]:
                round["pairings"].append({k.lower(): v for k, v in match_data.items()})
            conversion["rounds_data"].append(round)

    if "Standings" in data and data["Standings"]:
        for standing_data in data["Standings"]:
            conversion["standings_data"].append(
                {k.lower(): v for k, v in standing_data.items()}
            )

    return conversion


def build_decklist_from_mtgo(deck_data: dict, mtg_format: str):
    """Build a decklist from a deck data.

    CardName is edited by replacing `&&` by `//` because of the way
    the card names are displayed in the JSON files: `Walk-In Closet && Forgotten Cellar`
    for example.

    Args:
        deck_data (dict): A dictionary containing all data from a deck.
        mtg_format (str): The format of the deck.

    Returns:
        decklist_class: A decklist object.
    """
    format_models = FORMATS.get(mtg_format)()
    decklist = format_models.decklist()
    mainboard = {}
    sideboard = {}

    for line in deck_data["Mainboard"]:
        line["CardName"] = line["CardName"].replace("&&", "//")  # Handling rooms
        line["CardName"] = line["CardName"].split(":", 1)[0]  # `Ratonkhané:ton`
    for line in deck_data["Sideboard"]:
        line["CardName"] = line["CardName"].replace("&&", "//")  # Handling rooms
        line["CardName"] = line["CardName"].split(":", 1)[0]  # `Ratonkhané:ton`

    try:
        with CARD_DATABASE.get_session() as session:
            card_names = Card.get_by_names(
                session,
                [line["CardName"] for line in deck_data["Mainboard"]]
                + [line["CardName"] for line in deck_data["Sideboard"]],
            )
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des cartes : {e}")
        pass

    try:
        for card_line in deck_data["Mainboard"]:
            card_id = card_names[card_line["CardName"]].id
            if card_id not in mainboard:
                mainboard[card_id] = 0
            mainboard[card_id] += card_line["Count"]
        decklist.maindeck = mainboard
    except Exception as e:
        logger.error(f"Erreur lors de la mise en main : {e} | {card_line}")
        pass

    try:
        for card_line in deck_data["Sideboard"]:
            card_id = card_names[card_line["CardName"]].id
            if card_id not in sideboard:
                sideboard[card_id] = 0
            sideboard[card_id] += card_line["Count"]
        setattr(decklist, decklist.sideboard_or_commandzone, sideboard)
    except Exception as e:
        logger.error(f"Erreur lors de la mise en side : {e} | {card_line}")
        pass

    return decklist


def process_tournaments(data_queue: Queue) -> None:
    """Process tournaments from GitHub `MTGODecklistCache` repository.

    Args:
        data_queue (Queue): A queue to store both the format and the data loaded from a json file.
    """
    try:
        while True:
            mtg_format, data = data_queue.get()

            if mtg_format is None:  # Sentinel value to exit thread
                logger.debug("Sentinel received, stopping worker.")
                data_queue.task_done()
                return

            format_models = FORMATS.get(mtg_format)()
            data_converted = data_converter(data, mtg_format)

            with format_models.database.get_session() as session:
                try:
                    if data_converted.get("tournament_data"):
                        tournament = format_models.tournament.upsert(
                            session, data_converted.get("tournament_data")
                        )
                    if data_converted.get("players_data"):
                        for player_data in data_converted.get("players_data"):
                            format_models.player.upsert(session, player_data)
                    if data_converted.get("decks_data"):
                        for deck_data in data_converted.get("decks_data"):
                            deck_data["tournament_id"] = tournament.id
                            format_models.deck.upsert(session, deck_data)
                    if data_converted.get("standings_data"):
                        for standing_data in data_converted.get("standings_data"):
                            standing_data["tournament_id"] = tournament.id
                            format_models.standings.upsert(session, standing_data)
                    if data_converted.get("rounds_data"):
                        for round_data in data_converted.get("rounds_data"):
                            round_data["tournament_id"] = tournament.id
                            format_models.rounds.upsert(session, round_data)
                except Exception as e:
                    logger.error(f"Erreur lors de l'upsertion du tournoi : {e}")
                finally:
                    data_queue.task_done()

    except Exception as e:
        tournament_data = data_converted.get("tournament_data")
        logger.error(f"Erreur dans le thread de traitement : {e} | {tournament_data}")
        pass


def run_update(num_threads: int = 4) -> None:
    """Update the decklist cache from the GitHub repository."""
    # Initialization & Update
    GithubUtils.clone_or_update_repo(GIT_REPOSITORY, DESTINATION_PATH)

    # Actual script
    data_queue = Queue()
    thread = Thread(target=find_format_files, args=(data_queue, num_threads))
    thread.start()
    logger.info("Data fetching thread started.")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(process_tournaments, data_queue)
        logger.info("All worker threads submitted.")

    thread.join()
    logger.info("Data fetching thread completed.")

    data_queue.join()
    logger.info("All tasks completed.")
