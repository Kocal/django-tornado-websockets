# coding: utf-8
import inspect

import django
from django.conf import settings
from django.utils.six import StringIO
from django.core.management import call_command
from django.test import TestCase
from mock import patch, ANY

import tornado_websockets.management.commands.runtornado
from tornado_websockets.tornadowrapper import TornadoWrapper

django.setup()


def methodStub(*args, **kwargs):
    return inspect.getargspec(methodStub)


class TestCommandRuntornado(TestCase):
    """
        Tests for the management command « runtornado ».
    """

    def setUp(self):
        self.TORNADO = settings.TORNADO

    def tearDown(self):
        settings.TORNADO = self.TORNADO

    '''
        Tests for settings behavior.
    '''

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_without_tornado_settings(self, stub):
        del settings.TORNADO

        err = StringIO()

        call_command('runtornado', stdout=StringIO(), stderr=err)

        self.assertIn("Configuration => Not found: 'Settings' object has no attribute 'TORNADO'", err.getvalue())
        stub.assert_not_called()

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_with_tornado_settings(self, stub):
        err = StringIO()

        call_command('runtornado', stdout=StringIO(), stderr=err)

        self.assertNotIn("Configuration => Not found: 'Settings' object has no attribute 'TORNADO'", err.getvalue())
        stub.assert_called()

    '''
        Tests for handlers behavior.
    '''

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_without_handlers(self, stub):
        del settings.TORNADO['handlers']

        call_command('runtornado', stdout=StringIO())

        stub.assert_called_with([], ANY, ANY)

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_with_handlers(self, stub):
        call_command('runtornado', stdout=StringIO())

        stub.assert_called_with(ANY, ANY, ANY)

    '''
        Tests for settings behavior.
    '''

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_without_settings(self, stub):
        del settings.TORNADO['settings']

        call_command('runtornado', stdout=StringIO())

        stub.assert_called_with(ANY, {}, ANY)

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_with_settings(self, stub):
        call_command('runtornado', stdout=StringIO())

        stub.assert_called_with(ANY, {'autoreload': True, 'debug': True}, ANY)

    '''
        Tests for port behavior.
    '''

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_get_port_from_options(self, stub):
        settings.TORNADO['port'] = 1234

        call_command('runtornado', '8080', stdout=StringIO())

        stub.assert_called_with(ANY, ANY, 8080)

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_get_port_from_settings(self, stub):
        settings.TORNADO['port'] = 1234

        call_command('runtornado', stdout=StringIO())

        stub.assert_called_with(ANY, ANY, 1234)

    @patch('tornado_websockets.management.commands.runtornado.run')
    def test_get_port_with_default_port(self, stub):
        del settings.TORNADO['port']

        call_command('runtornado', stdout=StringIO())

        stub.assert_called_with(ANY, ANY, 8000)
