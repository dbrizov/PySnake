from pygame import time


class Time:
    _clock = time.Clock()
    _fps = 60
    _play_time = 0.0

    @staticmethod
    def _tick():
        milliseconds = Time._clock.tick(Time._fps)
        Time._play_time += milliseconds / 1000.0

    @staticmethod
    def get_delta_time():
        return Time._clock.get_time()

    @staticmethod
    def get_play_time():
        return Time._play_time

    @staticmethod
    def get_fps():
        return Time. _clock.get_fps()

    @staticmethod
    def set_fps(fps):
        Time._fps = fps
