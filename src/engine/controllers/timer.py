from .base import ControllerBase
from ..game.context.game import GameContext

class TimerController(ControllerBase):
    def __init__(self, context: GameContext, initial_duration: int | None = None):
        super(TimerController, self).__init__(context)
        self.duration = initial_duration
        self.start_ticks = None

    def init_update(self):
        pass

    def finish_update(self):
        pass

    def start(self, duration: int | None = None):
        target_duration = self.duration or duration
        if not target_duration:
            self.start_ticks = self.context.get_current_ticks()

    @property
    def started_at(self):
        return self.start_ticks

    @property
    def ticks_elapsed(self):
        if self.start_ticks:
            return self.context.get_current_ticks() - self.start_ticks
        else:
            return None
    
    @property
    def has_finished(self):
        return not self.start_ticks and self.ticks_elapsed >= self.duration
