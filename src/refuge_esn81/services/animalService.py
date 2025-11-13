from sqlalchemy.orm import Session
from refuge_esn81.schemas.animalSchema import AnimalCreate
from refuge_esn81.models.animal import Animal

class AnimalService:
    def create_animal(self, db: Session, animal: AnimalCreate):
        # Crée l'objet Animal SQLAlchemy
        db_animal = Animal(
            name=animal.name,
            age=animal.age,
            gender=animal.gender,
            description=animal.description,
            photo_url=animal.photo_url,
            species_id=animal.species_id
        )
        db.add(db_animal)  # ajoute à la session
        db.commit()  # commit dans la base
        db.refresh(db_animal)  # récupère les champs générés (id, etc.)
        return db_animal  # retourne l'objet créé

    def get_animals(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Animal).offset(skip).limit(limit).all()