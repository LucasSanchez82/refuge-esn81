from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from refuge_esn81.database.database import get_db
from refuge_esn81.schemas.animalSchema import Animal, AnimalCreate
from refuge_esn81.services.animalService import AnimalService

animalsRouter = APIRouter(prefix="/api/animals", tags=["animals"])

@animalsRouter.get("/", response_model=list[Animal])
async def get_animals(db: Session = Depends(get_db)):
    service = AnimalService()
    return service.get_animals(db)

@animalsRouter.post('/', response_model=Animal)
async def create_animals(animal: AnimalCreate, db: Session = Depends(get_db)):
    service = AnimalService()
    return service.create_animal(db, animal)
