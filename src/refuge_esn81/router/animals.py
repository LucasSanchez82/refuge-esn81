from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from refuge_esn81.database.database import get_db
from refuge_esn81.schemas.animalSchema import AnimalCreate as Animal
from refuge_esn81.services.animalService import AnimalService

animalsRouter = APIRouter(prefix="/animals", tags=["animals"])

@animalsRouter.get("/", response_model=list[Animal])
async def get_animals(db: Session = Depends(get_db)):
    service = AnimalService()
    return service.get_animals(db)

@animalsRouter.post('/', response_model=Animal)
async def create_animals(animal : Animal , db: Session = Depends(get_db)):
    service = AnimalService()
    return service.create_animal(db,animal)

