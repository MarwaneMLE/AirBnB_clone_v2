#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City
from os import getenv

class State(BaseModel):
    """ State class """
    __tablename__ = "states"

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(127), nullable=False)
        cities = relationship(
            "City", backref="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """
            returns the list of City instances
            with state_id equals to the current State.id
            """
            city_list = []
            city_dict = storage.all(City)

            for city in city_dict.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
