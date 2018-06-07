from tornado import web, ioloop
import datetime
import asyncio
from handlers import fun_timer
import orm

from config import configs


class MainHandler(web.RequestHandler):
    def get(self):
        self.write('Hello Tornado')

@asyncio.coroutine
def f2s():
    yield from print('2s', datetime.datetime.now())

@asyncio.coroutine
def init(loop):
    yield from orm.create_pool(loop=loop, **configs.db)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    application = web.Application([
        (r'/', MainHandler),
    ])
    application.listen(8081)
    ioloop.PeriodicCallback(fun_timer, 1000).start()  # start scheduler 每隔2s执行一次f2s
    ioloop.IOLoop.instance().start()