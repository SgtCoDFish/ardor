import os
import tcod

from ardor.player import Player
from ardor.map import Map
from ardor.item import Item, ItemEntity
from ardor.inventory import PickupResult
from ardor.stats import Stats
from ardor.events import (
    GameEvent, MovementEvent, NothingThereEvent,
    PickupEvent, InventoryFullEvent
)
from ardor.consoles import EventConsole, WorldConsole, HUDConsole

from typing import List


ROOT_WIDTH = 80
ROOT_HEIGHT = 50

WORLD_WIDTH = 46
WORLD_HEIGHT = 20

WORLD_SCREEN_X = ROOT_WIDTH - WORLD_WIDTH - 1
WORLD_SCREEN_Y = 1

font = os.path.join('data/fonts/consolas10x10_gs_tc.png')
tcod.console_set_custom_font(
    font, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

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


class Ardor:

    def __init__(self):
        self.player = Player(20, 10, '@', Stats(20))
        self.player.inventory.add_item(Item(
            "Healing Potion", 1.0, 2.0
        ))

        econsole_height = ROOT_HEIGHT // 2
        self.event_console = EventConsole(
            x=1, y=ROOT_HEIGHT-econsole_height,
            width=30, height=econsole_height
        )

        self.world_console = WorldConsole(
            x=WORLD_SCREEN_X, y=WORLD_SCREEN_Y,
            world_map=Map(
                WORLD_WIDTH, WORLD_HEIGHT, SAMPLE_MAP
            ),
            player=self.player
        )

        self.hud_console = HUDConsole(
            x=1, y=1, width=30, height=10, target=self.player
        )

        self.world_console.add_entity(ItemEntity(
            34, 12, "s", Item("Dagger", 1.0, 6.0)
        ))

    def on_enter(self):
        tcod.sys_set_fps(60)
        self.event_console.clear()
        self.world_console.clear()
        self.hud_console.clear()
        self.render(0.0)

    def render(self, delta_time: float) -> None:
        self.event_console.render()
        self.world_console.render()
        self.hud_console.render()

    def blit_consoles(self, target: tcod.console.Console) -> None:
        self.world_console.blit(target)
        self.event_console.blit(target)
        self.hud_console.blit(target)

    def handle_events(self) -> None:
        key = tcod.Key()
        mouse = tcod.Mouse()
        events = []  # type: List[GameEvent]

        EVENT_MASK = tcod.EVENT_MOUSE | tcod.EVENT_KEY_PRESS
        while tcod.sys_check_for_event(EVENT_MASK, key, mouse):
            events += self.on_mouse(mouse)
            events += self.on_key(key)

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

        self.event_console.add_events(events)

    def on_mouse(self, mouse) -> List[GameEvent]:
        return []

    def on_key(self, key: tcod.Key) -> List[GameEvent]:
        MOVE_KEYS = {
            ord('k'): (0, -1),
            ord('h'): (-1, 0),
            ord('j'): (0, 1),
            ord('l'): (1, 0),
        }

        events = []  # type: List[GameEvent]

        if key.c in MOVE_KEYS:
            x, y = MOVE_KEYS[key.c]
            dest_x = self.player.x + x
            dest_y = self.player.y + y

            if SAMPLE_MAP[dest_y][dest_x] == ' ':
                tcod.console_put_char(self.world_console.console,
                                      self.player.x, self.player.y, ' ',
                                      tcod.BKGND_NONE)
                self.player.move_to(dest_x, dest_y)
                tcod.console_put_char(self.world_console.console,
                                      self.player.x, self.player.y, '@',
                                      tcod.BKGND_NONE)
                self.world_console.recompute_lighting = True
                events.append(MovementEvent(self.player, dest_x, dest_y))
        elif key.c == ord('t'):
            self.world_console.recompute_lighting = True
            self.player.torch = not self.player.torch
        elif key.c == ord(','):
            item = self.world_console.pop_item(self.player.x, self.player.y)

            if item is None:
                events.append(NothingThereEvent())
            else:
                result = self.player.inventory.add_item(
                    item.item
                )

                if result != PickupResult.SUCCESS:
                    events.append(InventoryFullEvent(
                        self.player, item.item))
                    self.world_console.add_entity(item)
                else:
                    events.append(PickupEvent(self.player, item.item))

        return events


def main():
    ardor = Ardor()
    ardor.on_enter()
    root_console = tcod.console_init_root(
        ROOT_WIDTH, ROOT_HEIGHT, "ARDOR", False)

    while not tcod.console_is_window_closed():
        root_console.default_fg = (255, 255, 255)
        root_console.default_bg = (0, 0, 0)

        ardor.handle_events()
        ardor.render(tcod.sys_get_last_frame_length())

        ardor.blit_consoles(root_console)

        draw_stats(root_console)
        tcod.console_flush()


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
