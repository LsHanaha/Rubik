from abc import ABC, abstractmethod
from typing import Literal, Dict


FaceType = Literal['f', 'r', 'u', 'b', 'l', 'd']


class CubeInterface(ABC):

    @abstractmethod
    def __init__(self, cube):
        self._cube = cube

    @abstractmethod
    def face_colors(self, face: FaceType) \
            -> Dict[str, Literal['r', 'g', 'b', 'w', 'y', 'o']]:
        """указание на местоположение записывается в алфавитном порядке (flu)"""

        pass

    @abstractmethod
    def edge_colors(self, face: FaceType) \
            -> Dict[str, str]:
        """{'fu': "gb"}"""

        pass

    @abstractmethod
    def corner_colors(self, face: FaceType) \
            -> Dict[str, str]:
        """{'flu': "grb"}"""

        pass

    @abstractmethod
    def rotate_face(self, face: FaceType, clockwise: bool) -> None:
        """face: ('f', 'r', 'u', 'b', 'l', 'd')"""
        pass

    @abstractmethod
    def rotate_cube(self, direction: Literal['x', 'y', 'z'], clockwise: bool) \
            -> None:
        pass

    @abstractmethod
    def cube_is_solved(self) -> bool:
        pass
