import os
import tcod
import random

from ardor.player import Player
from ardor.map import Map
from ardor.item import ItemEntity, Fuel, HealingPotion
from ardor.inventory import PickupResult
from ardor.stats import Stats
from ardor.mobs import Mob
from ardor.ai import AIType
from ardor.entity import Battler
from ardor.attack import (  # noqa
    Attack, MeleeAttack, CapBlastAttack, DamageType
)
from ardor.events import (
    GameEvent, MovementEvent, NothingThereEvent,
    PickupEvent, InventoryFullEvent, ItemDroppedEvent,
    HealingPotionEvent, CapifyEvent,
    AttackEvent, DeathEvent, PlayerDeathEvent,
    TakeAimEvent, NeverMindEvent, BlastFizzleEvent, BlastMissEvent,
    FailedDescendEvent, DescendEvent, GameStartEvent
)
from ardor.consoles import (
    EventConsole, WorldConsole, HUDConsole, InventoryConsole,
    WinConsole, ControlsConsole, IntroConsole, GameOverConsole
)
from ardor.states import State
from ardor.worlds import World
from ardor.worlds import World1, World2, World3

from typing import List, Iterator, MutableSet, Tuple, Type  # noqa


ROOT_WIDTH = 80
ROOT_HEIGHT = 50

TORCH_DRAIN = 1.25

font = os.path.join('data/fonts/consolas12x12_gs_tc.png')
tcod.console_set_custom_font(
    font, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

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
        self.state = State.INTRO

        self.worlds = [
            World1(ROOT_WIDTH),
            World2(ROOT_WIDTH),
            World3(ROOT_WIDTH)
        ]

        self.world_counter = 0
        self.current_world = self.worlds[self.world_counter]

        self.player = Player(
            self.current_world.player_start_x,
            self.current_world.player_start_y, '@',
            Stats(30, 50.0, 5, 2, 10, 3)
        )
        self.player.stats.cap = self.player.stats.max_cap

        self.player.inventory.add_item(HealingPotion(5))
        for i in range(2):
            self.player.inventory.add_item(Fuel(
                "c", "Coal", i + 1.5 + random.random(), 1, 2.75
            ))

        self.attacks = []  # type: List[Attack]
        self.aim_type = None  # type: Type[Attack]

        econsole_height = ROOT_HEIGHT // 2
        self.event_console = EventConsole(
            x=1, y=ROOT_HEIGHT-econsole_height,
            width=30, height=econsole_height
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

        self.win_console = WinConsole(
            x=(ROOT_WIDTH // 8), y=(ROOT_HEIGHT // 8),
            width=((ROOT_WIDTH * 3) // 4),
            height=((ROOT_HEIGHT * 3) // 4)
        )

        self.intro_console = IntroConsole(
            x=(ROOT_WIDTH - 46) // 2,
            y=(ROOT_HEIGHT - 20) // 2,
            width=46,
            height=20
        )

        self.game_over_console = GameOverConsole(
            x=(ROOT_WIDTH - 37) // 2,
            y=(ROOT_HEIGHT - 15) // 2,
            width=37,
            height=15
        )

        control_width = 31
        control_height = 18
        self.controls_console = ControlsConsole(
            x=ROOT_WIDTH - control_width,
            y=ROOT_HEIGHT - control_height,
            width=control_width, height=control_height
        )

        self.init_world(self.current_world)

    def init_world(self, world: World) -> None:
        self.current_world = world
        self.world_console = WorldConsole(
            x=self.current_world.x, y=self.current_world.y,
            world_map=Map(
                self.current_world.width, self.current_world.height,
                self.current_world.base_map
            ),
            player=self.player
        )

        self.player.x = self.current_world.player_start_x
        self.player.y = self.current_world.player_start_y

        for i in self.current_world.items:
            self.world_console.add_entity(i)

        for m in self.current_world.mobs:
            self.world_console.add_entity(m)

    def on_enter(self) -> None:
        tcod.sys_set_fps(60)
        self.intro_console.clear()
        self.game_over_console.clear()
        self.event_console.clear()
        self.world_console.clear()
        self.hud_console.clear()
        self.controls_console.clear()
        self.render()

    def render(self) -> None:
        self.event_console.render()
        self.world_console.render()
        self.hud_console.render()
        self.controls_console.render()

        if self.state == State.INTRO:
            self.intro_console.render()
        elif self.state == State.INVENTORY:
            self.inventory_console.render()
        elif self.state == State.WON:
            self.win_console.render()
        elif self.state == State.GAME_OVER:
            self.game_over_console.render()

    def blit_consoles(self, target: tcod.console.Console) -> None:
        self.world_console.blit(target)
        self.event_console.blit(target)
        self.hud_console.blit(target)
        self.controls_console.blit(target)

        if self.state == State.INTRO:
            self.intro_console.blit(target)
        elif self.state == State.INVENTORY:
            self.inventory_console.blit(target)
        elif self.state == State.WON:
            self.win_console.blit(target)
        elif self.state == State.GAME_OVER:
            self.game_over_console.blit(target)

    def handle_events(self) -> List[GameEvent]:
        key = tcod.Key()
        mouse = tcod.Mouse()
        events = []  # type: List[GameEvent]

        EVENT_MASK = tcod.EVENT_MOUSE | tcod.EVENT_KEY_PRESS
        while tcod.sys_check_for_event(EVENT_MASK, key, mouse):
            events += self.on_mouse(mouse)
            events += self.on_key(key)

            # if key.vk == tcod.KEY_ENTER and key.lalt:
            #     tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
            # elif key.vk == tcod.KEY_PRINTSCREEN or key.c == 'p':
            #     print("screenshot")
            #     if key.lalt:
            #         tcod.console_save_apf(None, "samples.apf")
            #         print("apf")
            #     else:
            #         tcod.sys_save_screenshot()
            #         print("png")
            # elif key.c == ord('q'):
            #     raise SystemExit()

        return events

    def handle_ai(self, steps: int) -> List[GameEvent]:
        events = []

        for i in range(steps):
            for mob in self.current_world.mobs:
                if mob.ai_type == AIType.MINDLESS:
                    events += self._do_mindless_ai(mob)
                else:
                    print("WARNING: Unhandled AI type")

        return events

    def process_attacks(self) -> List[GameEvent]:
        events = []  # type: List[GameEvent]
        dead = set()  # type: MutableSet[Tuple[Battler, Attack]]

        for a in self.attacks:
            if a.damage_type == DamageType.PHYSICAL:
                damage = a.attacker.stats.attack - a.target.stats.defence
            elif a.damage_type == DamageType.SPECIAL:
                damage = a.attacker.stats.intelligence - a.target.stats.spirit
            else:
                damage = 1
                print("WARNING: unknown damage type")
            a.target.stats.hp -= damage
            events.append(AttackEvent(a, damage))
            if a.target.stats.hp == 0:
                dead.add((a.target, a))

        self.attacks.clear()

        for d, a in dead:
            if d is self.player:
                events.append(PlayerDeathEvent(d, a))
                self.state = State.GAME_OVER
            else:
                events.append(DeathEvent(d, a))
                self.current_world.mobs.remove(d)
                self.world_console.remove_entity(d)
                if d.inventory.size() > 0:
                    i = random.choice(d.inventory.contents)
                    d.inventory.remove_item(i)

                    self.world_console.add_entity(ItemEntity(d.x, d.y, i))

        return events

    def _do_mindless_ai(self, mob: Mob) -> List[GameEvent]:
        attack = mob.do_attack(self.player)
        if attack is not None:
            self.attacks.append(attack)
            return []

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(moves)

        if random.random() > 0.75:
            for m in moves:
                dx, dy = m
                newx, newy = mob.x + dx, mob.y + dy
                if self.world_console.map.map.walkable[newy][newx]:
                    self.world_console.entity_grid[mob.y][mob.x].remove(mob)
                    mob.move_to(newx, newy)
                    self.world_console.entity_grid[newy][newx].append(mob)
                    break

            return [MovementEvent(mob, newx, newy)]

        return []

    def on_mouse(self, mouse) -> List[GameEvent]:
        return []

    def on_key(self, key: tcod.Key) -> List[GameEvent]:
        if self.state == State.PLAY:
            return self._on_key_play(key)
        elif self.state == State.INVENTORY:
            return self._on_key_inventory(key)
        elif self.state == State.AIMING:
            return self._on_key_aiming(key)
        elif self.state == State.WON:
            return []
        elif self.state == State.INTRO:
            return self._on_key_intro(key)
        elif self.state == State.GAME_OVER:
            return []
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
            if key.shift:
                stairs = self.world_console.get_stairs(
                    self.player.x, self.player.y)
                if stairs is not None:
                    self.world_counter += 1
                    if self.world_counter == len(self.worlds):
                        self.state = State.WON
                    else:
                        self.init_world(self.worlds[self.world_counter])

                    return [DescendEvent(self.player)]
                else:
                    return [FailedDescendEvent(self.player)]

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
        elif key.c == ord('b'):
            if self.player.stats.cap < 10:
                events.append(BlastFizzleEvent())
            else:
                self.state = State.AIMING
                self.aim_type = CapBlastAttack
                events.append(TakeAimEvent())
        elif key.c == ord(']'):
            print("(x, y) = ({}, {})".format(self.player.x, self.player.y))

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
            try:
                idx = self.inventory_console.inventory_index()
                item = self.player.inventory.contents[idx]
            except IndexError:
                return []

            for name, char in item.actions:
                if key.c != ord(char[0]):
                    continue

                if name == "drop":
                    self.player.inventory.remove_item(item)

                    item_entity = ItemEntity(
                        self.player.x, self.player.y,
                        item
                    )
                    self.world_console.add_entity(item_entity)
                    return [ItemDroppedEvent(self.player, item)]
                elif name == "quaff":
                    self.player.inventory.remove_item(item)

                    self.player.stats.hp += item.potency
                    return [HealingPotionEvent(self.player, item)]
                elif name == "capify":
                    self.player.inventory.remove_item(item)
                    cap_val = item.energy_density * item.mass
                    self.player.stats.cap += cap_val
                    return [CapifyEvent(self.player, item, cap_val)]
                else:
                    print("WARNING: unhandled interaction:", name)

        return []

    def _on_key_aiming(self, key: tcod.Key) -> List[GameEvent]:
        if key.vk in MOVE_VKEYS:
            x, y = MOVE_VKEYS[key.vk]
            return self._do_aim_type(x, y)
        elif key.c in MOVE_KEYS:
            x, y = MOVE_KEYS[key.c]
            return self._do_aim_type(x, y)
        elif key.vk == tcod.KEY_ESCAPE:
            self.state = State.PLAY
            return [NeverMindEvent()]

        return []

    def _on_key_intro(self, key: tcod.Key) -> List[GameEvent]:
        if key.vk == tcod.KEY_SPACE:
            self.state = State.PLAY
            return [GameStartEvent(self.player)]

        return []

    def _do_aim_type(self, x_dir: int, y_dir: int) -> List[GameEvent]:
        self.state = State.PLAY
        self.player.stats.cap -= 10.0

        for i in range(1, self.aim_type.max_range + 1):
            e = self.world_console.get_battler(
                self.player.x + x_dir * i,
                self.player.y + y_dir * i
            )

            if e is not None:
                atk = self.aim_type(self.player, e)
                self.attacks.append(atk)
                return []

        return [BlastMissEvent()]

    def _do_move(self, x: int, y: int) -> List[GameEvent]:
        dest_x = self.player.x + x
        dest_y = self.player.y + y

        thing = self.world_console.is_walkable(dest_x, dest_y)

        if thing is True:
            self.player.move_to(dest_x, dest_y)
            self.world_console.recompute_lighting = True
            if self.player.torch is True:
                self.player.stats.cap -= TORCH_DRAIN
                if self.player.stats.cap == 0:
                    self.player.torch = False
            return [MovementEvent(self.player, dest_x, dest_y)]

        if thing is not None:
            if isinstance(thing, Battler):
                atk = MeleeAttack(self.player, thing)
                self.attacks.append(atk)
                return []
            else:
                return []

        return []


def main() -> None:
    # random.seed(0)
    ardor = Ardor()
    ardor.on_enter()
    root_console = tcod.console_init_root(
        ROOT_WIDTH, ROOT_HEIGHT, "ARDOR", False)

    while not tcod.console_is_window_closed():
        root_console.default_fg = (255, 255, 255)
        root_console.default_bg = (0, 0, 0)

        events = ardor.handle_events()

        events += ardor.process_attacks()
        steps = sum(e.steps for e in events)

        if steps > 0:
            events += ardor.handle_ai(steps)
            events += ardor.process_attacks()

        ardor.event_console.add_events(events)

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
