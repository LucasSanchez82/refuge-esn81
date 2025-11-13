from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from refuge_esn81.database.database import get_db
from refuge_esn81.schemas.animalSchema import Animal, AnimalCreate
from refuge_esn81.services.animalService import AnimalService

animalsRouter = APIRouter(prefix="/api/animals", tags=["animals"])

@animalsRouter.get(
    "/",
    response_model=list[Animal],
    summary="Get all animals",
    description="Retrieve a list of all animals in the refuge with their details and species information",
    response_description="List of animals with their complete information"
)
async def get_animals(db: Session = Depends(get_db)):
    """
    Get all animals from the refuge.

    Returns:
        List of animals with the following information:
        - **id**: Unique identifier
        - **name**: Animal's name
        - **age**: Animal's age (optional)
        - **gender**: Animal's gender
        - **description**: Additional details about the animal (optional)
        - **photo_url**: URL to animal's photo (optional)
        - **species_id**: ID of the species
        - **species**: Complete species information
    """
    service = AnimalService()
    return service.get_animals(db)

@animalsRouter.post(
    '/',
    response_model=Animal,
    summary="Create a new animal",
    description="Add a new animal to the refuge database",
    response_description="The created animal with its assigned ID",
    status_code=201
)
async def create_animals(animal: Animal, db: Session = Depends(get_db)):
    """
    Create a new animal in the refuge.

    Args:
        animal: Animal data including:
        - **name**: Animal's name (required)
        - **age**: Animal's age (optional)
        - **gender**: Animal's gender (required)
        - **description**: Additional details (optional)
        - **photo_url**: URL to photo (optional)
        - **species_id**: ID of the species (required)

    Returns:
        The created animal with all its information
    """
    service = AnimalService()
    return service.create_animal(db, animal)

