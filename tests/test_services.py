"""
Unit tests for Service layer
"""
import pytest
from sqlalchemy.orm import Session

from refuge_esn81.services.animalService import AnimalService
from refuge_esn81.services.specieService import SpecieService
from refuge_esn81.schemas.animalSchema import AnimalCreate
from refuge_esn81.schemas.speciesSchema import SpeciesCreate


class TestSpecieService:
    """Tests for SpecieService"""

    def test_create_specie(self, db_session):
        """Test creating a species through service"""
        service = SpecieService()
        specie_data = SpeciesCreate(name="Dog")

        result = service.create_specie(db_session, specie_data)

        assert result.id is not None
        assert result.name == "Dog"
        assert isinstance(result.id, int)

    def test_get_species_empty(self, db_session):
        """Test getting species when database is empty"""
        service = SpecieService()

        result = service.get_species(db_session)
        species_list = result.all()

        assert species_list == []

    def test_get_species_with_data(self, db_session, sample_species):
        """Test getting species with data"""
        service = SpecieService()

        result = service.get_species(db_session)
        species_list = result.all()

        assert len(species_list) == 1
        assert species_list[0].name == "Dog"
        assert species_list[0].id == sample_species.id

    def test_get_species_multiple(self, db_session):
        """Test getting multiple species"""
        service = SpecieService()

        # Create multiple species
        species_names = ["Dog", "Cat", "Bird"]
        for name in species_names:
            service.create_specie(db_session, SpeciesCreate(name=name))

        result = service.get_species(db_session)
        species_list = result.all()

        assert len(species_list) == 3
        names = [s.name for s in species_list]
        assert set(names) == set(species_names)

    def test_create_specie_returns_orm_model(self, db_session):
        """Test that create_specie returns a proper ORM model"""
        from refuge_esn81.models.species import Species

        service = SpecieService()
        specie_data = SpeciesCreate(name="Rabbit")

        result = service.create_specie(db_session, specie_data)

        assert isinstance(result, Species)
        assert hasattr(result, 'id')
        assert hasattr(result, 'name')


class TestAnimalService:
    """Tests for AnimalService"""

    def test_create_animal(self, db_session, sample_species):
        """Test creating an animal through service"""
        service = AnimalService()
        animal_data = AnimalCreate(
            name="Max",
            age=3,
            gender="Male",
            description="Friendly dog",
            photo_url="http://example.com/max.jpg",
            species_id=sample_species.id
        )

        result = service.create_animal(db_session, animal_data)

        assert result.id is not None
        assert result.name == "Max"
        assert result.age == 3
        assert result.gender == "Male"
        assert result.species_id == sample_species.id
        assert isinstance(result.id, int)

    def test_create_animal_minimal_data(self, db_session, sample_species):
        """Test creating animal with minimal required data"""
        service = AnimalService()
        animal_data = AnimalCreate(
            name="Buddy",
            gender="Male",
            species_id=sample_species.id
        )

        result = service.create_animal(db_session, animal_data)

        assert result.name == "Buddy"
        assert result.gender == "Male"
        assert result.age is None
        assert result.description is None
        assert result.photo_url is None

    def test_get_animals_empty(self, db_session):
        """Test getting animals when database is empty"""
        service = AnimalService()

        result = service.get_animals(db_session)

        assert result == []

    def test_get_animals_with_data(self, db_session, sample_animal):
        """Test getting animals with data"""
        service = AnimalService()

        result = service.get_animals(db_session)

        assert len(result) == 1
        assert result[0].name == "Max"
        assert result[0].id == sample_animal.id

    def test_get_animals_multiple(self, db_session, sample_species):
        """Test getting multiple animals"""
        from refuge_esn81.models.animal import Animal

        service = AnimalService()

        # Create multiple animals directly
        animals_data = [
            Animal(name="Max", gender="Male", species_id=sample_species.id),
            Animal(name="Bella", gender="Female", species_id=sample_species.id),
            Animal(name="Charlie", gender="Male", species_id=sample_species.id),
        ]

        for animal in animals_data:
            db_session.add(animal)
        db_session.commit()

        result = service.get_animals(db_session)

        assert len(result) == 3
        names = [a.name for a in result]
        assert set(names) == {"Max", "Bella", "Charlie"}

    def test_get_animals_pagination_skip(self, db_session, sample_species):
        """Test pagination with skip parameter"""
        from refuge_esn81.models.animal import Animal

        service = AnimalService()

        # Create 5 animals
        for i in range(5):
            animal = Animal(name=f"Animal{i}", gender="Male", species_id=sample_species.id)
            db_session.add(animal)
        db_session.commit()

        # Skip first 2 animals
        result = service.get_animals(db_session, skip=2)

        assert len(result) == 3

    def test_get_animals_pagination_limit(self, db_session, sample_species):
        """Test pagination with limit parameter"""
        from refuge_esn81.models.animal import Animal

        service = AnimalService()

        # Create 5 animals
        for i in range(5):
            animal = Animal(name=f"Animal{i}", gender="Male", species_id=sample_species.id)
            db_session.add(animal)
        db_session.commit()

        # Limit to 3 animals
        result = service.get_animals(db_session, limit=3)

        assert len(result) == 3

    def test_get_animals_pagination_skip_and_limit(self, db_session, sample_species):
        """Test pagination with both skip and limit"""
        from refuge_esn81.models.animal import Animal

        service = AnimalService()

        # Create 10 animals
        for i in range(10):
            animal = Animal(name=f"Animal{i}", gender="Male", species_id=sample_species.id)
            db_session.add(animal)
        db_session.commit()

        # Skip 3 and limit to 4
        result = service.get_animals(db_session, skip=3, limit=4)

        assert len(result) == 4

    def test_create_animal_returns_orm_model(self, db_session, sample_species):
        """Test that create_animal returns a proper ORM model"""
        from refuge_esn81.models.animal import Animal

        service = AnimalService()
        animal_data = AnimalCreate(
            name="Test",
            gender="Female",
            species_id=sample_species.id
        )

        result = service.create_animal(db_session, animal_data)

        assert isinstance(result, Animal)
        assert hasattr(result, 'id')
        assert hasattr(result, 'name')
        assert hasattr(result, 'species')


class TestServiceIntegration:
    """Integration tests between services"""

    def test_create_animal_with_species_from_service(self, db_session):
        """Test creating animal using species created through service"""
        specie_service = SpecieService()
        animal_service = AnimalService()

        # Create species
        species = specie_service.create_specie(db_session, SpeciesCreate(name="Cat"))

        # Create animal with that species
        animal_data = AnimalCreate(
            name="Mittens",
            gender="Female",
            species_id=species.id
        )
        animal = animal_service.create_animal(db_session, animal_data)

        assert animal.species_id == species.id
        assert animal.species.name == "Cat"

    def test_multiple_animals_one_species(self, db_session):
        """Test creating multiple animals for one species"""
        specie_service = SpecieService()
        animal_service = AnimalService()

        # Create one species
        species = specie_service.create_specie(db_session, SpeciesCreate(name="Dog"))

        # Create multiple animals
        animal_names = ["Max", "Bella", "Charlie"]
        for name in animal_names:
            animal_data = AnimalCreate(
                name=name,
                gender="Male",
                species_id=species.id
            )
            animal_service.create_animal(db_session, animal_data)

        # Verify all animals exist
        animals = animal_service.get_animals(db_session)
        assert len(animals) == 3

        # Verify all have same species
        for animal in animals:
            assert animal.species_id == species.id
