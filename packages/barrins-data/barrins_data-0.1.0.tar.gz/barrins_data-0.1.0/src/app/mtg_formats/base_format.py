from typing import Optional

from pydantic import BaseModel, Field


class BaseFormat(BaseModel):
    database: Optional[object] = Field(
        default=None,
        title="Database connection",
        description="Database connection to use for the specific format",
    )
    tournament: Optional[object] = Field(
        default=None,
        title="Tournament table",
        description="Tournament table to use for the specific format",
    )
    deck: Optional[object] = Field(
        default=None,
        title="Deck table",
        description="Deck table to use for the specific format",
    )
    decklist: Optional[object] = Field(
        default=None,
        title="Decklist class",
        description="Decklist class to use for the specific format",
    )
    player: Optional[object] = Field(
        default=None,
        title="Player class",
        description="Player class to use for the specific format",
    )
    rounds: Optional[object] = Field(
        default=None,
        title="Rounds class",
        description="Rounds class to use for the specific format",
    )
    standings: Optional[object] = Field(
        default=None,
        title="Standings class",
        description="Standings class to use for the specific format",
    )
