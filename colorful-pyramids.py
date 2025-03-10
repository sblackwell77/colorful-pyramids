import pyglet
import math
import random

window = pyglet.window.Window(800, 600, "Rotating Colorful 3D Pyramids")

pyramids = [
    [[0, 1, 0], [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1]],
    [[0, 2, 0], [-2, -2, -2], [2, -2, -2], [2, -2, 2], [-2, -2, 2]],
    [[0, 3, 0], [-3, -3, -3], [3, -3, -3], [3, -3, 3], [-3, -3, 3]]
]

edges = [
    [0, 1], [0, 2], [0, 3], [0, 4],
    [1, 2], [2, 3], [3, 4], [4, 1]
]

angle_x, angle_y = 0, 0
lines = []

def project_3d_to_2d(x, y, z, width, height):
    fov = 400
    z += 5
    factor = fov / z
    x_2d = x * factor + width // 2
    y_2d = y * factor + height // 2
    return x_2d, y_2d

def rotate_vertex(vertex, angle_x, angle_y):
    x, y, z = vertex
    y_rot = y * math.cos(angle_x) - z * math.sin(angle_x)
    z_rot = y * math.sin(angle_x) + z * math.cos(angle_x)
    x_rot = x * math.cos(angle_y) - z * math.sin(angle_y)
    z_rot = x * math.sin(angle_y) + z * math.cos(angle_y)
    return x_rot, y_rot, z_rot

def create_lines():
    global lines
    lines.clear()
    for pyramid in pyramids:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        rotated_vertices = [rotate_vertex(v, angle_x, angle_y) for v in pyramid]
        for edge in edges:
            v1 = rotated_vertices[edge[0]]
            v2 = rotated_vertices[edge[1]]
            x1, y1 = project_3d_to_2d(v1[0], v1[1], v1[2], window.width, window.height)
            x2, y2 = project_3d_to_2d(v2[0], v2[1], v2[2], window.width, window.height)
            line = pyglet.shapes.Line(x1, y1, x2, y2, width=2, color=color)
            lines.append(line)

@window.event
def on_draw():
    window.clear()
    create_lines()
    for line in lines:
        line.draw()

def update(dt):
    global angle_x, angle_y
    angle_x += 0.01
    angle_y += 0.01

pyglet.clock.schedule(update)
pyglet.app.run()
