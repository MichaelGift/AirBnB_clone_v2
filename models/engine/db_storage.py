"""
Houses the DBStorage class
"""
import models
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review,
           "State": State, "User": User
           }


class DBStorage:
    """Connects and Interacts with the MYSQL DB"""

    __engine = None
    __session = None

    def __init__(self):
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query current db session based on search parameters"""
        result = {}
        for item in classes:
            if cls is None or cls is classes[item] or cls is item:
                objs = self.__session.query(classes[item]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    result[key] = obj
        return result

    def new(self, obj):
        """Add new object to current db session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from current db session if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Re/Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = (sessionmaker
                           (bind=self.__engine, expire_on_commit=False))
        Session = scoped_session(session_factory)
        self.__session = Session
