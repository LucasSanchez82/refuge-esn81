from refuge_esn81.services.animalService import AnimalService
from src.refuge_esn81.models.animal import Animal
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from refuge_esn81.database.database import get_db

animalsRouter = APIRouter(prefix="/animals", tags=["animals"])

@animalsRouter.get("/", response_model=list[dict])
async def get_animals(db: Session = Depends(get_db)):
    service = AnimalService()
    return service.get_animals(db)
