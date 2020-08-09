#!/usr/bin/python3
"""This is the place class"""
from models.review import Review
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
""" from models.amenity import Amenity """

if models.storage_t == "db":
    place_amenity = Table(
        'place_amenity', Base.metadata,
        Column('place_id', String(60), ForeignKey(
            'places.id'), primary_key=True, nullable=False),
        Column('amenity_id', String(60), ForeignKey(
            'amenities.id'), primary_key=True, nullable=False)
    )
else:
    place_amenity = []


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
            city_id: city id
            user_id: user id
            name: name input
            description: string of description
            number_rooms: number of room in int
            number_bathrooms: number of bathrooms in int
            max_guest: maximum guest in int
            price_by_night:: pice for a staying in int
            latitude: latitude in flaot
            longitude: longitude in float
            amenity_ids: list of Amenity ids
    """
    if models.storage_t == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        reviews = relationship('Review', backref="place",
                               cascade="all, delete-orphan")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)

        @property
        def reviews(self):
            """Return list of reviews by an specific place
            """
            revs = []
            for rev in models.storage.all(Review).values():
                if rev.place_id == self.id:
                    revs.append(rev)
            return revs

    elif os.getenv('HBNB_TYPE_STORAGE') == 'file':
        @property
        def amenities(self):
            """Return list of amenities by an specific place
            """
            amenities_list = []
            for amen in self.amenity_ids:
                if amen == self.id:
                    amenities_list.append(amen)
            return amenities_list

        @amenities.setter
        def amenities(self, amen):
            """Set amenities"""
            if amen.__class__.__name__ == 'Amenity':
                self.amenity_ids.append(amen)

        @property
        def reviews(self):
            """Return a list of reviews by an specific place
            """
            reviews_list = []
            list_all = models.storage.all(Review)
            for review in list_all:
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list
