from pydantic import BaseModel, Field

class SpeciesBase(BaseModel):
    name: str = Field(..., description="Name of the species", example="Dog")

class SpeciesCreate(SpeciesBase):
    """Schema for creating a new species"""
    pass

class Species(SpeciesBase):
    """Schema for species with ID"""
    id: int = Field(..., description="Unique identifier for the species", example=1)

    class Config:
        from_attributes = True