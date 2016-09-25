"""
    Example of module « Progress Bar » by using `tornado_websocket.modules.ProgressBar` to handle communications,
    and Django's TemplateView for rendering.
"""
import threading
import time

from django.views.generic import TemplateView

from tornado_websockets.modules import ProgressBar
from tornado_websockets.websocket import WebSocket

tws = WebSocket('module_progressbar')
progress_bar = ProgressBar('foo', min=0, max=200)

tws.bind(progress_bar)


@progress_bar.on
def start():
    progress_bar.reset()
    start_thread(progress_bar)


def start_thread(bb):
    def fn():
        for value in range(0, progress_bar.max):
            time.sleep(.1)
            progress_bar.tick(label="[%d/%d] Tâche %d terminée" % (progress_bar.value + 1, progress_bar.max, value))

    threading.Thread(None, fn, None).start()


class MyProgressBar(TemplateView):
    template_name = 'testapp/progress_bar.html'
