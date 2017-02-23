import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from proxypool.schedule import ValidityTester


class SchduleTestCase(unittest.TestCase):

    def setUp(self):
        self._tester = ValidityTester()

    def tearDown(self):
        pass

    def test_tester(self):
        fake_proxies = ['00.000.00.00:8000',
                        '01.000.00.00:8001',
                        '00.020.00.00:8002',
                        '00.000.30.00:8003']
        self._tester.set_raw_proxies(fake_proxies)
        self._tester.test()
        proxies = self._tester._usable_proxies
        assert proxies == []

if __name__ == '__main__':
    unittest.main()