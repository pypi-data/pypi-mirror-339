class _Location:
    SIGN = ""
    def __init__(self, value: int) -> None:
        self.value: int = value
    def __int__(self) -> int:
        return self.value
    def __str__(self) -> str:
        return f"{self.SIGN}{self.value}"
class LocationX(_Location):
    SIGN = "x"
class LocationY(_Location):
    SIGN = "y"
class LocationArray:
    def __init__(self, x: LocationX, y: LocationY) -> None:
        self.x: LocationX = x
        self.y: LocationY = y
    def __iter__(self) -> iter:
        return iter([self.x, self.y])
    def __str__(self) -> str:
        return f"{self.x}{self.y}"
    @staticmethod
    def compare(location1: "LocationArray", location2: "LocationArray") -> bool:
        return str(location1) == str(location2)
    @classmethod
    def from_int(cls, x: int, y: int) -> "LocationArray":
        return cls(LocationX(x), LocationY(y))
class LocationOffset:
    def __init__(self, x_offset: LocationX, y_offset: LocationY) -> None:
        self.x: LocationX = x_offset
        self.y: LocationY = y_offset
    @classmethod
    def generate(cls, key: str) -> "LocationOffset":
        try:
            return cls(LocationX({
                "q": -1, "w": +0, "e": +1,
                "a": -1, "s": +0, "d": +1,
                "z": -1, "x": +0, "c": +1
            }[key]), LocationY({
                "q": +1, "w": +1, "e": +1,
                "a": +0, "s": -1, "d": +0,
                "z": -1, "x": -1, "c": -1
            }[key]))
        except KeyError:
            raise ValueError(f"invalid direction: '{key}'")
    def apply(self, location: LocationArray) -> LocationArray:
        return LocationArray(
            LocationX(
                int(location.x) + int(self.x)
            ),
            LocationY(
                int(location.y) + int(self.y)
            )
        )
    def __iter__(self) -> iter:
        return iter([int(self.x), int(self.y)])

class DirectionObject:
    def __init__(self, key: str) -> None:
        key = key.lower().replace("_", "-")
        try:
            self.__key: str = {
                "up-left": "q",
                "up": "w",
                "up-right": "e",
                "left": "a",
                "right": "d",
                "down-left": "z",
                "down": "x",
                "down-right": "c"
            }[key]
        except KeyError:
            raise ValueError(f"invalid direction: '{key}'")
        self.__name: str = key
        self.__arrow: str = {
            "q": "⬉",
            "w": "⬆",
            "e": "⬈",
            "a": "⬅",
            "s": "⬇",
            "d": "⮕",
            "z": "⬋",
            "x": "⬇",
            "c": "⬊"
        }[self.__key]
        self.__x_offset, self.__y_offset = LocationOffset.generate(self.__key)
    def to_offset(self) -> tuple[int]:
        return self.__x_offset, self.__y_offset
    def to_arrow(self) -> str:
        return self.__arrow
    def to_key(self) -> str:
        return self.__key
    def __str__(self) -> str:
        return self.__name

class _DirectionClass:
    def __getattr__(self, key: str) -> DirectionObject:
        return DirectionObject(key)

Direction: _DirectionClass = _DirectionClass()
ALL_POSSIBLE_DIRECTIONS: list[DirectionObject] = [
    Direction.up_left,
    Direction.up,
    Direction.up_right,
    Direction.left,
    Direction.right,
    Direction.down_left,
    Direction.down,
    Direction.down_right
]

class Route:
    def __init__(self, from_: tuple[int, int], to: tuple[int, int] | str) -> None:
        self.from_: list[int] = list(from_)
        self.to: list[int] = list(to)
    def calculateOptimalDirection(self, use_qezc: bool = True, return_as_str: bool = False) -> Direction:
        x_offset: int = 0
        y_offset: int = 0
        if self.from_[0] < self.to[0]:
            x_offset += 1
        if self.from_[0] > self.to[0]:
            x_offset -= 1
        if self.from_[1] < self.to[1]:
            y_offset += 1
        if self.from_[1] > self.to[1]:
            y_offset -= 1

        for direction in ALL_POSSIBLE_DIRECTIONS:
            if LocationArray.compare(LocationArray(x_offset, y_offset), LocationArray(*direction.to_offset())):
                return direction
    def updateLocation(self, x: int, y: int) -> None:
        self.from_[0] = x
        self.from_[1] = y
    def updateTarget(self, x: int, y: int) -> None:
        self.to[0] = x
        self.to[1] = y
    def __str__(self) -> str:
        return f"x{self.from_[0]}y{self.from_[1]} -> x{self.to[0]}y{self.to[1]}"