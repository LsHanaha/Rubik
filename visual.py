# pylint: skip-file
# type: ignore

""" Guys, you shouldn't open this topic. You are young, playful, everything is
easy for you. This is not it. This is not Chikatilo and not even the archives
of the special services. It's better not to go here. Seriously, any of you will
be sorry. Better close the topic and forget what was written here. I fully
understand that this message will cause additional interest, but I want to
immediately warn the curious - stop. The rest simply won't find it. """

from itertools import product
from ursina import *
from ursina.color import rgb


app = Ursina()

animation_time = 0.6

rotation_dims = {
    "f": (2, 1), "u": (1, 1), "l": (0, -1), "r": (0, 1), "b": (2, -1), "d": (1, -1)
}

rubik = Entity(model="cube", scale=(3,3,3), color=color.clear, position=(0,0,0))

faces = {}
faces["f"] = Entity(model="cube", scale=(1,1,1/3), parent=rubik, color=color.clear, position=(0,0,-1/3))
faces["b"] = Entity(model="cube", scale=(1,1,1/3), parent=rubik, color=color.clear, position=(0,0,1/3))
faces["l"] = Entity(model="cube", scale=(1/3,1,1), parent=rubik, color=color.clear, position=(-1/3,0,0))
faces["r"] = Entity(model="cube", scale=(1/3,1,1), parent=rubik, color=color.clear, position=(1/3,0,0))
faces["u"] = Entity(model="cube", scale=(1,1/3,1), parent=rubik, color=color.clear, position=(0,1/3,0))
faces["d"] = Entity(model="cube", scale=(1,1/3,1), parent=rubik, color=color.clear, position=(0,-1/3,0))
id2face = ["u", "l", "f", "r", "b", "d"]

cell_params = dict(model="cube", parent=rubik, scale=(1/3,1/3,1/3), color=color.black66)
cell_coords = [-1/3, 0, 1/3]  # lcr, dcu, fcb
cells = {(x, y, z): Entity(**cell_params, position=(cell_coords[x], cell_coords[y], cell_coords[z]))
         for  x, y, z in product(range(3), range(3), range(3))}


opacity = 255
colors = [
    rgb(255, 255, 51, a=opacity),  # yellow
    rgb(255, 153, 51, a=opacity),  # orange
    rgb(0, 51, 255, a=opacity),    # blue
    rgb(255, 51, 51, a=opacity),   # red
    rgb(153, 255, 51, a=opacity),  # green
    rgb(204, 204, 204, a=opacity), # white
]


tile_size = 0.875
tile_thickness = 0.05
tiles = []
# up
tiles.extend(Entity(model="cube", scale=(tile_size,tile_thickness,tile_size), parent=cells[x, 2, z], color=colors[0], position=(0,.5,0), reflectivity=10)
             for x, z in product(range(3), range(3)))
# left
tiles.extend(Entity(model="cube", scale=(tile_thickness,tile_size,tile_size), parent=cells[0, y, z], color=colors[1], position=(-.5,0,0))
             for y, z in product(range(3), range(3)))
# front
tiles.extend(Entity(model="cube", scale=(tile_size,tile_size,tile_thickness), parent=cells[x, y, 0], color=colors[2], position=(0,0,-.5))
             for x, y in product(range(3), range(3)))
# right
tiles.extend(Entity(model="cube", scale=(tile_thickness,tile_size,tile_size), parent=cells[2, y, z], color=colors[3], position=(.5,0,0))
             for y, z in product(range(3), range(3)))
# back
tiles.extend(Entity(model="cube", scale=(tile_size,tile_size,tile_thickness), parent=cells[x, y, 2], color=colors[4], position=(0,0,.5))
             for x, y in product(range(3), range(3)))
# down
tiles.extend(Entity(model="cube", scale=(tile_size,tile_thickness,tile_size), parent=cells[x, 0, z], color=colors[5], position=(0,-.5,0))
             for x, z in product(range(3), range(3)))


text = []
text.append(Text("Control rubik: 012345, lshift", font="Anonymous.ttf", origin=(-1.1, -16)))
text.append(Text("Control view: wasd, arrows   ", font="Anonymous.ttf", origin=(-1.1, -14)))
text.append(Text("Reset view: r                ", font="Anonymous.ttf", origin=(-1.1, -12)))
text.append(Text("Toggle help: h               ", font="Anonymous.ttf", origin=(-1.1, -10)))

tx, ty, tz = .08, .1, 0.55
label_kwargs = dict(font="Anonymous.ttf", scale=10, color=color.black)
text.append(Text("0", parent=cells[1,2,1], position=(-tx, tz, ty), rotation=(90,0,0), **label_kwargs))
text.append(Text("1", parent=cells[0,1,1], position=(-tz, ty, tx), rotation=(0,90,0), **label_kwargs))
text.append(Text("2", parent=cells[1,1,0], position=(-tx, ty, -tz), rotation=(0,0,0), **label_kwargs))
text.append(Text("3", parent=cells[2,1,1], position=(tz, ty, -tx), rotation=(0,-90,0), **label_kwargs))
text.append(Text("4", parent=cells[1,1,2], position=(tx, ty, tz), rotation=(0,180,0), **label_kwargs))
text.append(Text("5", parent=cells[1,0,1], position=(-tx, -tz, -ty), rotation=(-90,0,0), **label_kwargs))


def contains(a: Entity, b: Entity) -> bool:
    a_min = a.position - a.bounds / 2
    a_max = a.position + a.bounds / 2
    return ((a_min.x <= b.position.x <= a_max.x)
            and (a_min.y <= b.position.y <= a_max.y)
            and (a_min.z <= b.position.z <= a_max.z))


def rotate(face_id: str, reverse: bool):
    face = faces[face_id]
    for cell in cells.values():
        cell.reparent_to(rubik)
        if contains(face, cell):
            cell.reparent_to(face)

    rotation = face.rotation
    dim, direction = rotation_dims[face_id]
    rotation[dim] += 90 * direction * (-1 if reverse else 1)
    face.animate_rotation(rotation, duration=animation_time)#, curve=curve.linear)



def input(key):
    if key == "r":
        rubik.animate_rotation((0, 0, 0), duration=animation_time)
    elif key == "h":
        for t in text:
            t.enabled = not t.enabled
    elif key in "012345":
        if all(v % 90 == 0 for face in faces.values() for v in face.rotation):
            rotate(id2face[int(key)], held_keys["left shift"])


def update():
    rubik.rotation_x -= held_keys['w']
    rubik.rotation_x += held_keys['s']
    rubik.rotation_y += held_keys['d']
    rubik.rotation_y -= held_keys['a']
    rubik.rotation_z += held_keys['right arrow']
    rubik.rotation_z -= held_keys['left arrow']
    camera.z += held_keys['up arrow'] * .1
    camera.z -= held_keys['down arrow'] * .1


sky = Sky(texture="reflection_map_3")


app.run()
