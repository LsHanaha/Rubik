from typing import Dict, List, Tuple, Union, Any, Optional
from colorama import Fore, Style


_neighbours = {'u': None,
               'r': None,
               'b': None,
               'l': None}

_cubie_masks = {1: 255,
                2: 65280,
                3: 16711680,
                4: 4278190080,
                5: 1095216660480,
                6: 280375465082880,
                7: 71776119061217280,
                8: 18374686479671623680}

_clear_cubie_masks = {1: 18446744073709551360,
                      2: 18446744073709486335,
                      3: 18446744073692839935,
                      4: 18446744069431361535,
                      5: 18446742978492891135,
                      6: 18446463698244468735,
                      7: 18374967954648334335,
                      8: 72057594037927935}


class Cube:

    moves = 'FRUBLD'
    colors: Dict[int, str] = {0: 'Y', 1: 'G', 2: 'O', 3: 'B', 4: 'R', 5: 'W'}

    command_color: Dict[str, str] = {'U': 'Y',
                                     'D': 'W',
                                     'F': 'G',
                                     'R': 'O',
                                     'L': 'R',
                                     'B': 'B'}

    faces: Dict[str, Dict[str, Dict[str, Union[str, List[int]]]]] = \
        {'Y': _neighbours.copy(),
         'W': _neighbours.copy(),
         'G': _neighbours.copy(),
         'B': _neighbours.copy(),
         'O': _neighbours.copy(),
         'R': _neighbours.copy()}

    faces['Y']['u'] = {'color': 'B', 'mask': [3, 2, 1]}
    faces['Y']['r'] = {'color': 'O', 'mask': [3, 2, 1]}
    faces['Y']['b'] = {'color': 'G', 'mask': [3, 2, 1]}
    faces['Y']['l'] = {'color': 'R', 'mask': [3, 2, 1]}

    faces['W']['u'] = {'color': 'G', 'mask': [7, 6, 5]}
    faces['W']['r'] = {'color': 'O', 'mask': [7, 6, 5]}
    faces['W']['b'] = {'color': 'B', 'mask': [7, 6, 5]}
    faces['W']['l'] = {'color': 'R', 'mask': [7, 6, 5]}

    faces['R']['u'] = {'color': 'Y', 'mask': [1, 8, 7]}
    faces['R']['r'] = {'color': 'G', 'mask': [1, 8, 7]}
    faces['R']['b'] = {'color': 'W', 'mask': [1, 8, 7]}
    faces['R']['l'] = {'color': 'B', 'mask': [5, 4, 3]}

    faces['O']['u'] = {'color': 'Y', 'mask': [5, 4, 3]}
    faces['O']['r'] = {'color': 'B', 'mask': [1, 8, 7]}
    faces['O']['b'] = {'color': 'W', 'mask': [5, 4, 3]}
    faces['O']['l'] = {'color': 'G', 'mask': [5, 4, 3]}

    faces['G']['u'] = {'color': 'Y', 'mask': [7, 6, 5]}
    faces['G']['r'] = {'color': 'O', 'mask': [1, 8, 7]}
    faces['G']['b'] = {'color': 'W', 'mask': [3, 2, 1]}
    faces['G']['l'] = {'color': 'R', 'mask': [5, 4, 3]}

    faces['B']['u'] = {'color': 'Y', 'mask': [3, 2, 1]}
    faces['B']['r'] = {'color': 'R', 'mask': [1, 8, 7]}
    faces['B']['b'] = {'color': 'W', 'mask': [7, 6, 5]}
    faces['B']['l'] = {'color': 'O', 'mask': [5, 4, 3]}

    state: Dict[str, int] = {'Y': 0,
                             'G': 72340172838076673,
                             'O': 144680345676153346,
                             'B': 217020518514230019,
                             'R': 289360691352306692,
                             'W': 361700864190383365}

    def __init__(self):
        self.solution: List[str] = []

    def __repr__(self):
        green = self._get_face_colors('G', [1, 2, 3, 8, 4, 7, 6, 5])
        green = ['  ' * 5 + row for row in green]

        red = self._get_face_colors('R', [3, 4, 5, 2, 6, 1, 8, 7])
        white = self._get_face_colors('W', [1, 2, 3, 8, 4, 7, 6, 5])
        orange = self._get_face_colors('O', [7, 8, 1, 6, 2, 5, 4, 3])
        yellow = self._get_face_colors('Y', [5, 6, 7, 4, 8, 3, 2, 1])
        four = []
        for _temp in zip(red, white, orange, yellow):
            four.append('   '.join(_temp))

        blue = self._get_face_colors('B', [5, 6, 7, 4, 8, 3, 2, 1])
        blue = ['  ' * 5 + row for row in blue]
        return "{}\n\n{}\n\n{}\n\n{}\n".format('\n'.join(green),
                                               '\n'.join(four),
                                               '\n'.join(blue),
                                               '#' * 120)

    def _get_face_colors(self, face_color: str, masks: List[int]) \
            -> List[str]:

        face = self.state[face_color]

        face_colors = [self.__get_cubie_color(face, mask) for mask in masks]
        face_colors.insert(4, face_color)
        return ['  '.join(face_colors[x * 3: x * 3 + 3]) for x in range(3)]

    def __get_cubie_color(self, face: int, mask: int) -> str:

        val = face & _cubie_masks[mask]
        shift = (mask - 1) * 8
        val = val >> shift
        color = self.colors[val]

        if color == 'W':
            return color
        elif color == 'Y':
            return f"{Fore.YELLOW}Y{Style.RESET_ALL}"
        elif color == 'R':
            return f"{Fore.RED}R{Style.RESET_ALL}"
        elif color == 'G':
            return f"{Fore.GREEN}G{Style.RESET_ALL}"
        elif color == 'B':
            return f"{Fore.BLUE}B{Style.RESET_ALL}"
        elif color == 'O':
            return f"{Fore.LIGHTMAGENTA_EX}O{Style.RESET_ALL}"

    def shuffle(self, count: int):
        pass

    def rotation(self, command: str) -> None:

        command = command.upper()
        # command = self._redefine_command(command)  # for cube rotation purpose
        self.solution.append(command)

        counterclockwise = False

        if "'" in command:
            counterclockwise = True
            command = command.replace("'", "")

        color = self._define_color(command)
        self._rotate_face(color, counterclockwise)
        self._rotate_neighbours(color, counterclockwise)

    def _define_color(self, command: str) -> str:
        return self.command_color[command]

    def _rotate_face(self, command: str, counterclockwise: bool) \
            -> None:

        face = self.state[command[0]]
        if counterclockwise:
            mask = 18446462598732840960
            clear_mask = 281474976710655

            rot_value = face & mask >> 48
            face = face & clear_mask

            face = face << 16
            face = face ^ rot_value
        else:
            mask = 65535
            rot_value = face & mask << 48
            face = face >> 16
            face = rot_value ^ face

        self.state[command[0]] = face

    def _rotate_neighbours(self, command: str, counterclockwise: bool) \
            -> None:

        neighbours: Dict[str, Dict[str, Union[str, List[int]]]] = \
            self.faces[command]

        up: Dict[str, Union[str, List[int]]] = neighbours['u']
        right: Dict[str, Union[str, List[int]]] = neighbours['r']
        back: Dict[str, Union[str, List[int]]] = neighbours['b']
        left: Dict[str, Union[str, List[int]]] = neighbours['l']

        list_cubies = self._get_neighbour_cubies_list([up, right, back, left])

        if counterclockwise:
            list_cubies = list_cubies[1:] + list_cubies[:1]
        else:
            list_cubies = list_cubies[-1:] + list_cubies[:-1]

        self._set_neighbour_cubie_list([up, right, back, left], list_cubies)

    def _get_neighbour_cubies_list(self, face: List[Dict[str, Any]]) \
            -> List[List[int]]:

        up, right, back, left = face

        up_cubies = \
            self.__get_neighbour_cubies(self.state[up['color']], up['mask'])
        right_cubies = \
            self.__get_neighbour_cubies(self.state[right['color']],
                                        right['mask'])
        back_cubies = \
            self.__get_neighbour_cubies(self.state[back['color']], back['mask'])
        left_cubies = \
            self.__get_neighbour_cubies(self.state[left['color']], left['mask'])

        return [up_cubies, right_cubies, back_cubies, left_cubies]

    @staticmethod
    def __get_neighbour_cubies(neighbour: int, mask: List[int]) \
            -> List[int]:

        first = neighbour & _cubie_masks[mask[0]]
        second = neighbour & _cubie_masks[mask[1]]
        third = neighbour & _cubie_masks[mask[2]]

        return [
                first >> (mask[0] - 1) * 8,
                second >> (mask[1] - 1) * 8,
                third >> (mask[2] - 1) * 8
                ]

    def _set_neighbour_cubie_list(self, face: List[Dict[str, Any]],
                                  list_cubies: List[List[int]]) \
            -> None:

        up, right, back, left = face

        self.state[up['color']] = self.__set_neighbour_cubies(
            self.state[up['color']], up['mask'], list_cubies[0])

        self.state[right['color']] = self.__set_neighbour_cubies(
            self.state[right['color']], right['mask'], list_cubies[1])

        self.state[back['color']] = self.__set_neighbour_cubies(
            self.state[back['color']], back['mask'], list_cubies[2])

        self.state[left['color']] = self.__set_neighbour_cubies(
            self.state[left['color']], left['mask'], list_cubies[3])

    @staticmethod
    def __set_neighbour_cubies(neighbour: int, mask: List[int],
                               new_values: List[int]) \
            -> int:

        # clear old values for neighbour face
        neighbour = neighbour & _clear_cubie_masks[mask[0]]
        neighbour = neighbour & _clear_cubie_masks[mask[1]]
        neighbour = neighbour & _clear_cubie_masks[mask[2]]

        # and set new values
        new_values = [new_values[0] << (mask[0] - 1) * 8,
                      new_values[1] << (mask[1] - 1) * 8,
                      new_values[2] << (mask[2] - 1) * 8]
        new_value = new_values[0] | new_values[1] | new_values[2]
        neighbour = neighbour | new_value
        return neighbour


if __name__ == '__main__':
    cube = Cube()
    print(cube)
    cube.rotation("d")
    print(cube)

