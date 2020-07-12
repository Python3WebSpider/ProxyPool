from celery_proxy import app
from proxypool.processors.getter import Getter
from proxypool.processors.tester import Tester


@app.task
def test_add(x, y):
    return x + y


@app.task
def run_getter():
    getter = Getter()
    getter.run()


@app.task
def run_tester():
    tester = Tester()
    tester.run()

@app.task
def test_add_two(x):
    return x + 2