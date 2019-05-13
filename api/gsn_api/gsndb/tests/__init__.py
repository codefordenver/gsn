import unittest

def suite():   
    return unittest.TestLoader().discover("gsndb.tests", pattern="*.py")