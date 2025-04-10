from typing import Dict, Optional

from pydantic import BaseModel
from sqlmodel import Field
from typing_extensions import Annotated

from src.app.models import CARD_DATABASE
from src.app.models.tables import Card


class Decklist(BaseModel):
    """A decklist is a collection of cards in different quantities."""

    maindeck: Dict[str, Annotated[int, Field(gt=0)]] = {}
    sideboard: Optional[Dict[str, Annotated[int, Field(gt=0)]]] = None
    commandzone: Optional[Dict[str, Annotated[int, Field(gt=0)]]] = None

    sideboard_or_commandzone: Optional[str] = None

    def to_dict(self: "Decklist") -> dict:
        return {
            "maindeck": self.maindeck,
            "sideboard": self.sideboard or {},
            "commandzone": self.commandzone or {},
        }

    @property
    def full_decklist(self: "Decklist") -> dict[str, int]:
        """Returns the full decklist, including the maindeck, sideboard, and command zone."""
        full_decklist = self.maindeck.copy()
        if self.sideboard:
            full_decklist.update(self.sideboard)
        if self.commandzone:
            full_decklist.update(self.commandzone)

        return full_decklist

    def all_cards(self: "Decklist") -> dict[str, Card]:
        """Returns all Card objects related to the decklist."""
        with CARD_DATABASE.get_session() as session:
            return Card.get_by_ids(session, self.full_decklist.keys())
