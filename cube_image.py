from cube import Cube
from PIL import Image, ImageDraw
import numpy as np

BLACK = (0,0,0)
GRAY = (210,210,210)
WHITE = (255,255,255)
YELLOW = (240,255,0)
RED = (232,18,10)
ORANGE = (251,140,0)
GREEN = (102,255,51)
BLUE = (32,85,255)
PINK = (255,183,197)
PURPLE = (255,0,255)
CLEAR = (255,255,255,0)

color_code = {
    "W": WHITE,
    "G": GREEN,
    "R": RED,
    "O": ORANGE,
    "B": BLUE,
    "Y": YELLOW
}

WIDTH, HEIGHT = 1200, 1200
scale = 400
circle_pos = [WIDTH/2, HEIGHT/2]  # x, y

points = []
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

def get_xy_stickers(n, r, tlx, tly, tlz):
    stickers = []
    s = (2 - (n+1) * r) / n

    for v in range(n):
        for h in range(n):
            p1x = tlx + r + h * (r+s)
            p1y = tly + r + v * (r+s)
            p1z = tlz

            stickers.append([
                np.matrix([p1x, p1y, p1z]),
                np.matrix([p1x + s, p1y, p1z]),
                np.matrix([p1x + s, p1y + s, p1z]),
                np.matrix([p1x, p1y + s, p1z])
            ])

    return stickers

def get_xz_stickers(n, r, tlx, tly, tlz):
    stickers = []
    s = (2 - (n+1) * r) / n

    for v in range(n):
        for h in range(n):
            p1x = tlx + r + h * (r+s)
            p1y = tly
            p1z = tlz + r + v * (r+s)

            stickers.append([
                np.matrix([p1x, p1y, p1z]),
                np.matrix([p1x + s, p1y, p1z]),
                np.matrix([p1x + s, p1y, p1z + s]),
                np.matrix([p1x, p1y, p1z + s])
            ])

    return stickers

def get_zy_stickers(n, r, tlx, tly, tlz):
    stickers = []
    s = (2 - (n+1) * r) / n

    for v in range(n):
        for h in range(n):
            p1x = tlx
            p1y = tly + r + v * (r+s)
            p1z = tlz + r + h * (r+s)

            stickers.append([
                np.matrix([p1x, p1y, p1z]),
                np.matrix([p1x, p1y, p1z + s]),
                np.matrix([p1x, p1y + s, p1z + s]),
                np.matrix([p1x, p1y + s, p1z])
            ])

    return stickers

def draw_stickers(draw, colors, stickers, rotation_x, rotation_y, rotation_z, projection_matrix):
    for c, s in zip(colors, stickers):
        sticker_4pts = []
        for pt in s:
            rotated2d = pt.reshape((3, 1))
            rotated2d = np.dot(rotation_z, rotated2d)
            rotated2d = np.dot(rotation_y, rotated2d)
            rotated2d = np.dot(rotation_x, rotated2d)

            projected2d = np.dot(projection_matrix, rotated2d)

            x = int(projected2d[0][0] * scale) + circle_pos[0]
            y = int(projected2d[1][0] * scale) + circle_pos[1]

            sticker_4pts.append((x, y))

        draw.polygon(sticker_4pts, fill=color_code[c])
        draw.polygon(sticker_4pts, outline=BLACK, width=1)

def gen_cube_image(cube, r=0.08, ax=-0.5235987755982988, ay=-0.20943951023931956, az=0):
    n = cube.size

    u_stickers = get_xz_stickers(n, r, -1, -1, -1)
    d_stickers = get_xz_stickers(n, r, -1, 1, -1)
    r_stickers = get_zy_stickers(n, r, 1, -1, -1)
    l_stickers = get_zy_stickers(n, r, -1, -1, -1)
    f_stickers = get_xy_stickers(n, r, -1, -1, 1)
    b_stickers = get_xy_stickers(n, r, -1, -1, -1)

    rotation_z = np.matrix([
        [np.cos(az), -np.sin(az), 0],
        [np.sin(az), np.cos(az), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [np.cos(ay), 0, np.sin(ay)],
        [0, 1, 0],
        [-np.sin(ay), 0, np.cos(ay)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, np.cos(ax), -np.sin(ax)],
        [0, np.sin(ax), np.cos(ax)],
    ])

    image = Image.new("RGBA", (WIDTH, HEIGHT), CLEAR)
    draw = ImageDraw.Draw(image)

    colors = cube.get_d_colors()
    draw_stickers(draw, colors, d_stickers, rotation_x, rotation_y, rotation_z, projection_matrix)
    colors = cube.get_l_colors()
    draw_stickers(draw, colors, l_stickers, rotation_x, rotation_y, rotation_z, projection_matrix)
    colors = cube.get_b_colors()
    draw_stickers(draw, colors, b_stickers, rotation_x, rotation_y, rotation_z, projection_matrix)

    colors = cube.get_r_colors()
    draw_stickers(draw, colors, r_stickers, rotation_x, rotation_y, rotation_z, projection_matrix)
    colors = cube.get_u_colors()
    draw_stickers(draw, colors, u_stickers, rotation_x, rotation_y, rotation_z, projection_matrix)
    colors = cube.get_f_colors()
    draw_stickers(draw, colors, f_stickers, rotation_x, rotation_y, rotation_z, projection_matrix)

    image.save("cube.png")
    # image.show()

if __name__ == "__main__":
    cube = Cube(3)
    # alg = "x M2 U M2 U2 M2 U M2"
    # for move in alg.split():
    #     cube.do_move(move)
    
    # colormap = cube.get_cube_colormap()
    # for e in colormap.items():
    #     print(e)

    # print(cube.get_sticker_colors(['UBL', 'UB', 'UBR', 'UL', 'U', 'UR', 'UFL', 'UF', 'UFR']))
    # cube.print_cube(1)  
    
    # for f in "ULFRBD":
    #     for row in cube.faces[f]:
    #         print(row)

    # print(cube.get_u_colors())

    # x:-0.5235987755982988 y:-0.20943951023931956 z:0
    gen_cube_image(cube)