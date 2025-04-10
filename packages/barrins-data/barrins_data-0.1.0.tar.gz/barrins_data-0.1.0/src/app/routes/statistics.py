from typing import List, Literal

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from src.app.models import CARD_DATABASE, DUEL_DATABASE
from src.app.models.semantic_models import Decklist
from src.app.models.tables.cards_table import Card
from src.app.models.tables.duel_tables import DuelDeck
from src.app.scripts.deck_aggregation import aggregate_decks
from src.app.scripts.deck_clustering import DeckCoordinates, clusters_map

router = APIRouter()


@router.get(
    "/statistics/cluster_map/{mtg_format}",
    response_model=(
        dict[str, dict[str, DeckCoordinates | Decklist]]
        | dict[str, dict[str, list[DeckCoordinates]]]
    ),
    summary="Get the clusters map for a specific MTG format",
    description=(
        "Returns a mapping of decks to their clusters for a specific MTG format. "
        "The format must be one of the following: 'standard', 'modern', 'legacy', 'vintage', 'pioneer', 'duel commander'."
    ),
    response_description="Mapping of decks to their clusters",
)
def cluster_map(mtg_format: str = "duel commander", with_example: bool = False):
    try:
        return clusters_map(mtg_format, with_example)

    except NoResultFound:
        HTTPException(status_code=404, detail="Card not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get(
    "/statistics/aggregate_decks/by_cz_id/",
    response_model=Decklist | List[str],
    summary="Aggregate a list of decks into a single decklist.",
    description="Aggregate a list of decks using specified ID as a commander into a single decklist",
    response_description="The aggregated decklist",
)
def aggregate_decks_by_id(
    card_id: str, order: int = 1, output: Literal["decklist", "text"] = "decklist"
):
    if output not in ["decklist", "text"]:
        raise HTTPException(
            status_code=400, detail="Output must be either 'decklist' or 'text'."
        )
    try:
        with DUEL_DATABASE.get_session() as session:
            decks = DuelDeck.get_by_commander_id(session, card_id)
            if not decks:
                raise NoResultFound
            decklists = [deck.get_decklist() for deck in decks]
            aggregated = aggregate_decks(decklists, order)
            if output == "decklist":
                return aggregated
            if output == "text":
                with CARD_DATABASE.get_session() as session:
                    return [
                        f"{v} {Card.get_by_id(session, k).name}"
                        for k, v in aggregated.maindeck.items()
                    ]
    except NoResultFound:
        raise HTTPException(
            status_code=404, detail=f"No commander with id {card_id} found."
        )
