import unittest
import pydoc
import pydoc_utils

class TestUtils(unittest.TestCase):
    def test_getmodules(self):
        ms = pydoc_utils.getmodules()
        self.assertTrue('time' in ms)

    def test_getclasses(self):
        cs = pydoc_utils.getclasses('time')
        self.assertEqual(cs[0][0] , 'struct_time')

    def test_getfuncs(self):
        fs = pydoc_utils.getfuncs('time')
        self.assertTrue('strptime' in dict(fs))
