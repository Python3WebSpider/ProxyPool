from proxypool.api import app
from proxypool.schedule import Schedule

def main():
    s = Schedule()
    s.run()
    app.run()

if __name__ == '__main__':
    main()

