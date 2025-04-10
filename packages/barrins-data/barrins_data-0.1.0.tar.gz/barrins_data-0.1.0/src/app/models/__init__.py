from sqlmodel import Session, SQLModel, create_engine

from src.app.config.settings import settings
from src.app.models.databases import DBCards, DBDuel

# Multiple databases can be handled following this GitHub's comment:
# https://github.com/fastapi/sqlmodel/issues/264#issuecomment-1309867468


class DatabaseInitiator:
    """
    This class is used to initialize the database connection.
    It uses the settings from the settings module to establish the connection.

    ## Methods:
    - __init__(SQLModel, str): Initializes the database connection to a specific sqlite3 file.
    - create_database_and_tables(): Creates the database and the tables if they do not exist.
    - get_session(): Returns a Session object to communicate with the database.
    """

    def __init__(self, database: SQLModel, db_name: str) -> None:
        self.database = database
        self.sqlite_uri = f"sqlite:///{settings.get_db_path(db_name)}"
        self.engine = create_engine(self.sqlite_uri)

    def create_database_and_tables(self) -> None:
        self.database.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Returns a new SQLAlchemy session."""
        return Session(self.engine)


CARD_DATABASE = DatabaseInitiator(DBCards, "cards")
DUEL_DATABASE = DatabaseInitiator(DBDuel, "duel")


def init_models() -> None:
    """Initialize all models in the application."""
    CARD_DATABASE.create_database_and_tables()
    DUEL_DATABASE.create_database_and_tables()
