"""
-------------------------------------------------
    File Name:     run.py
    Description:   程序的入口。
    Author:        Liu
    Date:          2016/12/9
-------------------------------------------------
"""
from proxypool.api import app
from proxypool.schedule import Schedule
from multiprocessing import Process

def main():
    s = Schedule()
    s.run()
    app.run()

if __name__ == '__main__':
    main()

