import threading

from .logs import create_logger


class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.playing_thread = None
        self._playing = False
        self.logger = create_logger()

    def start(self):
        self.logger.info("Starts playing")
        self._playing = True
        self.playing_thread = self.StartingThread(self)
        self.playing_thread.start()
        self.view.start()

    def pause(self):
        self.logger.info("Pauses")
        self._playing = False

    def stop(self):
        self.logger.info("Stops playing")
        self._playing = False
        self.model.stop()

    def speed_up(self):
        self.logger.info("Increases speed")
        self.model.speed_up()

    def speed_down(self):
        self.logger.info("Lowers speed")
        self.model.speed_down()

    def reset(self):
        self.logger.info("Resets")
        self.stop()
        self.model.init_game_area()
        self.view.update(self.model)

    def clear(self):
        self.logger.info("Clears")
        self.stop()
        self.model.clear()

    def is_playing(self):
        return self._playing

    class StartingThread(threading.Thread):
        def __init__(self, controller):
            threading.Thread.__init__(self)
            self.controller = controller

        def run(self):
            while self.controller.is_playing():
                self.controller.model.evolve()
                self.controller.view.update(self.controller.model)
