# coding: utf-8


import django
from django.conf import settings
from django.utils.six import StringIO
from django.core.management import call_command
from django.test import TestCase
from mock import MagicMock

from tornado_websockets.tornadowrapper import TornadoWrapper

django.setup()


class TestCommandRuntornado(TestCase):
    """
    Tests for the management command « runtornado ».
    """

    def setUp(self):
        TornadoWrapper.start_app = MagicMock()
        TornadoWrapper.listen = MagicMock()
        TornadoWrapper.loop = MagicMock()
        self.TORNADO = settings.TORNADO

    def tearDown(self):
        settings.TORNADO = self.TORNADO

    def test_without_tornado_settings(self):
        del settings.TORNADO

        out = StringIO()
        err = StringIO()
        call_command('runtornado', stdout=out, stderr=err)

        self.assertIn("Configuration => Not found: 'Settings' object has no attribute 'TORNADO'", err.getvalue())

    def test_get_port_from_options(self):
        settings.TORNADO['port'] = 1234

        out = StringIO()
        call_command('runtornado', '8080', stdout=out)

        self.assertIn('Port => 8080', out.getvalue())
        TornadoWrapper.listen.assert_called_with(8080)

    def test_get_port_from_settings(self):
        settings.TORNADO['port'] = 1234

        out = StringIO()
        call_command('runtornado', stdout=out)

        self.assertIn('Port => 1234', out.getvalue())
        TornadoWrapper.listen.assert_called_with(1234)

    def test_get_port_with_default_port(self):
        del settings.TORNADO['port']

        out = StringIO()
        call_command('runtornado', stdout=out)

        self.assertIn('Port => 8000', out.getvalue())
        TornadoWrapper.listen.assert_called_with(8000)