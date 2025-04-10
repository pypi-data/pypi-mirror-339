import toml

with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f)

APP_NAME = pyproject["project"]["name"]
APP_VERSION = pyproject["project"]["version"]
