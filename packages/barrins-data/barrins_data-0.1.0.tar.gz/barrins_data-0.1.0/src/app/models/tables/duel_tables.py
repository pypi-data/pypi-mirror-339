import datetime
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy.types import JSON
from sqlmodel import Column, Field, Relationship, Session, select

from src.app.config.logger import logger
from src.app.models.databases import DBDuel
from src.app.models.semantic_models import Decklist


class DuelTournament(DBDuel, table=True):
    __tablename__ = "duel_tournaments"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(title="Tournament's name", description="Name of the tournament.")
    date: datetime.date = Field(
        title="Tournament's date", description="Date of the tournament."
    )
    url: str = Field(
        index=True, title="Tournament's URL", description="URL of the tournament."
    )
    size: int = Field(
        title="Tournament's size",
        description="Number of participants in the tournament.",
    )

    decks: List["DuelDeck"] = Relationship(back_populates="in_tournament")
    standings: List["DuelStanding"] = Relationship(back_populates="tournament")
    rounds: List["DuelRound"] = Relationship(back_populates="tournament")

    @classmethod
    def upsert(cls, session: Session, tournament_data: dict) -> "DuelTournament":
        """Upserts a tournament into the database.

        Args:
            session (Session): The database session.
            tournament_data (dict): The tournament data to upsert.

        Returns:
            DuelTournament: The upserted tournament.
        """
        statement = select(cls).where(cls.url == tournament_data["url"])
        existing_tournament = session.exec(statement).first()

        if existing_tournament:
            changes = []
            for key, value in tournament_data.items():
                if getattr(existing_tournament, key) != value:
                    changes.append(
                        {
                            "attr": key,
                            "old_value": getattr(existing_tournament, key),
                            "new_value": value,
                        }
                    )
                    setattr(existing_tournament, key, value)

            if changes:
                session.add(existing_tournament)
                session.commit()
                logger.debug(
                    f"Tournament updated : {existing_tournament.id}"
                    + f" | Changes : {','.join([f'{change['attr']}' for change in changes])}"
                )

            return existing_tournament

        new_tournament = cls(**tournament_data)
        session.add(new_tournament)
        session.commit()
        logger.debug(f"Tournament added: {new_tournament.id}")

        return new_tournament

    @classmethod
    def get_by_dates(
        cls, session: Session, start_date: datetime.date, end_date: datetime.date
    ) -> List["DuelTournament"]:
        statement = (
            select(cls).where(cls.date >= start_date).where(cls.date <= end_date)
        )
        return session.exec(statement).all()


class DuelDeck(DBDuel, table=True):
    __tablename__ = "duel_decks"

    id: Optional[int] = Field(
        default=None,
        title="Deck's ID",
        description="Unique identifier for the deck.",
        primary_key=True,
    )
    tournament_id: int = Field(
        title="Tournament's ID",
        foreign_key="duel_tournaments.id",
        description="ID of the tournament the deck is in.",
    )
    player_id: int = Field(
        title="Player's ID",
        foreign_key="duel_players.id",
        description="Name of the player who created the deck.",
    )
    result: Optional[str] = Field(
        title="Deck's result", description="Result of the deck in the tournament."
    )
    decklist: Dict[str, Dict[UUID, int]] = Field(
        sa_column=Column(JSON),  # Stocker la decklist sous forme de JSON
        title="Decklist",
        description="List of cards in the deck.",
    )
    url: Optional[str] = Field(
        title="Deck's URL",
        description="URL of the deck on a platform (e.g. MTGGoldfish).",
    )

    in_tournament: Optional["DuelTournament"] = Relationship(back_populates="decks")
    player: Optional["DuelPlayer"] = Relationship(back_populates="decks")

    def decklist_from_pydantic(self, decklist: "DuelDecklist") -> None:
        self.decklist = decklist.model_dump(mode="json")

    def get_decklist(self) -> "DuelDecklist":
        return DuelDecklist(**self.decklist)

    @classmethod
    def upsert(cls, session: Session, deck_data: dict) -> "DuelDeck":
        """Upserts a deck into the database.

        Args:
            session (Session): The database session.
            deck_data (dict): The deck data to upsert.

        Returns:
            DuelDeck: The upserted deck.
        """
        duel_player = DuelPlayer.upsert(session, deck_data["player"])
        deck_data["player_id"] = duel_player.id
        del deck_data["player"]

        deck_data["decklist"] = deck_data["decklist"].model_dump(mode="json")

        statement = (
            select(cls)
            .where(cls.tournament_id == deck_data["tournament_id"])
            .where(cls.player_id == deck_data["player_id"])
            .where(cls.url == deck_data["url"])
        )
        existing_deck = session.exec(statement).first()

        if existing_deck:
            changes = []
            for key, value in deck_data.items():
                if getattr(existing_deck, key) != value:
                    changes.append(
                        {
                            "attr": key,
                            "old_value": getattr(existing_deck, key),
                            "new_value": value,
                        }
                    )
                    setattr(existing_deck, key, value)

            if changes:
                session.add(existing_deck)
                session.commit()
                logger.debug(
                    f"Deck updated : {existing_deck.id}"
                    + f" | Changes : {','.join([f'{change['attr']}' for change in changes])}"
                )

            return existing_deck

        new_deck = cls(**deck_data)
        session.add(new_deck)
        session.commit()
        logger.debug(f"Deck added: {new_deck.id}")

        return new_deck

    @classmethod
    def get_by_dates(
        cls, session: Session, start_date: datetime.date, end_date: datetime.date
    ) -> List["DuelDeck"]:
        """Get all decks between two dates.

        Args:
            session (Session): The database session.
            start_date (datetime.date): The start date.
            end_date (datetime.date): The end date.

        Returns:
            List[DuelDeck]: A list of decks between the two dates.
        """
        tournament_ids = [
            tournament.id
            for tournament in DuelTournament.get_by_dates(session, start_date, end_date)
        ]
        statement = select(cls).where(cls.tournament_id.in_(tournament_ids))
        return session.exec(statement).all()

    @classmethod
    def get_decks_from_30_days(cls, session: Session) -> List["DuelDeck"]:
        """Get all decks from the last 30 days.

        Args:
            session (Session): The database session.

        Returns:
            List[DuelDeck]: A list of decks from the last 30 days.
        """
        today = datetime.date.today()
        thirty_days_ago = today - datetime.timedelta(days=30)
        return cls.get_by_dates(session, thirty_days_ago, today)

    @classmethod
    def get_by_id(cls, session: Session, deck_id: int) -> Optional["DuelDeck"]:
        """Get a deck by its ID.

        Args:
            session (Session): The database session.
            deck_id (int): The ID of the deck to get.

        Returns:
            Optional[DuelDeck]: The deck with the given ID, or None if not found.
        """
        return session.get(cls, deck_id)

    @classmethod
    def get_by_commander_id(
        cls, session: Session, commander_id: int
    ) -> List["DuelDeck"]:
        """Get all decks with a specific commander.

        Args:
            session (Session): The database session.
            commander_id (int): The ID of the commander to filter by.

        Returns:
            List[DuelDeck]: A list of decks with the specified commander.
        """
        statement = select(cls)
        all_decks = session.exec(statement).all()
        return [
            deck for deck in all_decks if commander_id in deck.decklist["commandzone"]
        ]

    @property
    def str_commandzone(self: "DuelDeck") -> str:
        """Returns the command zone as a string."""
        decklist = self.get_decklist()
        decklist_cards = decklist.all_cards()
        command_zone = decklist.commandzone

        if len(command_zone) > 1:
            cards = [
                decklist_cards[card]
                for card in command_zone
                if (
                    "Companion" not in decklist_cards[card].text
                    or "Doctor's" in decklist_cards[card].text
                )
                and "Background" not in decklist_cards[card].type
            ]

            return " + ".join(
                sorted([card.name.split(" // ")[0].strip() for card in cards])
            )

        return decklist_cards[list(command_zone.keys())[0]].name


class DuelPlayer(DBDuel, table=True):
    __tablename__ = "duel_players"

    id: Optional[int] = Field(
        default=None,
        title="Player's ID",
        description="Unique identifier for the player.",
        primary_key=True,
    )
    name: str = Field(title="Player's name", description="Name of the player.")

    decks: List["DuelDeck"] = Relationship(back_populates="player")
    standings: List["DuelStanding"] = Relationship(back_populates="player")

    @classmethod
    def upsert(cls, session: Session, player_name: str) -> "DuelPlayer":
        """Upserts a player into the database.

        Args:
            session (Session): The database session.
            player_name (str): The name of the player to upsert.

        Returns:
            DuelPlayer: The upserted player.
        """
        statement = select(cls).where(cls.name == player_name)
        existing_player = session.exec(statement).first()

        if existing_player:
            return existing_player

        new_player = cls(name=player_name)
        session.add(new_player)
        session.commit()
        logger.debug(f"Player added: {new_player.id}")

        return new_player


class DuelStanding(DBDuel, table=True):
    __tablename__ = "duel_standings"

    id: Optional[int] = Field(
        default=None,
        title="Standing's ID",
        description="Unique identifier for the standing.",
        primary_key=True,
    )
    tournament_id: int = Field(
        title="Tournament's ID",
        foreign_key="duel_tournaments.id",
        description="ID of the tournament the standing is in.",
    )
    player_id: int = Field(
        title="Player's ID",
        foreign_key="duel_players.id",
        description="ID of the player in the standing.",
    )
    rank: int = Field(default=0, description="The player's rank in the tournament.")
    points: int = Field(default=0, description="The player's points.")
    wins: int = Field(default=0, description="The player's wins.")
    losses: int = Field(default=0, description="The player's losses.")
    draws: int = Field(default=0, description="The player's draws.")
    omwp: float = Field(default=0, description="The player's OMWP.")
    gwp: float = Field(default=0, description="The player's GWP.")
    ogwp: float = Field(default=0, description="The player's OGWP.")

    tournament: Optional["DuelTournament"] = Relationship(back_populates="standings")
    player: Optional["DuelPlayer"] = Relationship(back_populates="standings")

    @classmethod
    def upsert(cls, session: Session, standing_data: dict) -> "DuelStanding":
        """Upserts a standing into the database.

        Args:
            session (Session): The database session.
            standing_data (dict): The standing data to upsert.

        Returns:
            DuelStanding: The upserted standing.
        """
        duel_player = DuelPlayer.upsert(session, standing_data["player"])
        standing_data["player_id"] = duel_player.id
        del standing_data["player"]

        statement = (
            select(cls)
            .where(cls.tournament_id == standing_data["tournament_id"])
            .where(cls.player_id == standing_data["player_id"])
        )
        existing_standing = session.exec(statement).first()

        if existing_standing:
            changes = []
            for key, value in standing_data.items():
                if getattr(existing_standing, key) != value:
                    changes.append(
                        {
                            "attr": key,
                            "old_value": getattr(existing_standing, key),
                            "new_value": value,
                        }
                    )
                    setattr(existing_standing, key, value)

            if changes:
                session.add(existing_standing)
                session.commit()
                logger.debug(
                    f"Standing updated : {existing_standing.id}"
                    + f" | Changes : {','.join([f'{change['attr']}' for change in changes])}"
                )

            return existing_standing

        new_standing = cls(**standing_data)
        session.add(new_standing)
        session.commit()
        logger.debug(f"Standing added: {new_standing.id}")

        return new_standing


class DuelRound(DBDuel, table=True):
    __tablename__ = "duel_rounds"

    id: Optional[int] = Field(
        default=None,
        title="Round's ID",
        description="Unique identifier for the round.",
        primary_key=True,
    )
    tournament_id: int = Field(
        title="Tournament's ID",
        foreign_key="duel_tournaments.id",
        description="ID of the tournament the round is in.",
    )
    round: str = Field(
        title="Round's number or name depending on the source",
        description="Number of the round in the tournament.",
    )
    pairings: Dict[str, Dict[str, str]] = Field(
        sa_column=Column(JSON),
        title="Pairings",
        description="List of pairings for the round.",
    )

    tournament: Optional["DuelTournament"] = Relationship(back_populates="rounds")

    @classmethod
    def upsert(cls, session: Session, round_data: dict) -> "DuelRound":
        """Upserts a round into the database.

        Args:
            session (Session): The database session.
            round_data (dict): The round data to upsert.

        Returns:
            DuelRound: The upserted round.
        """
        statement = (
            select(cls)
            .where(cls.tournament_id == round_data["tournament_id"])
            .where(cls.round == round_data["round"])
        )
        existing_round = session.exec(statement).first()

        if existing_round:
            changes = []
            for key, value in round_data.items():
                if getattr(existing_round, key) != value:
                    changes.append(
                        {
                            "attr": key,
                            "old_value": getattr(existing_round, key),
                            "new_value": value,
                        }
                    )
                    setattr(existing_round, key, value)

            if changes:
                session.add(existing_round)
                session.commit()
                logger.debug(
                    f"Round updated : {existing_round.id}"
                    + f" | Changes : {','.join([f'{change['attr']}' for change in changes])}"
                )

            return existing_round

        new_round = cls(**round_data)
        session.add(new_round)
        session.commit()
        logger.debug(f"Round added: {new_round.id}")

        return new_round


class DuelDecklist(Decklist):
    sideboard_or_commandzone: str = "commandzone"
