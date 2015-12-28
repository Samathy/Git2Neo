import unittest
from git_to_Neo4J import *

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        return


    def test_generate_match(self):
        match = "MATCH (Person(name:'Joe Blogs')) RETURN (Person)"
        self.assertEqual(generateMatch("Person","name","Joe Blogs"),match)

    def test_generate_add(self):
        add = "CREATE (x: TEST(name: 'Joe Blogs', Age: '20', Job: 'Engineer', )) RETURN (x)"
        self.assertEqual(generateAdd("TEST",[("name","Joe Blogs"),("Age","20"),("Job","Engineer")]),add)







if __name__ == '__main__':
    unittest.main()
