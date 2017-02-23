import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from proxypool.db import RedisClient
from proxypool.api import app


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self._app = app.test_client()
        self._conn = RedisClient()

    def tearDown(self):
        self._conn.flush()

    def test_get(self):
        self._conn.put('aaa')
        self._conn.put('bbb')
        r = self._app.get('/get')
        assert 'aaa' in str(r.data)
        r = self._app.get('/get')
        assert 'bbb' in str(r.data)

    def test_count(self):
        self._conn.put('aaa')
        self._conn.put('bbb')
        r = self._app.get('/count')
        assert '2' in str(r.data)
        self._conn.put('ccc')
        self._conn.put('ddd')
        r = self._app.get('/count')
        assert '4' in str(r.data)
        proxy = self._conn.pop()
        r = self._app.get('/count')
        assert '3' in str(r.data)

if __name__ == '__main__':
    unittest.main()
