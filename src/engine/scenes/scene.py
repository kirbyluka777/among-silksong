from abc import ABC, abstractmethod
from ..game.context.game import GameContext


class Scene(ABC):
    @abstractmethod
    def load(self, context: GameContext):
        pass

    @abstractmethod
    def start(self, context: GameContext):
        pass

    @abstractmethod
    def update(self, context: GameContext):
        pass

    @abstractmethod
    def draw(self, context: GameContext):
        pass

    @abstractmethod
    def exit(self, context: GameContext):
        pass