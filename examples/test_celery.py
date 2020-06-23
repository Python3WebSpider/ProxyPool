from tasks.celery_scheduler import test_add, run_getter, run_tester


def test_celery():
    r = test_add.delay(1, 2)
    print(r.task_id, r.get())


def test_run_getter():
    r2 = run_getter.delay()
    print(r2.task_id, r2.get())


def test_run_tester():
    r3 = run_tester.delay()
    print(r3.task_id, r3.get())


if __name__ == '__main__':
    test_run_tester()
