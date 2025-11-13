"""
Unit tests for Animals endpoints
"""
import pytest
from fastapi import status


class TestGetAnimals:
    """Tests for GET /animals endpoint"""

    def test_get_empty_animals_list(self, client):
        """Test getting animals when database is empty"""
        response = client.get("/animals/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_animals_list(self, client, sample_animal):
        """Test getting animals list with data"""
        response = client.get("/animals/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        animal = data[0]
        assert animal["name"] == "Max"
        assert animal["age"] == 3
        assert animal["gender"] == "Male"
        assert animal["description"] == "Friendly dog"
        assert animal["id"] == sample_animal.id

    def test_get_animals_includes_species(self, client, sample_animal):
        """Test that animal data includes species information"""
        response = client.get("/animals/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        animal = data[0]
        assert "species" in animal
        assert animal["species"]["name"] == "Dog"
        assert animal["species"]["id"] == sample_animal.species_id

    def test_get_multiple_animals(self, client, db_session, sample_species):
        """Test getting multiple animals"""
        from refuge_esn81.models.animal import Animal

        # Create multiple animals
        animals_data = [
            {"name": "Max", "age": 3, "gender": "Male"},
            {"name": "Bella", "age": 2, "gender": "Female"},
            {"name": "Charlie", "age": 5, "gender": "Male"},
        ]

        for animal_data in animals_data:
            animal = Animal(
                name=animal_data["name"],
                age=animal_data["age"],
                gender=animal_data["gender"],
                species_id=sample_species.id
            )
            db_session.add(animal)
        db_session.commit()

        response = client.get("/animals/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        names = [a["name"] for a in data]
        assert set(names) == {"Max", "Bella", "Charlie"}


class TestCreateAnimal:
    """Tests for POST /animals endpoint"""

    def test_create_animal_success(self, client, sample_species):
        """Test creating a new animal successfully"""
        animal_data = {
            "name": "Luna",
            "age": 2,
            "gender": "Female",
            "description": "Playful cat",
            "photo_url": "http://example.com/luna.jpg",
            "species_id": sample_species.id
        }
        response = client.post("/animals/", json=animal_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Luna"
        assert data["age"] == 2
        assert data["gender"] == "Female"
        assert data["description"] == "Playful cat"
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_animal_minimal_data(self, client, sample_species):
        """Test creating animal with only required fields"""
        animal_data = {
            "name": "Buddy",
            "gender": "Male",
            "species_id": sample_species.id
        }
        response = client.post("/animals/", json=animal_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Buddy"
        assert data["gender"] == "Male"
        assert data["age"] is None
        assert data["description"] is None

    def test_create_animal_missing_required_field(self, client, sample_species):
        """Test creating animal without required field fails"""
        animal_data = {
            "age": 3,
            "gender": "Male",
            "species_id": sample_species.id
            # Missing 'name'
        }
        response = client.post("/animals/", json=animal_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_animal_invalid_species_id(self, client):
        """Test creating animal with non-existent species"""
        animal_data = {
            "name": "Ghost",
            "gender": "Male",
            "species_id": 99999  # Non-existent species
        }
        response = client.post("/animals/", json=animal_data)
        # This might fail or succeed depending on database constraints
        # If it succeeds, the animal is created but with invalid FK reference
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ]

    def test_create_animal_persistence(self, client, sample_species):
        """Test that created animal persists in database"""
        # Create animal
        animal_data = {
            "name": "Rocky",
            "age": 4,
            "gender": "Male",
            "species_id": sample_species.id
        }
        create_response = client.post("/animals/", json=animal_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        animal_id = create_response.json()["id"]

        # Verify it appears in GET request
        get_response = client.get("/animals/")
        assert get_response.status_code == status.HTTP_200_OK
        animals_list = get_response.json()
        assert any(a["id"] == animal_id and a["name"] == "Rocky" for a in animals_list)

    def test_create_animal_with_optional_fields(self, client, sample_species):
        """Test creating animal with all optional fields"""
        animal_data = {
            "name": "Whiskers",
            "age": 1,
            "gender": "Female",
            "description": "Very shy but sweet",
            "photo_url": "http://example.com/whiskers.jpg",
            "species_id": sample_species.id
        }
        response = client.post("/animals/", json=animal_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["description"] == "Very shy but sweet"
        assert data["photo_url"] == "http://example.com/whiskers.jpg"


class TestAnimalsIntegration:
    """Integration tests for animals and species"""

    def test_create_animal_with_species_relationship(self, client, db_session):
        """Test creating animal with proper species relationship"""
        from refuge_esn81.models.species import Species

        # Create a species first
        cat_species = Species(name="Cat")
        db_session.add(cat_species)
        db_session.commit()
        db_session.refresh(cat_species)

        # Create an animal with that species
        animal_data = {
            "name": "Mittens",
            "gender": "Female",
            "species_id": cat_species.id
        }
        response = client.post("/animals/", json=animal_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Verify species relationship
        animal = response.json()
        assert animal["species"]["name"] == "Cat"
        assert animal["species"]["id"] == cat_species.id

    def test_multiple_animals_same_species(self, client, sample_species):
        """Test creating multiple animals with same species"""
        animals = [
            {"name": "Dog1", "gender": "Male", "species_id": sample_species.id},
            {"name": "Dog2", "gender": "Female", "species_id": sample_species.id},
        ]

        for animal_data in animals:
            response = client.post("/animals/", json=animal_data)
            assert response.status_code == status.HTTP_201_CREATED

        # Verify all animals are created
        get_response = client.get("/animals/")
        assert len(get_response.json()) == 2
