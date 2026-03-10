from abc import ABC, abstractmethod


class Aperture(ABC):

    @abstractmethod
    def contains(self, x: float, y: float) -> bool:
        pass