import time

from typing import Callable, Any
from colorama import Style, Fore

from .essentials import ScriptHandler

# economy:

class Currency:
    def __init__(self, name: str, sign: str, color: "ColorObject") -> None:
        self.name: str = name
        self.sign: str = sign
        self.color: "ColorObject" = color
    @classmethod
    def setup(cls, name: str) -> "Currency":
        sh: ScriptHandler = ScriptHandler()
        currency: object = sh.createClass(name)
        return cls(name, currency.S, currency.C)
    def apply(self, number: float, *, name: bool = False, sign: bool = True, color: bool = True) -> str:
        return (self.color.apply if color else str)(f"{self.sign if sign else ''}{number}{' '+self.name if name else ''}")

class TaxSystem:
    def __init__(self, name: str, description: str, amount: str, color: "ColorObject", tp: int = 0, hidden: bool = False, every_x_ticks: int = 1, times_effective: int = -1):
        self.name: str = name
        self.description: str = description
        self.amount: str = f"round({amount})"
        self.color: "ColorObject" = color
        self.tp: int = tp
        self.hidden: bool = hidden
        self.every_x_ticks: int = every_x_ticks
        self.times_effective: int = times_effective
        self.times_unpaid: int = 0
    @classmethod
    def setup(cls, name: str) -> "TaxSystem":
        sh: ScriptHandler = ScriptHandler()
        tax_system: object = sh.createClass(name)
        return cls(name, tax_system.D, tax_system.A, tax_system.C, tax_system.H, tax_system.X, tax_system.F)
    def whenUnpaidDno(self) -> None: # dno = do not overwrite (in class children)
        self.times_effective += 1
        self.unpaid()
    def unpaid(self) -> None:
        print(f"{Fore.RED}insufficient funds!{Style.RESET_ALL}")
        exit(1)

class OneTimePayment(TaxSystem):
    def __init__(self, listing: "ShopItemListing") -> None:
        super().__init__(f"purchased {listing.item.name}", listing.item.description, listing.price.amount, listing.color, times_effective=1)

class Wallet:
    def __init__(self, currency: Currency, amount: float, taxes: list[TaxSystem] | None = None, tp: int = 0) -> None:
        self.currency: Currency = currency
        self.amount: float = amount
        self.taxes: list[list[TaxSystem, int, int]] = [] # [tax, tick, times_applied]
        self.tp: int = tp
        if taxes:
            for tax in taxes:
                self.addTax(tax)
    @classmethod
    def setup(cls, name: str) -> "Wallet":
        sh: ScriptHandler = ScriptHandler()
        wallet: object = sh.createClass(name)
        return cls(Currency.setup(wallet.V), wallet.A, [TaxSystem.setup(i) for i in wallet.T])
    def deposit(self, amount: float) -> None:
        self.amount += amount
    def withdraw(self, amount: float) -> bool:
        if amount <= self.amount:
            self.amount -= amount
            return True
        else:
            return False
    def round(self) -> None:
        self.amount = round(self.amount)
    def tick(self, *, delay: float = 1.0) -> None:
        remove: list[int] = []
        for i, (tax, tick, times_applied) in enumerate(self.taxes):
            if tax.tp < self.tp or (tax.tp != -1 and self.tp == -1):
                continue
            if tax.times_effective == times_applied:
                remove.append(i)
                continue
            if tick == tax.every_x_ticks:
                self.tax(tax, delay=delay)
                self.taxes[i][1] = 1
                self.taxes[i][2] += 1
            else:
                self.taxes[i][1] += 1
        for i in remove:
            self.taxes.pop(i)
    def tax(self, tax: TaxSystem, *, delay: float = 1.0) -> None:
        x = self.amount
        amount = eval(tax.amount)
        if self.amount < amount:
            raise ValueError("insufficient funds")
        self.withdraw(amount)
        tick = 1
        if not tax.hidden:
            print(tax.color.apply(f"-{self.currency.apply(amount, color=False)}, ({tax.name}: {tax.description})"))
            time.sleep(delay)
    def addTax(self, tax: TaxSystem) -> None:
        self.taxes.append([tax, 1, 0])
    def __str__(self, **kwargs: Any) -> str:
        return self.currency.apply(self.amount, **kwargs)

# item:

class Item:
    def __init__(self, name: str, description: str, effect: Callable | str) -> None:
        self.name: str = name
        self.description: str = description
        self.effect: Callable = lambda _: print(effect) if isinstance(effect, str) else effect
    @classmethod
    def setup(cls, name: str) -> "Item":
        sh: ScriptHandler = ScriptHandler()
        item: object = sh.createClass(name)
        return cls(listing.N, listing.D, listing.E)
    def use(self, game: "Game", *, delay: float = 2.0) -> None:
        self.effect(game)
        time.sleep(delay)
class ItemInventory:
    def __init__(self, wallet: Wallet, items: list[Item] | None = None) -> None:
        self.wallet: Wallet = wallet
        self.items: list[Item] = items or []
    @classmethod
    def setup(cls) -> "ItemInventory":
        sh: ScriptHandler = ScriptHandler()
        player: object = sh.createClass("Player")
        return cls(Wallet.setup(player.W), [Item.setup(i) for i in player.I])
    def get(self, name: str, if_not_found: Callable | None = None) -> Item:
        for item in self.items:
            if item.name.lower().replace("_", " ") == name.lower().replace("_", " "):
                return item
        if if_not_found:
            return if_not_found
        raise ValueError(f"no item named '{name}' found in the inventory.")
    def add(self, item: Item, *, delay: float = 1.0) -> None:
        print(f"{Fore.MAGENTA}new item received: {item.name}{Style.RESET_ALL}")
        time.sleep(delay)
        self.items.append(item)
    def remove(self, item: Item) -> None:
        for i, l_item in enumerate(self.items):
            if l_item.name == item.name:
                self.items.pop(i)
                return
class ShopItemListing:
    def __init__(self, item: Item, price: Wallet, color: "ColorObject") -> None:
        self.item: Item = item
        self.price: Wallet = price
        self.color: "ColorObject" = color
    @classmethod
    def createItem(cls, name: str, description: str, effect: Callable, price: float, currency: Currency, color: "ColorObject") -> "ShopItemListing":
        return cls(Item(name, description, effect), Wallet(currency, price), color)
    @classmethod
    def fromFunction(cls, price: float, currency: Currency, color: "ColorObject") -> Callable:
        def wrapper1(function: Callable) -> "ShopItemListing":
            return cls.createItem(function.__name__.replace("_", " "), function.__doc__, function, price, currency, color)
        return wrapper1
    @classmethod
    def setup(cls, name: str) -> "ShopItemListing":
        sh: ScriptHandler = ScriptHandler()
        listing: object = sh.createClass(name)
        return cls.createItem(listing.N if hasattr(listing, "N") else name, listing.D, listing.E, listing.P, Currency.setup(listing.V), listing.C)

    def __str__(self) -> str:
        return (f"{self.color.apply(self.item.name)}\n"
                f"- {'\n- '.join(self.item.description.split('\n'))}\n"
                f"- costs: {self.price}")
    def buy(self, inventory: ItemInventory, amount: int = 1, *, delay: float = 1.0) -> None:
        otp: OneTimePayment = OneTimePayment(self)
        try:
            inventory.wallet.tax(otp, delay=delay)
        except ValueError:
            otp.when_unpaid()
            time.sleep(delay)
            return
        inventory.add(self.item, delay=delay)

class Shop:
    def __init__(self, name: str, color: "ColorObject", items: list[ShopItemListing]) -> None:
        self.name: str = name
        self.color: "ColorObject" = color
        self.items: list[ShopItemListing] = items
    @classmethod
    def setup(cls, name: str) -> "Shop":
        sh: ScriptHandler = ScriptHandler()
        shop: object = sh.createClass(name)
        return cls(name, shop.C, [ShopItemListing.setup(i) for i in shop.I])
    def display(self, *, delay: float = 1.0) -> ShopItemListing:
        print(self.color.apply(f"{self.name}:"))
        for i, item in enumerate(self.items, start=1):
            print(f"{Fore.GREEN}{i}. {Style.RESET_ALL}{item}")
        while True:
            try:
                choice: str | int = input("choose an item (1-" + str(len(self.items)) + ") or 'c' to cancel: ").lower()
                if choice == "c":
                    print(f"{Fore.LIGHTBLACK_EX}operation cancelled{Style.RESET_ALL}")
                    time.sleep(delay)
                    return
                choice = int(choice)
            except ValueError:
                print(f"{Fore.RED}invalid choice{Style.RESET_ALL}")
                continue
            if 1 <= choice <= len(self.items):
                return self.items[choice-1]
            else:
                print(f"{Fore.RED}invalid choice{Style.RESET_ALL}")
    def send(self, game: "Game", command: str = "m", enabled: bool = True) -> "Shop":
        game.newShop(self, command)
        game.toggleShop(self, enabled)
        return self

def newItem(name: str, shop_listing: bool = True) -> ShopItemListing:
    item: ShopItemListing = ShopItemListing.setup(name)
    return item if shop_listing else item.item