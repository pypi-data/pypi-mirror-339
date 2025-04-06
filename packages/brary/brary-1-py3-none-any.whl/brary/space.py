from difflib import get_close_matches

from .location import *
from .essentials import *

class ColorObject:
    def __init__(self, color: str) -> None:
        color = str(color).lower()
        if color in ["grey", "gray"]:
            color = "LIGHTBLACK_EX"
        if color == "brown":
            color = "ansi38m2m139m69m19m"
        if color == "reset":
            color = str(Style.RESET_ALL)
        elif color.startswith("ansi") and color.endswith("m"):
            ansi_codes: list[str] = color.removeprefix("ansi").removesuffix("m").split("m")
            self.color = eval(rf"'\033[{';'.join(ansi_codes)}m'")
        else:
            color = color.upper()
            if not hasattr(Fore, color):
                closest: list[str] = get_close_matches(color, Fore.__dict__)
                raise ValueError(f"no color named {color}.{' did you mean: \''+closest[0]+'\'' if closest else ''}")
            self.color: str = str(getattr(Fore, color))
    def apply(self, string: str) -> str:
        return f"{self.color}{string}{Style.RESET_ALL}"
class _ColorClass:
    def __getattr__(self, item: str) -> ColorObject:
        return ColorObject(item)
Color: _ColorClass = _ColorClass()
class TileTexture:
    def __init__(self, texture: str, color: ColorObject) -> None:
        if len(texture) > 1:
            raise ValueError("texture must be only 1 character.")
        self.texture: str = str(texture)
        self.color: ColorObject = color
    def __str__(self, color: bool = True) -> str:
        return self.color.apply(self.texture) if color else self.texture
class BoardState:
    def __init__(self, space_id: int, location: LocationArray, texture: TileTexture, tag: str) -> None:
        self.space_id: int = space_id
        self.location: LocationArray = location
        self.texture: TileTexture = texture
        self.tag: str = tag
    def __str__(self) -> str:
        return f"{self.space_id} ({self.texture}) at {self.location} with tag '{self.tag}'"
    @staticmethod
    def compare(state1: "BoardState", state2: "BoardState") -> bool:
        return str(state1) == str(state2)
class Piston:
    def __init__(self, board: "Board") -> None:
        self.board: "Board" = board
        self.pushes: int = 0
    def push(self,
        space_id: int,
        key_or_offset: str | LocationOffset,
        distance: int = 1,
        destructive: bool | None = False,
        cannot_go_there_warning: bool = False
    ) -> LocationArray:
        pushes_before: int = self.pushes
        for _ in range(distance):
            offset: LocationOffset = key_or_offset if isinstance(key_or_offset, LocationOffset) else LocationOffset.generate(key_or_offset)
            old_location: LocationArray = self.board.locationById(space_id)
            new_location: LocationArray = offset.apply(old_location)
            if cannot_go_there_warning and not self.board.StatePlacementOperator.checkLocationValidity(self.board, new_location):
                break
            self.board.StatePlacementOperator.ensureLocationValidity(self.board, new_location)
            if self.board.stateTaken(new_location):
                if destructive is True:
                    ...
                elif destructive is False:
                    break
                elif destructive is None:
                    raise ValueError("non-destructive push attempt on occupied location.")
            self.board.StatePlacementOperator(
                self.board,
                space_id,
                new_location,
                self.board.tagById(space_id),
                self.board.textureById(space_id)
            )
            self.board.rmById(space_id)
            self.pushes += 1
        pushes_after: int = self.pushes
        elapsed_pushes: int = pushes_after - pushes_before
        if cannot_go_there_warning and elapsed_pushes == 0:
            print(f"{Fore.RED}cannot go there!{Style.RESET_ALL}")
            time.sleep(0.4)
        return new_location # NOQA
class _SmClass:
    def __matmul__(self, other: int | float) -> tuple[int, int]:
        return int(other), int(other / 2)

Sm = _SmClass()