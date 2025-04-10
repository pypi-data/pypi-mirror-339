import subprocess
from pathlib import Path


class GithubUtils:
    @staticmethod
    def clone_or_update_repo(repo_url: str, destination_path: Path) -> None:
        """Clone or update the GitHub repository at the specified URL.

        Args:
            repo_url (str): The URL of the GitHub repository to clone or update.
            destination_path (Path): The path where the repository will be cloned or updated.
        """
        if not destination_path.exists():
            subprocess.run(["git", "clone", repo_url, destination_path])

        else:
            subprocess.run(["git", "-C", destination_path, "pull"])
