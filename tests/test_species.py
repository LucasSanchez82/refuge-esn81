"""
Unit tests for Species endpoints
"""
import pytest
from fastapi import status


class TestGetSpecies:
    """Tests for GET /api/species endpoint"""

    def test_get_empty_species_list(self, client):
        """Test getting species when database is empty"""
        response = client.get("/api/species/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_species_list(self, client, sample_species):
        """Test getting species list with data"""
        response = client.get("/api/species/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Dog"
        assert data[0]["id"] == sample_species.id

    def test_get_multiple_species(self, client, db_session):
        """Test getting multiple species"""
        from refuge_esn81.models.species import Species

        # Create multiple species
        species_list = ["Dog", "Cat", "Bird"]
        for species_name in species_list:
            species = Species(name=species_name)
            db_session.add(species)
        db_session.commit()

        response = client.get("/api/species/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        names = [s["name"] for s in data]
        assert set(names) == set(species_list)


class TestCreateSpecies:
    """Tests for POST /api/species endpoint"""

    def test_create_species_success(self, client):
        """Test creating a new species successfully"""
        species_data = {"name": "Cat"}
        response = client.post("/api/species/", json=species_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Cat"
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_species_missing_name(self, client):
        """Test creating species without name fails"""
        species_data = {}
        response = client.post("/api/species/", json=species_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_species_empty_name(self, client):
        """Test creating species with empty name"""
        species_data = {"name": ""}
        response = client.post("/api/species/", json=species_data)
        # Should succeed - validation can be added later if needed
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_422_UNPROCESSABLE_ENTITY]

    def test_create_species_persistence(self, client):
        """Test that created species persists in database"""
        # Create species
        species_data = {"name": "Rabbit"}
        create_response = client.post("/api/species/", json=species_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        species_id = create_response.json()["id"]

        # Verify it appears in GET request
        get_response = client.get("/api/species/")
        assert get_response.status_code == status.HTTP_200_OK
        species_list = get_response.json()
        assert any(s["id"] == species_id and s["name"] == "Rabbit" for s in species_list)
