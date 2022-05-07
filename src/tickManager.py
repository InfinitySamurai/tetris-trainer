
import time


class TickManager():
    def __init__(self, fps):
        self.paused = False
        self.fps = fps
        self.seconds_per_frame = 1 / fps
        self.current_tick = 0
        self.last_update_time = time.time()
        self.accumulated_tick_time = 0

    def has_ticked(self):
        if self.accumulated_tick_time > self.seconds_per_frame:
            self.accumulated_tick_time = 0
            self.current_tick += 1
            return True
        return False

    def update(self):
        if not self.paused:
            current_update_time = time.time()
            self.accumulated_tick_time += current_update_time - self.last_update_time
            self.last_update_time = current_update_time
