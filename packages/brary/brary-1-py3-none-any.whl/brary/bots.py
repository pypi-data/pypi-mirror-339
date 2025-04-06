from typing import Callable, Any

from .essentials import ScriptHandler
from .location import Route
from .space import Piston


class Bot:
    SERVICES: list[Any] = []
    def __init__(self, game: "Game", tag: str, piston: "Piston", route: Route, speed: int = 1) -> None:
        self.game: "Game" = game
        self.tag: str = tag
        self.piston: "Piston" = piston
        self.route: Route = route
        self.speed: int = speed
        self.completed: bool = False
        for service in self.SERVICES:
            service(self)
    @classmethod
    def setup(cls, game: "Game", tag: str) -> "SimpleBot":
        sh: ScriptHandler = ScriptHandler()
        bot: object = sh.createClass(tag)
        return cls(game, tag, Piston(game.board), Route((bot.X, bot.Y), bot.P), bot.S)
    @classmethod
    def withService(cls, obj: Any) -> None:
        class _Bot(cls):
            SERVICES = cls.SERVICES + [obj]
        return _Bot
    def tick(self, destructive_push: bool | None = False, complete_on_failed_calculation: bool = True, complete_on_failed_push: bool = False) -> None:
        if self.completed:
            return
        direction = self.route.calculateOptimalDirection()
        if direction is None:
            self.completed = complete_on_failed_calculation
            return
        location: "LocationArray | None" = self.piston.push(self.game.board.idByTag(self.tag), direction.to_key(), self.speed, destructive_push)
        if location is None:
            self.completed = complete_on_failed_push
            return
        self.route.updateLocation(int(location.x), int(location.y))
def simpleTracker(tag: str) -> Callable:
    def wrapper(bot: Bot) -> None:
        old_tick_method: Callable = bot.tick
        update_location: Callable = lambda: bot.route.updateTarget(*map(int, bot.game.board.locationByTag(tag)))
        def new_tick_method(destructive_push: bool | None = False, complete_on_failed_push: bool = False) -> None:
            update_location()
            old_tick_method(destructive_push, False, complete_on_failed_push)
        update_location()
        bot.tick = new_tick_method
    return wrapper