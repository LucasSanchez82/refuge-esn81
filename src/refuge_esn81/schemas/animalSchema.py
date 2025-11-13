from typing import Optional
from pydantic import BaseModel
from refuge_esn81.schemas.speciesSchema import Species

class AnimalBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    species_id: int

class AnimalCreate(AnimalBase):
    pass

class Animal(AnimalBase):
    id: int
    # à compléter
    species: Species

    class Config:
        from_attributes = True
