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


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
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
class TestYGetCountnoitems(unittest.TestCase):
    """Test count and get no items"""

    def setUp(self):
        """SetUp Tests"""
        storage = FileStorage()
        for obj in storage.all().values():
            storage.delete(obj)
        storage.save()

    def test_a_count_no_items(self):
        """Test count with 0 items"""
        storage = FileStorage()
        actual = 0
        db_objs = storage.all(self)
        self.assertEqual(0, len(db_objs))
        count = storage.count()
        self.assertEqual(0, count)

    def test_b_get_no_items(self):
        """Test get with 0 items"""
        storage = FileStorage()
        get = storage.get(User, 123)
        self.assertEqual(None, get)


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestZCountGet(unittest.TestCase):
    """Test get and count ith items"""

    def tearDown(self):
        """Execute after each test"""
        storage = FileStorage()
        for obj in storage.all().values():
            storage.delete(obj)
        storage.save()

    def setUp(self):
        """Set Up before each test"""
        storage = FileStorage()
        self.amenity = Amenity()
        self.amenity.name = 'test'
        self.amenity.save()
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'San_Mateo'
        self.city.state_id = self.state.id
        self.city.save()
        self.user = User()
        self.user.first_name = 'test'
        self.user.last_name = 'test'
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()
        self.place = Place()
        self.place.city_id = self.city.id
        self.place.user_id = self.user.id
        self.place.name = 'test_place'
        self.place.description = 'test_description'
        self.place.number_rooms = 2
        self.place.number_bathrooms = 1
        self.place.max_guest = 4
        self.place.price_by_night = 100
        self.place.latitude = 120.12
        self.place.longitude = 101.4
        self.place.save()
        self.review = Review()
        self.review.place_id = self.city.id
        self.review.user_id = self.user.id
        self.review.save()

    def test_a_get(self):
        """checks get method with class and id inputs"""
        storage = FileStorage()
        duplicate = storage.get(Amenity, self.amenity.id)
        expected = self.amenity.id
        actual = duplicate.id
        self.assertEqual(expected, actual)
        duplicate = storage.get(State, self.state.id)
        expected = self.state.id
        actual = duplicate.id
        self.assertEqual(expected, actual)
        duplicate = storage.get(City, self.city.id)
        expected = self.city.id
        actual = duplicate.id
        self.assertEqual(expected, actual)
        duplicate = storage.get(User, self.user.id)
        expected = self.user.id
        actual = duplicate.id
        self.assertEqual(expected, actual)
        duplicate = storage.get(Place, self.place.id)
        expected = self.place.id
        actual = duplicate.id
        self.assertEqual(expected, actual)
        duplicate = storage.get(Review, self.review.id)
        expected = self.review.id
        actual = duplicate.id
        self.assertEqual(expected, actual)

    def test_b_count_id(self):
        """checks count method by id"""
        storage = FileStorage()
        count = storage.count(Amenity)
        self.assertEqual(1, count)
        count = storage.count(State)
        self.assertEqual(1, count)
        count = storage.count(City)
        self.assertEqual(1, count)
        count = storage.count(User)
        self.assertEqual(1, count)
        count = storage.count(Place)
        self.assertEqual(1, count)
        count = storage.count(Review)
        self.assertEqual(1, count)

    def test_c_count(self):
        """checks count method"""
        storage = FileStorage()
        count = storage.count()
        self.assertEqual(6, count)
