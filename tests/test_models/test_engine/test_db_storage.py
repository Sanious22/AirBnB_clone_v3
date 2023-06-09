#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    def populate(self):
        """Add one of each class to the database"""
        state = State(name='Connecticut')
        state.save()
        city = City(state_id=state.id, name='New Haven')
        city.save()
        amenity = Amenity(name='Wi-Fi')
        amenity.save()
        user = User(email='postmaster@example.com', password='password')
        user.save()
        place = Place(city_id=city.id, user_id=user.id, name='Big Blue House')
        place.amenities.append(amenity)
        place.save()
        review = Review(place_id=place.id, user_id=user.id, text='Bad.')
        review.save()
        return [review, place, user, amenity, city, state]

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """test retrieving single objects"""
        objects = self.populate()
        for obj in objects:
            found = models.storage.get(type(obj), obj.id)
            self.assertIs(found, obj)
        for obj in objects:
            obj.delete()
            found = models.storage.get(type(obj), obj.id)
            self.assertIsNone(found)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_multi_argument(self):
        """ pass extra arguments to get """
        models.storage.close()
        models.storage = models.engine.db_storage.DBStorage()
        models.storage.reload()
        obj = self.populate()
        with self.assertRaises(TypeError):
            models.storage.get(type(obj[0]), obj[0].id, obj[1].id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_none(self):
        """ pass none arguments to get. """
        models.storage.close()
        models.storage = models.engine.db_storage.DBStorage()
        models.storage.reload()
        obj = self.populate()

        found = models.storage.get(type(obj[0]), None)
        self.assertEqual(found, None)
        with self.assertRaises(KeyError):
            models.storage.get(None, obj[0].id)
        with self.assertRaises(KeyError):
            models.storage.get(None, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """ test counting objects.
        Start with 6 and delete one then check repetedly until 0. """
        models.storage.close()
        models.storage = models.engine.db_storage.DBStorage()
        models.storage.reload()
        objects = self.populate()
        count = 6
        self.assertEqual(6, len(objects))
        for obj in objects:
            obj.delete()
            models.storage.save()
            count -= 1
            self.assertEqual(models.storage.count(), count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_bad(self):
        """ give count extra arguments. """
        with self.assertRaises(KeyError):
            models.storage.count("2")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_two_arg(self):
        """ give count extra arguments. """
        objects = self.populate()
        state = objects[0]
        with self.assertRaises(TypeError):
            models.storage.count(state, "idhere")
