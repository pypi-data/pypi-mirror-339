import os
import unittest

from pychemstation.control.controllers import CommunicationController
from tests.constants import room


class TestComm(unittest.TestCase):
    """
    These tests should always work with an online controller.
    """

    def setUp(self):
        num = 254
        self.cs_dirs, self.data_dirs = room(num)
        self.comm = CommunicationController(comm_dir=self.cs_dirs[0])

    def test_load_dirs(self):
        meth, seq, data_dirs = self.comm.get_chemstation_dirs()
        data_dirs = [d.upper() for d in data_dirs]
        self.assertEqual(
            os.path.normpath(meth.upper()), os.path.normpath(self.cs_dirs[1].upper())
        )
        self.assertEqual(
            os.path.normpath(seq.upper()), os.path.normpath(self.cs_dirs[2].upper())
        )
        for data_dir in self.data_dirs:
            self.assertTrue(os.path.isdir(data_dir))


if __name__ == "__main__":
    unittest.main()
