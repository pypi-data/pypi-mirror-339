from fastapi import APIRouter, BackgroundTasks, Header, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from src.app.config.settings import settings
from src.app.models import CARD_DATABASE
from src.app.models.tables import Card
from src.app.scripts.card_update import run_update

router = APIRouter()


@router.post("/update-cards", status_code=202, tags=["Maintenance"])
async def update_cards(
    background_tasks: BackgroundTasks,
    authorization: str = Header(...),
):
    """Endpoint sécurisé pour lancer la mise à jour des cartes MTG."""
    if authorization != f"Bearer {settings.secret_token}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    background_tasks.add_task(run_update)

    return {"message": "Mise à jour des cartes lancée en arrière-plan."}


@router.get(
    "/cards/id/{card_uuid}",
    response_model=Card,
    summary="Retrieve card details by UUID",
    description=(
        "Fetch detailed information about a Magic: The Gathering card using its unique identifier (ID). "
        "The UUID corresponds to the unique identifier provided by Scryfall."
    ),
    response_description="Details of the requested card in JSON format",
)
def get_card_id(card_uuid: str):
    try:
        with CARD_DATABASE.get_session() as session:
            statement = select(Card).where(Card.id == card_uuid)
            card = session.exec(statement).first()
            return card.to_dict()
    except NoResultFound:
        HTTPException(status_code=404, detail="Card not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
