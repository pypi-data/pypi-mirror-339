from typing import Type

import src.app.models.tables.duel_tables as tables
from src.app.models import DUEL_DATABASE
from src.app.mtg_formats.base_format import BaseFormat


class DuelCommander(BaseFormat):
    database: object = DUEL_DATABASE
    tournament: Type[tables.DuelTournament] = tables.DuelTournament
    deck: Type[tables.DuelDeck] = tables.DuelDeck
    decklist: Type[tables.DuelDecklist] = tables.DuelDecklist
    player: Type[tables.DuelPlayer] = tables.DuelPlayer
    rounds: Type[tables.DuelRound] = tables.DuelRound
    standings: Type[tables.DuelStanding] = tables.DuelStanding
