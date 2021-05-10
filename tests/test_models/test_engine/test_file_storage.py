#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
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
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))


@unittest.skipIf(models.storage_t == 'db', "not testing file storage")
class TestGetCountnoitems(unittest.TestCase):
    """Test count and get no items"""

    def setUp(self):
        """SetUp Tests"""
        storage = FileStorage()
        for obj in list(storage.all().values()):
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


@unittest.skipIf(models.storage_t == 'db', "not testing file storage")
class TestZCountGet(unittest.TestCase):
    """Test get and count ith items"""

    def tearDown(self):
        """Execute after each test"""
        storage = FileStorage()
        for obj in list(storage.all().values()):
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
