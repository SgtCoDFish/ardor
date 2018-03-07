import os
import tcod
import random

from ardor.player import Player
from ardor.map import Map
from ardor.item import Item, ItemEntity, Fuel, HealingPotion
from ardor.inventory import PickupResult
from ardor.stats import Stats
from ardor.mobs import Mob
from ardor.ai import AIType
from ardor.events import (
    GameEvent, MovementEvent, NothingThereEvent,
    PickupEvent, InventoryFullEvent, ItemDroppedEvent,
    HealingPotionEvent
)
from ardor.consoles import (
    EventConsole, WorldConsole, HUDConsole, InventoryConsole
)
from ardor.states import State

from typing import List


ROOT_WIDTH = 80
ROOT_HEIGHT = 50

WORLD_WIDTH = 46
WORLD_HEIGHT = 20

WORLD_SCREEN_X = ROOT_WIDTH - WORLD_WIDTH - 1
WORLD_SCREEN_Y = 1

TORCH_DRAIN = 1.5

font = os.path.join('data/fonts/consolas12x12_gs_tc.png')
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

MOVE_KEYS = {
    ord('k'): (0, -1),
    ord('h'): (-1, 0),
    ord('j'): (0, 1),
    ord('l'): (1, 0),
}

MOVE_VKEYS = {
    tcod.KEY_UP: (0, -1),
    tcod.KEY_LEFT: (-1, 0),
    tcod.KEY_DOWN: (0, 1),
    tcod.KEY_RIGHT: (1, 0)
}


class Ardor:

    def __init__(self):
        random.seed(0)
        self.state = State.PLAY

        self.player = Player(20, 10, '@', Stats(20, 100.0))
        self.player.inventory.add_item(HealingPotion(5))
        for i in range(2):
            self.player.inventory.add_item(Fuel(
                "c", "Coal", i + 1.0 + random.random(), 1, 2.0
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

        self.inventory_console = InventoryConsole(
            x=(ROOT_WIDTH // 8), y=(ROOT_HEIGHT // 8),
            width=((ROOT_WIDTH * 3) // 4),
            height=((ROOT_HEIGHT * 3) // 4),
            target=self.player.inventory
        )

        self.mobs = [
            Mob(25, 10, 'G', Stats(5, 5), AIType.MINDLESS)
        ]
        self.world_console.add_entity(ItemEntity(
            34, 12, Item("d", "Dagger", 1.0, 6.0)
        ))

        for m in self.mobs:
            self.world_console.add_entity(m)

    def on_enter(self):
        tcod.sys_set_fps(60)
        self.event_console.clear()
        self.world_console.clear()
        self.hud_console.clear()
        self.render()

    def render(self) -> None:
        self.event_console.render()
        self.world_console.render()
        self.hud_console.render()

        if self.state == State.INVENTORY:
            self.inventory_console.render()

    def blit_consoles(self, target: tcod.console.Console) -> None:
        self.world_console.blit(target)
        self.event_console.blit(target)
        self.hud_console.blit(target)

        if self.state == State.INVENTORY:
            self.inventory_console.blit(target)

    def handle_events(self) -> int:
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
            # elif key.c == ord('q'):
            #     raise SystemExit()

        step_count = sum(int(isinstance(e, MovementEvent)) for e in events)

        self.event_console.add_events(events)

        return step_count

    def handle_ai(self, steps: int) -> None:
        for i in range(steps):
            for mob in self.mobs:
                if mob.ai_type == AIType.MINDLESS:
                    self._do_mindless_ai(mob)
                else:
                    print("WARNING: Unhandled AI type")

    def _do_mindless_ai(self, mob: Mob) -> None:
        if mob.distance_to(self.player) <= 3.0:
            # TODO: attack
            print("ATTACK!", mob.distance_to(self.player))
            return

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(moves)

        if random.random() > 0.75:
            for m in moves:
                dx, dy = m
                newx, newy = mob.x + dx, mob.y + dy
                if self.world_console.map.map.walkable[newy][newx]:
                    mob.move_to(newx, newy)
                    break

    def on_mouse(self, mouse) -> List[GameEvent]:
        return []

    def on_key(self, key: tcod.Key) -> List[GameEvent]:
        if self.state == State.PLAY:
            return self._on_key_play(key)
        elif self.state == State.INVENTORY:
            return self._on_key_inventory(key)
        else:
            print("Unhandled state:", self.state)
            return []

    def _on_key_play(self, key: tcod.Key) -> List[GameEvent]:
        events = []  # type: List[GameEvent]

        if key.vk in MOVE_VKEYS:
            x, y = MOVE_VKEYS[key.vk]
            events += self._do_move(x, y)
        elif key.c in MOVE_KEYS:
            x, y = MOVE_KEYS[key.c]
            events += self._do_move(x, y)
        elif key.c == ord('t'):
            if self.player.torch is True:
                self.world_console.recompute_lighting = True
                self.player.torch = False
            elif self.player.stats.cap >= TORCH_DRAIN:
                self.world_console.recompute_lighting = True
                self.player.torch = True
                self.player.stats.cap -= TORCH_DRAIN
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
        elif key.c == ord('i'):
            self.state = State.INVENTORY

        return events

    def _on_key_inventory(self, key: tcod.Key) -> List[GameEvent]:
        if key.vk == tcod.KEY_ESCAPE:
            self.state = State.PLAY
        elif key.vk in MOVE_VKEYS:
            _, y = MOVE_VKEYS[key.vk]
            self.inventory_console.cursor += y
        elif key.c in MOVE_KEYS:
            x, y = MOVE_KEYS[key.c]
            self.inventory_console.cursor += y
        elif key.vk == tcod.KEY_CHAR:
            item = self.player.inventory.contents[
                self.inventory_console.inventory_index()
            ]

            for name, char in item.actions:
                if key.c != ord(char[0]):
                    continue

                if name == "drop":
                    self.player.inventory.contents.remove(item)

                    item_entity = ItemEntity(
                        self.player.x, self.player.y,
                        item
                    )
                    self.world_console.add_entity(item_entity)
                    return [ItemDroppedEvent(self.player, item)]
                elif name == "quaff":
                    self.player.inventory.contents.remove(item)

                    self.player.stats.hp += item.potency
                    return [HealingPotionEvent(self.player, item.potency)]
                elif name == "capify":
                    self.player.inventory.contents.remove(item)
                    self.player.stats.cap += item.energy_density * item.mass
                else:
                    print("WARNING: unhandled interaction:", name)

        return []

    def _do_move(self, x: int, y: int) -> List[GameEvent]:
        dest_x = self.player.x + x
        dest_y = self.player.y + y

        if SAMPLE_MAP[dest_y][dest_x] == ' ':
            self.player.move_to(dest_x, dest_y)
            tcod.console_put_char(self.world_console.console,
                                  self.player.x, self.player.y, '@',
                                  tcod.BKGND_NONE)
            self.world_console.recompute_lighting = True
            if self.player.torch is True:
                self.player.stats.cap -= TORCH_DRAIN
                if self.player.stats.cap == 0:
                    self.player.torch = False
            return [MovementEvent(self.player, dest_x, dest_y)]

        return []


def main() -> None:
    ardor = Ardor()
    ardor.on_enter()
    root_console = tcod.console_init_root(
        ROOT_WIDTH, ROOT_HEIGHT, "ARDOR", False)

    while not tcod.console_is_window_closed():
        root_console.default_fg = (255, 255, 255)
        root_console.default_bg = (0, 0, 0)

        steps = ardor.handle_events()

        if steps > 0:
            ardor.handle_ai(steps)

        root_console.clear()
        ardor.render()

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
