#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
import json

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    try:
                        setattr(self, key, value)
                    except:
                        try:
                            if type(value) == list:
                                setattr(self, key, [v for v in value])
                        except:
                            pass
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        # print("to dict:\n\t", dir(self))
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if type(models.storage).__name__ != "FileStorage":
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict
        # new_dict = {}
        # for key in dir(self):
        #     conds = [key[:2] != '__',
        #              key != 'save',
        #              key != 'delete',
        #              key != 'to_dict'
        #              ]
        #     if all(conds):
        #         value = eval("self.{}".format(key))
        #         new_dict[key] = value
        # if "created_at" in new_dict:
        #     new_dict["created_at"] = new_dict["created_at"].strftime(time)
        # if "updated_at" in new_dict:
        #     new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        # new_dict["__class__"] = self.__class__.__name__
        # if "_sa_instance_state" in new_dict:
        #     del new_dict["_sa_instance_state"]
        # pla = "place_amenities"
        # if pla in new_dict:
        #     del new_dict[pla]
        # return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
