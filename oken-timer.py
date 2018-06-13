from tornado import web, ioloop
import datetime
import asyncio
from handlers import fun_timer
import orm

from config import configs
import logging; logging.basicConfig(level=logging.INFO,filename='stu.log')

class MainHandler(web.RequestHandler):
    def get(self):
        self.write('Hello Tornado')

@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        # yield from asyncio.sleep(0.3)
        return (yield from handler(request))
    return logger

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
    application.listen(9003)
    ioloop.PeriodicCallback(fun_timer, 4000).start()  # start scheduler 每隔2s执行一次f2s
    ioloop.IOLoop.instance().start()