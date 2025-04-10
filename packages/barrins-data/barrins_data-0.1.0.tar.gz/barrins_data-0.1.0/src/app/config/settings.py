from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Barrin's API"
    db_folder: Path = Path(__file__).parent.parent / "databases"
    alembic_ini: Path = Path(__file__).parent.parent.parent.parent / "alembic.ini"
    secret_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_db_path(self, db_name: str) -> Path:
        """Returns the path to the database file based on the format key.

        Args:
            db_name (str): The database name to use when constructing the database path.

        Returns:
            Path: The path to the database file.
        """
        return self.db_folder / f"{db_name}.sqlite"


settings = Settings()
settings.db_folder.mkdir(parents=True, exist_ok=True)
