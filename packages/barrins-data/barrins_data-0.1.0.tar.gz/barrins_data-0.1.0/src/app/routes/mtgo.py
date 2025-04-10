from fastapi import APIRouter, BackgroundTasks, Header, HTTPException

from src.app.config.settings import settings
from src.app.scripts.mtgo_update import run_update

router = APIRouter()


@router.post("/update_mtgo", status_code=202, tags=["Maintenance"])
async def update_mtgo(
    background_tasks: BackgroundTasks,
    authorization: str = Header(...),
):
    """Endpoint sécurisé pour lancer la mise à jour des données MTGO."""
    if authorization != f"Bearer {settings.secret_token}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    background_tasks.add_task(run_update)

    return {"message": "Mise à jour des tournois lancée en arrière-plan."}
