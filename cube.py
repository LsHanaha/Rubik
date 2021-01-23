""" Describes the model of the rubik cube. """
from enum import auto, Enum
from itertools import product
from typing import Dict, Callable, Iterator, List, Tuple, Union


class Color(Enum):
    yellow = 0
    orange = auto()
    blue = auto()
    red = auto()
    green = auto()
    white = auto()

    def __str__(self,
                _color_codes: List[int] = [220, 202, 39, 124, 78, 231]) -> str:
        return f"\033[38;5;{_color_codes[self.value]}m■\033[00m"

Coords = Tuple[int, int, int]


class Notation:
    face2id: Dict[str, int] = {face: i for i, face in enumerate("ulfrbd")}

    faces_rel: List[Callable[[Coords], bool]] = [
        lambda coords: coords[1] == 1,
        lambda coords: coords[0] == -1,
        lambda coords: coords[2] == -1,
        lambda coords: coords[0] == 1,
        lambda coords: coords[2] == 1,
        lambda coords: coords[1] == -1
    ]


class RotatableThing:
    """ Describes something that has coordinates and can be rotated """

    def __init__(self, coords: Coords):
        self.coords = coords

    def rotate(self, dim: int, clockwise: bool = True):
        """ Rotates the object along dim axis. """
        i, j = (axis for axis in range(3) if axis != dim)
        new_coords = [0, 0, 0]
        new_coords[dim] = self.coords[dim]
        if clockwise:
            new_coords[i] = self.coords[j]
            new_coords[j] = -self.coords[i]
        else:
            new_coords[i] = -self.coords[j]
            new_coords[j] = self.coords[i]
        self.coords = tuple(new_coords)

    @property
    def x(self) -> int:
        return self.coords[0]

    @property
    def y(self) -> int:
        return self.coords[1]

    @property
    def z(self) -> int:
        return self.coords[2]


class Tile(RotatableThing):
    """ A colored tile attached to a cell. It is characterized by one point
    relative to the center of its cell and a color. """

    def __init__(self, coords: Coords, color: Color):
        super().__init__(coords)
        self.color = color

    def __str__(self) -> str:
        return f"{self.color:12} at {str(self.coords):12}"


class Cell(RotatableThing):
    """ A building block of the rubik cube.
    Can have 1-3 tiles attached to it. """

    def __init__(self, coords: Coords, *tiles: Tile):
        assert 1 <= len(tiles) <= 3
        super().__init__(coords)
        self.tiles = list(tiles)

    def __str__(self) -> str:
        tiles = " and ".join(str(tile) for tile in self.tiles)
        return f"Cell at {str(self.coords):12} with {tiles}"

    def rotate(self, dim: int, clockwise: bool = True):
        super().rotate(dim, clockwise)
        for tile in self.tiles:
            tile.rotate(dim, clockwise)

    def color_at_face(self, face_id: int) -> Color:
        """ Returns the color that the cell has on the given face.
        Raises if it is not part of that face. """
        filter_func = Notation.faces_rel[face_id]
        return next(tile.color for tile in self.tiles
                    if filter_func(tile.coords))


class Cube:
    """ A collection of cells with methods for rearranging them. """

    initial_color_coords = [
        (0, 1, 0),  # up
        (-1, 0, 0), # left
        (0, 0, -1), # front
        (1, 0, 0),  # right
        (0, 0, 1),  # back
        (0, -1, 0)  # down
    ]

    rotations_rel: List[Tuple[int, int]] = [
        (1, False),     # y axis, no inversion
        (0, False),     # x axis, no inversion
        (2, False),     # z axis, no inversion
        (0, True),
        (2, True),
        (1, True)
    ]

    def __init__(self):
        self.cells = []
        coords2color = dict(zip(Cube.initial_color_coords, Color))
        coords_iter = product((0, -1, 1), (0, -1, 1), (0, -1, 1))
        next(coords_iter)  # skipping (0, 0, 0), as the center cell is not used
        for coords in coords_iter:
            tiles = []
            for dim, value in enumerate(coords):
                if value:
                    tile_coords_lst = [0, 0, 0]
                    tile_coords_lst[dim] = value
                    tile_coords = tuple(tile_coords_lst)
                    tiles.append(Tile(tile_coords, coords2color[tile_coords]))
            self.cells.append(Cell(coords, *tiles))

    def __repr__(self):

        # TODO: generalize this
        up = sorted(self.get_face_rel(0), key=lambda cell: (-cell.z, cell.x))
        up = list(map(lambda cell: str(cell.color_at_face(0)), up))

        left = sorted(self.get_face_rel(1), key=lambda cell: (-cell.y, -cell.z))
        left = list(map(lambda cell: str(cell.color_at_face(1)), left))

        front = sorted(self.get_face_rel(2), key=lambda cell: (-cell.y, cell.x))
        front = list(map(lambda cell: str(cell.color_at_face(2)), front))

        right = sorted(self.get_face_rel(3), key=lambda cell: (-cell.y, cell.z))
        right = list(map(lambda cell: str(cell.color_at_face(3)), right))

        back = sorted(self.get_face_rel(4), key=lambda cell: (-cell.y, -cell.x))
        back = list(map(lambda cell: str(cell.color_at_face(4)), back))

        down = sorted(self.get_face_rel(5), key=lambda cell: (cell.z, cell.x))
        down = list(map(lambda cell: str(cell.color_at_face(5)), down))

        tiles = ["\n"]
        for i in range(0, 9, 3):
            tiles.append(" " * 7)
            tiles.extend(up[i:i + 3])
            tiles.append("\n")
        tiles.append("\n")

        center_faces = [left, front, right, back]
        for i in range(0, 9, 3):
            for face in center_faces:
                tiles.extend(face[i:i + 3])
                tiles.append(" ")
            tiles.append("\n")
        tiles.append("\n")

        for i in range(0, 9, 3):
            tiles.append(" " * 7)
            tiles.extend(down[i:i + 3])
            tiles.append("\n")
        tiles.append("\n")

        return " ".join(tiles)

    def get_face_rel(self, face_id: int) -> Iterator[Cell]:
        filter_func = Notation.faces_rel[face_id]
        yield from (cell for cell in self.cells if filter_func(cell.coords))

    def rotate_face_rel(self, face: Union[int, str], clockwise: bool = True):
        """
        Rotates one of the relative faces clockwise or counter-clockwise.

        Args:
            face: either face id (0-5) or face name ("ulfrbd")
            clockwise: True for FRUBLD, False for F'R'U'B'L'D'
        """
        face_id = face if isinstance(face, int) else Notation.face2id[face]
        dim, inverse = Cube.rotations_rel[face_id]
        if inverse:
            clockwise = not clockwise
        for cell in self.get_face_rel(face_id):
            cell.rotate(dim, clockwise)

    def rotate_cube(self, dim: int, clockwise: bool = True):
        """
        Rotates the whole cube to change relative faces.

        Args:
            dim: the axis along which to rotate. One of 0, 1, 2 (x, y, z),
                where x is right, y is up, z is forward. The axis to rotate
                is the axis whose coordinate does not change after rotation.
            clockwise: whether or not to rotate clockwise
        """
        for cell in self.cells:
            cell.rotate(dim, clockwise)


if __name__ == "__main__":
    # as before, indices of faces are 0-5 in ULFRBD
    cube = Cube()   # init cube, by default F is blue
    # print("-------------------------")
    # for cell in cube.get_face_rel(2):   # so this will output (among others)
    #     print(cell)                     # the following:
    # print("-------------------------")
    #
    # Cell at (0, 0, -1)   with Color.blue   at (0, 0, -1)
    # This means Cell at position (0, 0, -1) relative to the center of cube (center, center, closer)
    # will have color blue at position (0, 0, -1) relative to the center of the CELL (center, center, closer)
    #
    # Cell at (-1, -1, -1) with Color.orange at (-1, 0, 0)   and Color.white  at (0, -1, 0)   and Color.blue   at (0, 0, -1)
    # This means Cell at position (-1, -1, -1) relative to the center of cube (left, down, closer)
    # will have color orange at position (-1, 0, 0) relative to the center of the CELL (left, center, center)
    #           color white  at position (0, -1, 0) relative to the center of the CELL (center, down, center)
    #           color blue   at position (0, 0, -1) relative to the center of the CELL (center, center, closer)
    #
    # so now cube.rotate_face_rel("f") will rotate the FRONT (still BLUE) FACE
    cube.rotate_cube(1)  # rotate cube along y axis clockwise. Now RED is front, BLUE is left
    # so now cube.rotate_face_rel("f") will rotate the FRONT (now RED) FACE
    cube.rotate_face_rel("f")
    print(cube)  # need better representation, I know
