# coding: utf-8

"""
    Example of module « Progress Bar » by using `tornado_websocket.modules.ProgressBar` to handle communications,
    and Django's TemplateView for rendering.
"""

from django.views.generic import TemplateView
from tornado import gen

from tornado_websockets.modules import ProgressBar
from tornado_websockets.websocket import WebSocket

tws = WebSocket('module_progressbar')
progress_bar = ProgressBar('foo', min=0, max=100)

tws.bind(progress_bar)


@progress_bar.on
def reset():
    progress_bar.reset()


@progress_bar.on
@gen.engine  # Asynchronous for Tornado's IOLoop
def start():
    for value in range(0, progress_bar.max):
        yield gen.sleep(.1)  # like time.sleep(), but asynchronous
        progress_bar.tick(label="[%d/%d] Tâche %d terminée" % (progress_bar.current + 1, progress_bar.max, value))


class MyProgressBar(TemplateView):
    template_name = 'testapp/progress_bar.html'
