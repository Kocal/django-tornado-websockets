# Thanks to Ben Darnell for his file which show how to makes Tornado runs fine with Django and other WSGI Handler:
#   https://github.com/bdarnell/django-tornado-demo/blob/master/testsite/tornado_main.py
#
# I also made a more advanced file for a Django WSGIHandler, a Tornado WebSocketHandler, and a Tornado RequestHandler:
#   https://github.com/Kocal/django-test-websockets/blob/tornado-websocket/DjangoTestWebsockets/tornado_main.py

import django.core.handlers.wsgi
from django.apps import AppConfig
from django.conf import settings
from django.core.management import BaseCommand

from tornado_websockets.tornadowrapper import TornadoWrapper

if django.VERSION[1] > 5:
    django.setup()


class Command(BaseCommand, AppConfig):
    help = 'Run Tornado web server with Django and WebSockets support'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.default_port = 8000

    def add_arguments(self, parser):
        parser.add_argument('port', nargs='?', help='Optional port number', type=int)

    def handle(self, *args, **options):
        test_mode = options.get('test_mode')

        # 1 - Read Tornado settings from Django settings file
        try:
            tornado_configuration = settings.TORNADO
        except AttributeError as e:
            tornado_configuration = {}

        if not tornado_configuration:
            tornado_configuration = {}

        # 2 - Get port for Tornado
        tornado_port = options.get('port')

        if not tornado_port:
            tornado_port = tornado_configuration.get('port')
        if not tornado_port:
            tornado_port = self.default_port

        # 3 - Set-up Tornado handlers
        tornado_handlers = tornado_configuration.get('handlers', [])

        # 4 - Set up Tornado settings
        tornado_settings = tornado_configuration.get('settings', {})

        # 6 - Run Tornado
        TornadoWrapper.start_app(tornado_handlers, tornado_settings)
        TornadoWrapper.listen(tornado_port)
        TornadoWrapper.loop()
