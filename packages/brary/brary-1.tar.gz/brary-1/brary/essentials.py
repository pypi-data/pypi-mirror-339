import os, random, time

from pathlib import Path
from typing import Any, Literal, Callable
from colorama import Style, Fore

from .location import *
from .space import *

class ScriptHandler:
    def __init__(self) -> None:
        ...
    def addClass(self, cls: type):
        self.__dict__ |= {
            f"{cls.__name__.capitalize()}Class": cls,
            cls.__name__.lower(): cls()
        }
    @staticmethod
    def createClassFromString(name: str, s: str) -> type:
        class_name: str = name.replace("-", "_")
        s = "..." if not s else s
        lns: list[str] = f"""
from brary import *
class {class_name}:
    def __getattr__(self, name: str) -> None:
        raise AttributeError(f"attempted to retrieve {name} attribute '{{name}}', but it is not defined in the {name} script.")
        """.strip().split("\n") + [f"    {ln}" for ln in s.split("\n")]
        s = "\n".join(lns)
        exec(s)
        return locals()[class_name]()
    @staticmethod
    def createClass(name: str) -> type:
        new_name: str = ""
        set_upper: bool = False
        for char in name:
            if char == " ":
                set_upper = True
            elif set_upper:
                new_name += char.upper()
                set_upper = False
            else:
                new_name += char
        name = new_name
        scripts_path: Path = Path(os.getcwd()) / "scripts"
        file_path: Path = scripts_path / name
        if not scripts_path.exists():
            raise FileNotFoundError(f"sh setup() requires a scripts directory in your current working directory ({os.getcwd()}). you can run 'mkdir {scripts_path}' to create it.")
        if not file_path.exists():
            raise FileNotFoundError(f"sh setup() requires {name} script in {scripts_path}")
        with file_path.open() as file:
            code: str = file.read()
        return ScriptHandler.createClassFromString(name, code)
class Game:
    def __init__(self, board: "Board") -> None:
        self.board: "Board" = board
        self.player: object = ScriptHandler.createClass("Player")
        self.player.inventory_enabled = True
        self.piston: Piston = board.new(Piston)
        self.tos: "list[object]" = [] # tick objects
        self.shops: "list[Shop, str, bool]" = [] # [shop, command, enabled]
    def nto(self, obj: object) -> None: # new tick object
        self.tos.append(obj)
        return obj
    def newShop(self, shop: "Shop", command: str) -> None:
        self.shops.append([shop, command, True])
    def toggleShop(self, shop: "Shop | int", to: bool | None = None) -> None: # 'to' argument toggles when set to None
        shop = self.shops[shop] if isinstance(shop, int) else shop
        for iter_shop in self.shops:
            if iter_shop[0].name == shop.name:
                iter_shop[2] = not iter_shop[2] if to is None else to
    def newInventory(self, ii_cls: type | None = None) -> None:
        from .economy import ItemInventory

        ii_cls = ii_cls or ItemInventory
        self.player.inventory = ii_cls.setup()
    def loop(self, clear: bool = True, until: Callable | bool = False, player_tag: str = "Player", *, dno_secured: bool = False) -> None:
        if not dno_secured:
            try:
                self.loop(clear, until, player_tag, dno_secured=True)
            except (KeyboardInterrupt, EOFError):
                ...
            return
        while not (until() if callable(until) else until):
            for obj in self.tos:
                obj.tick()
            if clear:
                os.system("cls" if os.name == "nt" else "clear")
            print(self.board.render())
            q: str = input("> ")
            if q in list("qweasdzxc"):
                self.piston.push(self.board.idByTag(player_tag), q, self.player.S, cannot_go_there_warning=True)
            elif q == "i":
                if not hasattr(self.player, "inventory") or not self.player.inventory_enabled:
                    print(f"{Fore.RED}inventory unavailable!{Style.RESET_ALL}")
                    time.sleep(0.4)
                    continue
                print(f"{Fore.GREEN}inventory:{Style.RESET_ALL}")
                print(f"1. {self.player.inventory.wallet}")
                print(*([f"{i}. {item.name}" for i, item in enumerate(self.player.inventory.items, start=2)] or [f"{Fore.LIGHTBLACK_EX}...nothing in inventory...{Style.RESET_ALL}"]), sep="\n")
                while True:
                    try:
                        q2: str | int = input(f"{Fore.LIGHTBLACK_EX}press <return> to close inventory or type command here: {Style.RESET_ALL}").lower()
                        if q2 == "":
                            break
                        q2 = int(q2) - 2
                        if q2 < 0:
                            continue
                    except ValueError:
                        print(f"{Fore.RED}invalid command{Style.RESET_ALL}")
                        time.sleep(0.4)
                        continue
                    if q2 < len(self.player.inventory.items):
                        print(f"{Fore.LIGHTBLACK_EX}using {self.player.inventory.items[q2].name}{Style.RESET_ALL}")
                        self.player.inventory.items[q2].use(self)
                        break
            else:
                if self.player.inventory_enabled:
                    for shop in self.shops:
                        if q == shop[1] and shop[2] is True:
                            item: "ShopItemListing" = shop[0].display()
                            if item is not None:
                                item.buy(self.player.inventory)
                            break

class Board:
    def __init__(self, size: LocationArray, bg: TileTexture) -> None:
        self.size: LocationArray = size
        self.states: list[BoardState] = []
        self.bg: TileTexture = bg
    @classmethod
    def setup(cls) -> "Board":
        sh: ScriptHandler = ScriptHandler()
        board: object = sh.createClass("Board")
        return cls(LocationArray(LocationX(board.W), LocationY(board.H)), TileTexture(board.T, board.C))
    @staticmethod
    def generateRandomSpaceId() -> int:
        return random.randint(0, 999999)
    def new(self, cls: type) -> Any:
        return cls(self)
    def stateTaken(self, location: LocationArray) -> bool:
        for state in self.states:
            if LocationArray.compare(state.location, location):
                return state
        return False
    class StatePlacementOperator:
        def __init__(
            self,
            board: "Board",
            space_id: int,
            location: LocationArray,
            tag: str,
            texture: TileTexture,
            overwrite: bool = True
        ) -> None:
            self.board: "Board" = board
            self.ensureLocationValidity(board, location)
            state: BoardState | False = board.stateTaken(location)
            if not overwrite and state is not False:
                raise ValueError(f"location {location} already taken.")
            for i, state2 in enumerate(board.states):
                if BoardState.compare(state, state2):
                    board.states.pop(i)
            board.states.append(BoardState(space_id, location, texture, tag))
            self.__state: BoardState = board.states[-1]
        def fetch(self) -> BoardState:
            return self.__state
        @staticmethod
        def checkLocationValidity(board: "Board", location: LocationArray) -> bool | str:
            return not any([
                int(location.x) > int(board.size.x),
                int(location.y) > int(board.size.y),
                int(location.x) <= 0,
                int(location.y) <= 0
            ])
        @staticmethod
        def ensureLocationValidity(board: "Board", location: LocationArray) -> None:
            if not Board.StatePlacementOperator.checkLocationValidity(board, location):
                raise ValueError(f"location {location} is out of bounds.")
    def lookFor(self, formula: str, **vars: Any) -> Any:
        for i, state in enumerate(self.states):
            if eval(formula, globals() | locals() | vars, {}):
                return i, state
        return 0, None

    def rmByState(self, state: BoardState) -> None:
        i, state = self.lookFor(f"state.space_id == space_id", space_id=state.space_id)
        if state is None:
            raise ValueError(f"tile with id '{space_id}' not found.")
        self.states.pop(i)

    # by id:

    def stateById(self, space_id: int) -> BoardState:
        return self.lookFor(f"state.space_id == space_id", space_id=space_id)[1]
    def locationById(self, space_id: int) -> LocationArray:
        return self.stateById(space_id).location
    def tagById(self, space_id: int) -> LocationArray:
        return self.stateById(space_id).tag
    def textureById(self, space_id: int) -> LocationArray:
        return self.stateById(space_id).texture
    def rmById(self, space_id: int) -> None:
        self.rmByState(self.stateById(space_id))

    # by tag:

    def stateByTag(self, tag: str) -> BoardState:
        return self.lookFor(f"state.tag == tag", tag=tag)[1]
    def locationByTag(self, tag: str) -> LocationArray:
        return self.stateByTag(tag).location
    def idByTag(self, tag: str) -> int:
        return self.stateByTag(tag).space_id
    def textureByTag(self, tag: str) -> LocationArray:
        return self.stateByTag(tag).texture
    def rmByTag(self, tag: str) -> None:
        self.rmByState(self.stateByTag(tag))

    # by location:

    def stateByLocation(self, location: LocationArray) -> BoardState:
        return self.lookFor(f"LocationArray.compare(state.location, location)", location=location)[1]
    def idByLocation(self, location: LocationArray) -> int:
        return self.stateByLocation(location).space_id
    def tagByLocation(self, location: LocationArray) -> str:
        return self.stateByLocation(location).tag
    def textureByLocation(self, location: LocationArray) -> LocationArray:
        return self.stateByLocation(location).texture
    def rmByLocation(self, location: LocationArray) -> None:
        self.rmByState(self.stateByLocation(location))

    def create(self, tag: str, name: str | None = None) -> object:
        """name parameter defaults to tag"""
        name = tag if name is None else name
        space_cls: type = ScriptHandler.createClass(name)
        space_id: int = self.generateRandomSpaceId()
        class new_space_cls(space_cls.__class__):
            id = space_id
            def rm(self1):
                self.rmById(space_id)
        space: new_space_cls = new_space_cls() # NOQA
        location_x: int = space.X
        location_y: int = space.Y
        texture: str = space.T
        color: str | ColorObject = space.C
        self.StatePlacementOperator(
            self,
            space_id,
            LocationArray(
                LocationX(location_x),
                LocationY(location_y)
            ),
            tag,
            TileTexture(
                texture,
                ColorObject(color) if isinstance(color, str) else color
            )
        )
        return space
    def render(self) -> str:
        lns = []
        for y in range(-int(self.size.y), 0):
            ln = [
                str(self.bg)
                if not self.stateTaken(LocationArray.from_int(x, -y))
                else str(self.stateTaken(LocationArray.from_int(x, -y)).texture)
                for x in range(1, int(self.size.x) + 1)
            ]
            lns.append("".join(ln))
        return "\n".join(lns)