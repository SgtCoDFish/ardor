import os

import numpy as np
import tcod

from ardor.player import Player
from ardor.stats import Stats

ROOT_WIDTH = 80
ROOT_HEIGHT = 50

WORLD_WIDTH = 46
WORLD_HEIGHT = 20

WORLD_SCREEN_X = 20
WORLD_SCREEN_Y = 10

EVENT_SCREEN_X = 0
EVENT_SCREEN_Y = ROOT_HEIGHT-10

font = os.path.join('data/fonts/consolas10x10_gs_tc.png')
tcod.console_set_custom_font(
    font, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

TORCH_RADIUS = 4
SQUARED_TORCH_RADIUS = TORCH_RADIUS * TORCH_RADIUS

SAMPLE_MAP = [
    '##############################################',
    '#######################      #################',
    '######    ###########    #     ###############',
    '#####      ###########  ###        #         #',
    '####        ######      #####      =         #',
    '###         ####       ########    #         #',
    '###         ###      ###########  ######## ###',
    '######### ######    ######             ### ###',
    '########   #######  ######   #     #   ### ###',
    '########   ######      ###                 ###',
    '########                               #######',
    '####       ######      ###   #     #   #######',
    '#### ###   ########## ####             #######',
    '#### ###   ##########   ###########=##########',
    '#### ##################   #####          #####',
    '#### ###             #### #####          #####',
    '####           #     ####                #####',
    '########       #     #### #####          #####',
    '########       #####      ####################',
    '##############################################',
]

SAMPLE_MAP = np.array([list(line) for line in SAMPLE_MAP])

DARK_WALL = tcod.Color(0, 0, 100)
LIGHT_WALL = tcod.Color(130, 110, 50)
DARK_GROUND = tcod.Color(50, 50, 150)
LIGHT_GROUND = tcod.Color(200, 180, 50)


class Ardor:

    def __init__(self):
        self.world_console = tcod.console_new(
            WORLD_WIDTH, WORLD_HEIGHT)
        self.event_console = tcod.console_new(20, 10)
        self.player = Player(20, 10, '@', Stats(20))
        self.recompute = True
        self.torch = True
        self.map = None
        self.noise = None
        self.torchx = 0.0
        self.light_walls = True
        # 1d noise for the torch flickering
        self.noise = tcod.noise_new(1, 1.0, 1.0)

        self.map = tcod.map_new(WORLD_WIDTH, WORLD_HEIGHT)
        self.map.walkable[:] = SAMPLE_MAP[:] == ' '
        self.map.transparent[:] = self.map.walkable[:] | (SAMPLE_MAP == '=')

        self.light_map_bg = np.full(SAMPLE_MAP.shape + (3,), LIGHT_GROUND,
                                    dtype=np.uint8)
        self.light_map_bg[SAMPLE_MAP[:] == '#'] = LIGHT_WALL
        self.dark_map_bg = np.full(SAMPLE_MAP.shape + (3,), DARK_GROUND,
                                   dtype=np.uint8)
        self.dark_map_bg[SAMPLE_MAP[:] == '#'] = DARK_WALL

    def draw_ui(self):
        pass

    def on_enter(self):
        tcod.sys_set_fps(60)
        # we draw the foreground only the first time.
        #  during the player movement, only the @ is redrawn.
        #  the rest impacts only the background color
        # draw the help text & player @
        tcod.console_clear(self.world_console)
        self.draw_ui()
        tcod.console_put_char(
            self.world_console,
            self.player.x, self.player.y, '@', tcod.BKGND_NONE)
        # draw windows
        self.world_console.ch[np.where(SAMPLE_MAP == '=')] = tcod.CHAR_DHLINE
        self.world_console.fg[np.where(SAMPLE_MAP == '=')] = tcod.black

    def render(self, delta_time: float) -> None:
        self.render_event_log()

        dx = 0.0
        dy = 0.0
        di = 0.0

        if self.recompute:
            self.recompute = False
            self.map.compute_fov(
                self.player.x,
                self.player.y,
                TORCH_RADIUS if self.torch else 0,
                self.light_walls,
                tcod.FOV_SHADOW
            )
            self.world_console.bg[:] = self.dark_map_bg[:]
            if self.torch:
                # slightly change the perlin noise parameter
                self.torchx += 0.1
                # randomize the light position between -1.5 and 1.5
                tdx = [self.torchx + 20.0]
                dx = tcod.noise_get(self.noise, tdx, tcod.NOISE_SIMPLEX) * 1.5
                tdx[0] += 30.0
                dy = tcod.noise_get(self.noise, tdx, tcod.NOISE_SIMPLEX) * 1.5
                di = 0.2 * tcod.noise_get(
                    self.noise, [self.torchx], tcod.NOISE_SIMPLEX
                )
                # where_fov = np.where(self.map.fov[:])
                mgrid = np.mgrid[:WORLD_HEIGHT, :WORLD_WIDTH]
                # get squared distance
                light = ((mgrid[0] - self.player.y + dy) ** 2 +
                         (mgrid[1] - self.player.x + dx) ** 2)
                light = light.astype(np.float16)
                where_visible = np.where((light < SQUARED_TORCH_RADIUS) &
                                         self.map.fov[:])
                light[where_visible] = (
                    SQUARED_TORCH_RADIUS - light[where_visible]
                )
                light[where_visible] /= SQUARED_TORCH_RADIUS
                light[where_visible] += di
                light[where_visible] = light[where_visible].clip(0, 1)

                for yx in zip(*where_visible):
                    self.world_console.bg[yx] = tcod.color_lerp(
                        tuple(self.dark_map_bg[yx]),
                        tuple(self.light_map_bg[yx]),
                        light[yx],
                    )
        else:
            where_fov = np.where(self.map.fov[:])
            self.world_console.bg[where_fov] = self.light_map_bg[where_fov]

    def render_event_log(self) -> None:
        self.event_console.default_fg = tcod.grey
        self.event_console.default_bg = tcod.black
        out = ["Did a thing", "Did another thing"]
        for i, msg in enumerate(out):
            self.event_console.print_(
                0, self.event_console.height - (len(out) - i),
                '%d %s' % (i, msg.ljust(18)),
                tcod.BKGND_SET, tcod.LEFT
            )

    def blit_consoles(self, target: tcod.console.Console) -> None:
        self.world_console.blit(
            0, 0, self.world_console.width, self.world_console.height,
            target, WORLD_SCREEN_X, WORLD_SCREEN_Y)

        self.event_console.blit(
            0, 0, self.event_console.width, self.event_console.height,
            target, EVENT_SCREEN_X, EVENT_SCREEN_Y)

    def on_mouse(self, mouse) -> None:
        pass

    def on_key(self, key: tcod.Key) -> None:
        MOVE_KEYS = {
            ord('k'): (0, -1),
            ord('h'): (-1, 0),
            ord('j'): (0, 1),
            ord('l'): (1, 0),
        }

        if key.c in MOVE_KEYS:
            x, y = MOVE_KEYS[key.c]
            dest_x = self.player.x + x
            dest_y = self.player.y + y

            if SAMPLE_MAP[dest_y][dest_x] == ' ':
                tcod.console_put_char(self.world_console,
                                      self.player.x, self.player.y, ' ',
                                      tcod.BKGND_NONE)
                self.player.move_to(dest_x, dest_y)
                tcod.console_put_char(self.world_console,
                                      self.player.x, self.player.y, '@',
                                      tcod.BKGND_NONE)
                self.recompute = True
        elif key.c == ord('t'):
            self.torch = not self.torch
            self.draw_ui()
            self.recompute = True
        elif key.c == ord('w'):
            self.light_walls = not self.light_walls
            self.draw_ui()
            self.recompute = True


def main():
    ardor = Ardor()
    ardor.on_enter()
    root_console = tcod.console_init_root(
        ROOT_WIDTH, ROOT_HEIGHT, "ARDOR", False)

    while not tcod.console_is_window_closed():
        root_console.default_fg = (255, 255, 255)
        root_console.default_bg = (0, 0, 0)

        ardor.render(tcod.sys_get_last_frame_length())
        ardor.blit_consoles(root_console)

        draw_stats(root_console)
        handle_events(ardor)
        tcod.console_flush()


def handle_events(ardor: Ardor) -> None:
    key = tcod.Key()
    mouse = tcod.Mouse()
    EVENT_MASK = tcod.EVENT_MOUSE | tcod.EVENT_KEY_PRESS
    while tcod.sys_check_for_event(EVENT_MASK, key, mouse):
        ardor.on_mouse(mouse)
        ardor.on_key(key)

        if key.vk == tcod.KEY_ENTER and key.lalt:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        elif key.vk == tcod.KEY_PRINTSCREEN or key.c == 'p':
            print("screenshot")
            if key.lalt:
                tcod.console_save_apf(None, "samples.apf")
                print("apf")
            else:
                tcod.sys_save_screenshot()
                print("png")
        elif key.vk == tcod.KEY_ESCAPE:
            raise SystemExit()


def draw_stats(root_console: tcod.console.Console) -> None:
    root_console.default_fg = tcod.grey
    root_console.print_(
        ROOT_WIDTH - 1, ROOT_HEIGHT - 1,
        ' last frame : %3d ms (%3d fps)' % (
            tcod.sys_get_last_frame_length() * 1000.0,
            tcod.sys_get_fps(),
            ),
        tcod.BKGND_NONE, tcod.RIGHT
        )


if __name__ == '__main__':
    main()
