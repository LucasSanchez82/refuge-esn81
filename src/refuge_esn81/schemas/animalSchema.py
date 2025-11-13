from typing import Optional
from pydantic import BaseModel, Field
from refuge_esn81.schemas.speciesSchema import Species

class AnimalBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    species_id: int

class AnimalCreate(AnimalBase):
    """Schema for creating a new animal"""
    pass

class Animal(AnimalBase):
    """Schema for animal with ID and species information"""
    id: int
    # à compléter
    species: Species

    class Config:
        from_attributes = True
