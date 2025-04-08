import sys
import os
import unittest

current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, "..")

sys.path.append(os.path.normpath(src_dir))

from netora.connection import check_connection
from netora.validation import validate_ip

target_ip = "8.8.8.8"

class TestConnection(unittest.TestCase):

    def test_check_connection(self):
        try:
            check_connection(target_ip)
            result = True

        except SystemExit: 
            result = False
        self.assertTrue(result)

    def test_validate_ip(self):
        self.assertTrue(validate_ip("8.8.8.8"))
        self.assertFalse(validate_ip("256.256.256.256"))
        self.assertFalse(validate_ip("abcd"))

if __name__ == "__main__":
    unittest.main()