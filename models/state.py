#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City


class State(BaseModel):
    """ State class """
    __tablename__ = "states"
    name = Column(String(127), nullable=False)
    cities = relationship(
            "City", backref="state", cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        if models.storage_t == 'db':
            return self.cities
        else:
            return [city for city in models.storage.all(city).values()
                    if city.state_id == self.id]
