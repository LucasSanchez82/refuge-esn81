from sqlalchemy import Column, Integer, String, ForeignKey
from refuge_esn81.database.database import Base
from sqlalchemy.orm import relationship

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)
    gender = Column(String(50), nullable=False)
    description = Column(String(255))
    photo_url = Column(String(300))
    species_id = Column(Integer, ForeignKey("species.id"))

    # Relation : un animal appartient à une espèce
    species = relationship("Species", back_populates="animals")
