from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from refuge_esn81.database.database import get_db
from refuge_esn81.schemas.animalSchema import AnimalCreate
from src.refuge_esn81.services.animalService import AnimalService , Animal


animalsRouter = APIRouter(prefix="/animals", tags=["animals"])

# A compléter

@animalsRouter.post('/')
async def create_animals(animal : AnimalCreate , db: Session = Depends(get_db)):
    service = AnimalService()
    return service.create_animal(db,animal)

