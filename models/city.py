#!/usr/bin/python3
""" City Module for HBNB project """

import models
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if models.storage_type == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade='all, delete, delete-orphan')
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a city object"""
        super().__init__(*args, **kwargs)
