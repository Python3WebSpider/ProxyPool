import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from proxypool.db import RedisClient


class RedisClientTestCase(unittest.TestCase):

    def setUp(self):
        self._conn = RedisClient()

    def tearDown(self):
        self._conn.flush()

    def test_put_and_pop(self):
        self._conn.put("label")
        assert self._conn.pop() == "label"

    def test_put_many(self):
        self._conn.put_many(['a', 'b'])
        assert self._conn.pop() == "a"
        assert self._conn.pop() == "b"

    def test_len(self):
        self._conn.put_many(['a', 'b', 'c'])
        assert self._conn.queue_len == 3

    def test_get(self):
        self._conn.put_many(['a', 'b', 'c', 'd'])
        _ = self._conn.get(2)
        assert self._conn.queue_len == 2

if __name__ == '__main__':
    unittest.main()
