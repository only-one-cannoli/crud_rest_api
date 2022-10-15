from tornado.ioloop import IOLoop
from tornado.web import Application

from .defs.settings import Settings


if __name__ == "__main__":
    app = Application(list(Settings.handlers.items()))
    app.listen(Settings.localhost_port)
    IOLoop.instance().start()
