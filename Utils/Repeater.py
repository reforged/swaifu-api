from threading import Timer

# https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds/13151299#13151299


class RepeatedTimer(object):
    def __init__(self, interval, function):
        self._timer = None
        self.interval = interval
        self.function = function
        self.is_running = False
        self.start()

    def __del__(self):
        self.stop()
        del self

    def _run(self):
        self.is_running = False
        self.start()
        self.function()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
