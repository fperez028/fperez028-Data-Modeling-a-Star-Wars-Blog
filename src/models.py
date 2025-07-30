from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "favorites": [fav.serialize() for fav in self.favorites],
        }

class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=True)
    mass: Mapped[float] = mapped_column(Float, nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    homeworld: Mapped[str] = mapped_column(String(200), nullable=True)  # store URL or FK

    favorites = relationship("Favorite", back_populates="character", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    population: Mapped[Float] = mapped_column(Float, nullable=True)
    diameter: Mapped[Float] = mapped_column(Float, nullable=True)
    rotation_period: Mapped[Float] = mapped_column(Float, nullable=True)
    orbital_period: Mapped[Float] = mapped_column(Float, nullable=True)
    gravity: Mapped[str] = mapped_column(String(20), nullable=True)
    surface_water: Mapped[Float] = mapped_column(Float, nullable=True)

    favorites = relationship("Favorite", back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "surface_water": self.surface_water,
        }

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    vehicle_class: Mapped[str] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(200), nullable=True)
    cost_in_credits: Mapped[Float] = mapped_column(Float, nullable=True)
    length: Mapped[Float] = mapped_column(Float, nullable=True)
    crew: Mapped[str] = mapped_column(String(50), nullable=True)
    passengers: Mapped[str] = mapped_column(String(50), nullable=True)
    max_atmosphering_speed: Mapped[str] = mapped_column(String(50), nullable=True)
    cargo_capacity: Mapped[Float] = mapped_column(Float, nullable=True)
    consumables: Mapped[str] = mapped_column(String(50), nullable=True)

    favorites = relationship("Favorite", back_populates="vehicle", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
        }

class Favorite(db.Model):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=True)

    user = relationship("User", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    vehicle = relationship("Vehicle", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize() if self.character else None,
            "planet": self.planet.serialize() if self.planet else None,
            "vehicle": self.vehicle.serialize() if self.vehicle else None,
        }
