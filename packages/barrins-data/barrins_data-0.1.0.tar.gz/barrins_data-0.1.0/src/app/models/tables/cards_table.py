from typing import Dict, Optional

from sqlalchemy import or_
from sqlalchemy.types import JSON
from sqlmodel import Column, Field, Session, select

from src.app.config.logger import logger
from src.app.models.databases import DBCards


class Card(DBCards, table=True):
    __tablename__ = "cards"

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str = Field(
        index=True,
        title="Card's Name",
        description="Name of the Card based on its official non-Universe (SLU and such expansions) name.",
    )
    type: Optional[str] = Field(
        default=None,
        title="Card's Type",
        description="Full type line of the card, possesses `[super-type]` `type` [- `subtype`*] structure.",
    )
    mana_value: Optional[float] = Field(
        default=None,
        title="Card's Mana Value",
        description="Mana Value of the card represented by a float value.",
    )
    color_identity: Optional[str] = Field(
        default="C",
        title="Card's Color Identity",
        description="Color identity of the card, represented by a string of all colors collated next to each other.",
    )
    text: Optional[str] = Field(
        default=None,
        title="Card's Text",
        description="Card's text, represented by a string.",
    )
    power: Optional[str] = Field(
        default=None,
        title="Card's Power",
        description="Card's power, represented by a string value as some cards have a `*` in their power definition.",
    )
    toughness: Optional[str] = Field(
        default=None,
        title="Card's Toughness",
        description="Card's toughness, represented by a string value as some cards have a `*` in their toughness definition.",
    )
    loyalty: Optional[str] = Field(
        default=None,
        title="Card's Loyalty",
        description="Card's loyalty, represented by an string value.",
    )
    first_print: Optional[str] = Field(
        default=None,
        title="Card's First Print",
        description="Card's first print, represented by a string.",
    )
    legalities: Optional[Dict[str, str]] = Field(
        sa_column=Column(JSON),
        default=None,
        title="Card's Legalities",
        description="Card's legalities, represented by a dictionary with keys like `standard`, `modern`, `legacy`.",
    )
    image: Optional[Dict[str, str]] = Field(
        sa_column=Column(JSON),
        default=None,
        title="Card's Image",
        description="Card's images URL, represented by a dictionary of all faces and arts.",
    )

    @classmethod
    def upsert(cls, session: Session, card_data: dict) -> "Card":
        """Upserts a card into the database.

        Args:
            session (SQLAlchemy.orm.Session): The database session.
            card_data (dict): The card data to upsert.

        Returns:
            Card: The upserted card.
        """
        statement = select(cls).where(cls.name == card_data["name"])
        existing_card = session.exec(statement).first()

        if existing_card:
            changes = []
            for key, value in card_data.items():
                if getattr(existing_card, key) != value:
                    changes.append(
                        {
                            "attr": key,
                            "old_value": getattr(existing_card, key),
                            "new_value": value,
                        }
                    )
                    setattr(existing_card, key, value)

            if changes:
                session.add(existing_card)
                session.commit()
                logger.debug(
                    f"Card updated : {card_data['name']}"
                    + f" | Changes : {','.join([f'{change['attr']}' for change in changes])}"
                )

            return existing_card

        new_card = cls(**card_data)
        session.add(new_card)
        session.commit()
        logger.debug(f"Card added: {card_data['name']}")

        return new_card

    @classmethod
    def get_by_id(cls, session: Session, card_id: str) -> Optional["Card"]:
        """Gets a card by its ID.

        Args:
            session (Session): The database session.
            card_id (str): The ID of the card to get.

        Returns:
            Optional[Card]: The card with the given ID, or None if not found.
        """
        return session.get(cls, card_id)

    @classmethod
    def get_by_ids(
        cls, session: Session, card_ids: list[str]
    ) -> Optional[Dict[str, "Card"]]:
        """Gets a list of cards by their IDs.

        Args:
            session (Session): The database session.
            card_ids (list[str]): The IDs of the cards to get.

        Returns:
            Optional[Dict[str, Card]]: A dictionary mapping card IDs to their corresponding cards, or
            None if not found.
        """
        statement = select(cls).where(cls.id.in_(card_ids))
        query = session.exec(statement).all()
        return {card.id: card for card in query}

    @classmethod
    def get_by_names(
        cls, session: Session, card_names: list[str]
    ) -> Optional[Dict[str, "Card"]]:
        """Gets a list of cards by their names.

        Args:
            session (Session): The database session.
            card_names (list[str]): The names of the cards to get.

        Returns:
            Optional[Dict[str, Card]]: A dictionary mapping card names to their corresponding cards, or
            None if not found.
        """
        statement = select(cls).where(or_(*[cls.name == name for name in card_names]))
        query = session.exec(statement).all()
        result = {card.name: card for card in query}

        if not all(name in result for name in card_names):
            missing_cards = [name for name in card_names if name not in result]
            for missing_card in missing_cards:
                statement = select(cls).where(cls.name.startswith(missing_card))
                query = session.exec(statement).first()
                if query:
                    result[missing_card] = query

        # Check if all cards were found
        if not all(name in result for name in card_names):
            missing_cards = [name for name in card_names if name not in result]
            logger.error(f"Missing cards: {missing_cards}")

        return result

    def to_dict(self: "Card") -> dict:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
