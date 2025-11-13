from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from refuge_esn81.database.database import get_db
from src.refuge_esn81.models.animal import Animal

animalsRouter = APIRouter(prefix="/animals", tags=["animals"])


@animalsRouter.get("/", response_model=list[dict])
def get_animals(db: Session = Depends(get_db)):
    animals = db.query(Animal).all()
    if not animals:
        raise HTTPException(status_code=404, detail="Aucun animal trouvé.")

    return [
        {
            "id": a.id,
            "name": a.name,
            "age": a.age,
            "gender": a.gender,
            "description": a.description,
            "photo_url": a.photo_url,
            "species_id": a.species_id
        }
        for a in animals
    ]