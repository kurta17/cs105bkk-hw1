"""HW1: a Bangkok food-delivery order. Practises Sessions 1-3: aliasing and defaults, comprehensions,
classes with a guarded property, __repr__ and __eq__, inheritance with super(), composition and duck typing."""


class MenuItem:
    """A dish on a restaurant's menu. The price is a whole number of baht."""

    def __init__(self, name: str, price: int):
        """Store the name and the price. The price goes through the setter, so it is checked."""
        raise NotImplementedError("core: store the name, and set the price through the setter")

    @property
    def price(self) -> int:
        """Provided: the price in baht."""
        return self._price

    @price.setter
    def price(self, value: int) -> None:
        """Set the price. Raise ValueError if it is 0 or less, and keep the old price."""
        raise NotImplementedError("core: check the new price, then store it in self._price")

    def __repr__(self) -> str:
        """Return the developer view, for example MenuItem('Pad Thai', 60)."""
        raise NotImplementedError("core: return the developer view, ClassName('name', price)")

    def __eq__(self, other: object) -> bool:
        """Two menu items are equal when their names and prices are equal."""
        raise NotImplementedError("core: compare name and price, or return NotImplemented")

    def cost(self, quantity: int) -> int:
        """Provided: what quantity of this dish costs, in baht."""
        return self.price * quantity


class PromoItem(MenuItem):
    """A dish on a "buy 2, get 1 free" promotion: every third one is free."""

    def cost(self, quantity: int) -> int:
        """Return what quantity costs when every third one is free."""
        raise NotImplementedError("core: work out the free ones, then ask super() for the cost")


class Order:
    """One customer's delivery order: a list of (menu item, quantity) lines."""

    delivery_fee = 30  # Provided: baht added to every order with food in it
    free_delivery_from = 300  # Provided: food worth this much or more is delivered free

    def __init__(self, customer: str, lines: list[tuple[MenuItem, int]] | None = None):
        """Store the customer and a new list of lines. Never share a list with the caller or another order."""
        raise NotImplementedError("core: store the customer and your own new list of lines")

    def add(self, item: MenuItem, quantity: int = 1) -> None:
        """Add one line. Raise ValueError if quantity is less than 1."""
        raise NotImplementedError("core: check the quantity, then add the line")

    def total(self) -> int:
        """Return the food cost plus the delivery fee; free delivery from free_delivery_from; 0 if empty."""
        raise NotImplementedError("core: ask each item for its cost, then add delivery")

    def summary(self) -> list[str]:
        """Return one text line per order line, for example "2 x Pad Thai"."""
        raise NotImplementedError("core: build the summary lines with a list comprehension")


def cheapest(options: list) -> object | None:
    """Return the option with the smallest total(). First one wins a tie; None for an empty list.

    An option can be anything with a total() method, not only an Order.
    """
    raise NotImplementedError("core: return the option whose total() is smallest")
