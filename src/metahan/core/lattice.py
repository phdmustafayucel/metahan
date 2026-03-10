import numpy as np
import gdstk

class Lattice:

    def __init__(self, pitch: float):
        self.pitch = pitch


    def square(self, nx: int, ny: int):

        positions = []

        for i in range(nx):
            for j in range(ny):

                x = (i - nx/2) * self.pitch
                y = (j - ny/2) * self.pitch

                positions.append((x, y))

        return positions


    def hexagonal(self, nx: int, ny: int):

        positions = []

        dy = self.pitch * np.sqrt(3)/2

        for j in range(ny):

            shift = 0.5 * self.pitch if j % 2 else 0

            for i in range(nx):

                x = i * self.pitch + shift
                y = j * dy

                positions.append((x, y))

        return positions