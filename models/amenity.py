#!/usr/bin/python3
"""This is the amenity class"""
import models
from models.base_model import BaseModel, Base
from models.place import Place
from models.place import place_amenity
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """This is the class for Amenity
    Attributes:
        name: input name
    """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary=place_amenity)
    else:
        name = ""
        place_id = []

    def to_dict(self):
        """
        return dict representation
        """
        obj = super().to_dict()
        return obj
