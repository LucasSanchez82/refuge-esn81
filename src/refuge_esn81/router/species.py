from fastapi import APIRouter, FastAPI, Depends, HTTPException
from refuge_esn81.schemas.speciesSchema import Species, SpeciesCreate
from sqlalchemy.orm import Session
from refuge_esn81.database.database import get_db
from refuge_esn81.services.specieService import SpecieService


speciesRouter = APIRouter(prefix="/api/species", tags=["species"])

@speciesRouter.get(
    "/",
    response_model=list[Species],
    summary="Get all species",
    description="Retrieve a list of all animal species available in the refuge system",
    response_description="List of all species"
)
async def get_species(db: Session = Depends(get_db)):
    """
    Get all species from the database.

    Returns:
        List of species with:
        - **id**: Unique identifier
        - **name**: Species name (e.g., Dog, Cat, Bird)
    """
    service = SpecieService()
    return service.get_species(db)

@speciesRouter.post(
    "/",
    response_model=Species,
    summary="Create a new species",
    description="Add a new animal species to the system",
    response_description="The created species with its assigned ID",
    status_code=201
)
def create_new_species(specie: SpeciesCreate, db: Session = Depends(get_db)):
    """
    Create a new species in the database.

    Args:
        specie: Species data including:
        - **name**: Species name (required)

    Returns:
        The created species with its ID
    """
    service = SpecieService()
    return service.create_specie(db, specie)