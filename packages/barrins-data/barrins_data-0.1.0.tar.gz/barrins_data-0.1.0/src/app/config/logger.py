import inspect
import logging
import re
from enum import Enum
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir()

SENSITIVE_KEYS = {"password", "passwd", "token", "apikey", "secret", "auth"}


def mask_sensitive_data(data):
    """Remplace les valeurs des clés sensibles par '***HIDDEN***'."""
    if isinstance(data, dict):
        return {
            k: "***HIDDEN***" if k.lower() in SENSITIVE_KEYS else v
            for k, v in data.items()
        }
    elif isinstance(data, str):
        for key in SENSITIVE_KEYS:
            data = re.sub(
                rf"({key}\s*=\s*)(['\"]?)([^'\"]+)(['\"]?)",
                r"\1\2***HIDDEN***\4",
                data,
                flags=re.IGNORECASE,
            )
    return data


def get_caller_info():
    """Récupère les arguments de la fonction appelante tout en masquant les valeurs sensibles."""
    frame = inspect.currentframe().f_back.f_back  # On remonte à l'appel réel
    func_name = frame.f_code.co_name
    args, _, _, values = inspect.getargvalues(frame)

    masked_values = mask_sensitive_data({arg: values[arg] for arg in args})
    arg_str = ", ".join(f"{arg}={masked_values[arg]}" for arg in masked_values)
    return f"Exception dans {func_name}({arg_str})"


class CustomFormatter(logging.Formatter):
    """Formatter personnalisé qui affiche plus d'infos pour WARNING et ERROR."""

    basic_format = "[%(asctime)s] - %(levelname)s - %(message)s"
    detailed_format = "[%(asctime)s] - %(levelname)s - Module %(module)s - Function %(funcName)s - Line %(lineno)d - Message: %(message)s"

    def format(self, record):
        log_format = (
            self.detailed_format
            if record.levelno >= logging.WARNING
            else self.basic_format
        )
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


class LogErrors(Enum):
    """Enumération des niveaux de log pour les erreurs."""

    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL


# Création du logger
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.DEBUG)  # Changer en INFO ou WARNING en production

# Console handler (affiche les logs dans la console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
logger.addHandler(console_handler)

# File handler (enregistre les logs dans un fichier, rotation automatique)
for level in LogErrors:
    file_handler = RotatingFileHandler(
        f"{LOG_DIR}/{level.name}.log", maxBytes=5_000_000, backupCount=3
    )
    file_handler.setFormatter(CustomFormatter())
    file_handler.setLevel(level.value)
    logger.addHandler(file_handler)
