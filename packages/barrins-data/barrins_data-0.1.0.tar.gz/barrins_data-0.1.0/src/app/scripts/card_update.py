from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Thread

from src.app.config.logger import logger
from src.app.models import CARD_DATABASE
from src.app.models.tables import Card
from src.app.utils.scryfall import ScryfallUtils


def fetch_data(data_queue: Queue, num_threads: int):
    """Fetch data from Scryfall API.

    This function is used to fetch data from Scryfall API. It fetches the data from Scryfall API, and returns the data
    in a dictionary format.

    Args:
        data_queue (Queue): A list of dictionaries containing card data from Scryfall API.
        num_threads (int): Number of opened threads to process `data_queue`.
    """
    data = {
        "data": [],
        "has_more": True,
        "next_page": "https://api.scryfall.com/cards/search?format=json&include_extras=false&include_multilingual=false&include_variations=false&order=name&q=is%3Afirstprint",
    }

    try:
        while data["has_more"]:
            data = ScryfallUtils.call_scryfall_api(data["next_page"])
            if "data" in data:
                for card in data["data"]:
                    data_queue.put(card)

        for _ in range(num_threads):
            data_queue.put(None)  # Signal that scrapping has ended
            logger.debug("Signal value inserted in queue.")

    except Exception as e:
        logger.error(f"Error fetching data: {e}")


def data_converter(card_dict: dict) -> dict:
    """Convert data from Scryfall API to be usable by the Card class constructor.

    Args:
        card_dict (dict): A dictionary containing card data from Scryfall API.

    Returns:
        dict: A dictionary containing card data in a format usable by the Card class constructor.
    """
    has_faces = "card_faces" in card_dict
    has_images = "image_uris" in card_dict["card_faces"][0] if has_faces else False

    return {
        "id": card_dict["id"],
        "name": card_dict["name"],
        "type": card_dict["type_line"],
        "mana_value": card_dict["cmc"],
        "power": (
            " // ".join([str(face.get("power", 0)) for face in card_dict["card_faces"]])
            if has_faces
            else card_dict["power"] if "power" in card_dict else None
        ),
        "toughness": (
            " // ".join(
                [str(face.get("toughness", 0)) for face in card_dict["card_faces"]]
            )
            if has_faces
            else card_dict["toughness"] if "toughness" in card_dict else None
        ),
        "loyalty": (
            str(card_dict["loyalty"])
            if not has_faces and "loyalty" in card_dict
            else (
                " // ".join(
                    [str(face.get("loyalty", 0)) for face in card_dict["card_faces"]]
                )
                if has_faces
                and any("loyalty" in face for face in card_dict["card_faces"])
                else None
            )
        ),
        "color_identity": "".join(card_dict["color_identity"]) or "C",
        "first_print": card_dict["set"],
        "legalities": card_dict["legalities"],
        "image": card_dict.get(
            "image_uris",
            {
                "front": (
                    card_dict["card_faces"][0]["image_uris"]
                    if has_faces and has_images
                    else ""
                ),
                "back": (
                    card_dict["card_faces"][1]["image_uris"]
                    if has_faces and has_images
                    else ""
                ),
            },
        ),
        "text": (
            "\n//\n".join([face["oracle_text"] for face in card_dict["card_faces"]])
            if has_faces
            else card_dict["oracle_text"]
        ),
    }


def process_queue(data_queue: Queue):
    """Process cards from Scryfall API.

    Args:
        data_queue (Queue): A list of dictionaries containing card data from Scryfall API.
    """
    try:
        while True:
            card = data_queue.get()

            if card is None:  # Sentinel value to exit thread
                logger.debug("Sentinel received, stopping worker.")
                data_queue.task_done()
                return

            with CARD_DATABASE.get_session() as session:
                try:
                    Card.upsert(session, data_converter(card))
                except Exception as e:
                    logger.error(f"Erreur lors du traitement de la carte : {e}")
                finally:
                    data_queue.task_done()

    except Exception as e:
        logger.error(f"Erreur dans le thread de traitement : {e}")


def run_update(num_threads: int = 4) -> None:
    """Run the update process."""
    data_queue = Queue()
    thread = Thread(target=fetch_data, args=(data_queue, num_threads))
    thread.start()
    logger.info("Data fetching thread started.")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(process_queue, data_queue)
        logger.info("All worker threads submitted.")

    thread.join()
    logger.info("Data fetching thread completed.")

    data_queue.join()
    logger.info("All tasks completed.")
