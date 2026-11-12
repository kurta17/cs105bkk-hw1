# HW1: a Bangkok food-delivery order

**Worth 10% of your grade.** HW1 covers Sessions 1 to 3. You will build the order part of a small food-delivery app: menu items with prices in baht, a "buy 2, get 1 free" promotion, and an order that adds everything up, including delivery.

**Released:** Thu 12 Nov. **Due:** Mon 16 Nov, 23:59.

**Late work:** each day late costs 10% of the mark. You can hand in up to 3 days late; after that, HW1 is not accepted.

## 1. Get your own copy

1. On this repository's GitHub page, click **Use this template** → **Create a new repository**.
2. Owner: your own account. Name: `cs105bkk-hw1`. Click **Create repository**.
3. Clone **your** new repository and open the folder in VS Code:

   ```
   git clone https://github.com/<your-username>/cs105bkk-hw1.git
   ```

## 2. Set up and see red

From the repository folder:

```
python -m venv .venv
```

Activate it. On macOS: `source .venv/bin/activate`. On Windows: `.venv\Scripts\activate`.

```
python -m pip install pytest
python -m pytest
```

Every test fails with `NotImplementedError`. That is the starting point. Each error message names the part you still have to write.

## 3. The story

You are writing the code behind a food-delivery app in Bangkok. A customer picks dishes from a restaurant's menu, the app adds up the order, and a rider brings it. Everything costs whole baht.

Open `delivery.py`. Every function whose body is `raise NotImplementedError(...)` is yours to write. Parts marked **Provided** are already done; read them, but don't change them. Don't change any names or signatures either, because the tests use them.

## 4. Write the code

Work through the parts in this order. Run `python -m pytest` after each one.

### `MenuItem`: one dish on the menu

A menu item has a `name` and a `price` in baht. A price must be more than 0.

1. **`__init__(self, name, price)`** stores the name and the price. Set the price with `self.price = price`, not `self._price = price`, so that the setter checks it.

   ```python
   >>> pad_thai = MenuItem("Pad Thai", 60)
   >>> pad_thai.name, pad_thai.price
   ('Pad Thai', 60)
   ```

2. **The `price` setter** raises `ValueError` if the new price is 0 or less. Otherwise it stores the price in `self._price`. If the price is rejected, the item keeps its old price. The getter is provided.

   ```python
   >>> pad_thai.price = 0
   ValueError: price must be more than 0 baht, got 0
   >>> pad_thai.price
   60
   ```

3. **`__repr__(self)`** returns the developer view: the class name, then the name and the price in brackets. Use `type(self).__name__` for the class name, so that a `PromoItem` (below) shows its own name without any extra code.

   ```python
   >>> MenuItem("Pad Thai", 60)
   MenuItem('Pad Thai', 60)
   >>> PromoItem("Thai iced tea", 40)
   PromoItem('Thai iced tea', 40)
   ```

4. **`__eq__(self, other)`** says two menu items are equal when their names and their prices are equal. If `other` is not a `MenuItem`, return `NotImplemented`; Python then answers `False` for `==` instead of crashing.

   ```python
   >>> MenuItem("Som tam", 50) == MenuItem("Som tam", 50)
   True
   >>> MenuItem("Som tam", 50) == MenuItem("Som tam", 55)
   False
   >>> MenuItem("Som tam", 50) == "Som tam"
   False
   ```

`cost(self, quantity)` is provided: it returns `price * quantity`.

### `PromoItem`: a dish on "buy 2, get 1 free"

A `PromoItem` is a `MenuItem` (it inherits from it), so it already has a name, a checked price, `__repr__` and `__eq__`. Only its cost is different: every third one is free.

5. **`cost(self, quantity)`** works out how many are free, then asks the parent class for the cost of the rest with `super().cost(...)`. Don't repeat the `price * quantity` sum here.

   ```python
   >>> tea = PromoItem("Thai iced tea", 40)
   >>> tea.cost(2)     # no free one yet
   80
   >>> tea.cost(3)     # one free
   80
   >>> tea.cost(7)     # two free, so you pay for 5
   200
   ```

### `Order`: one customer's order

An order has a `customer` and a list called `lines`. Each line is a tuple `(menu_item, quantity)`. An order does not work out prices itself: it asks each menu item for its `cost`. Two class attributes are provided: `delivery_fee = 30` and `free_delivery_from = 300`.

6. **`__init__(self, customer, lines=None)`** stores the customer and the lines. The order must always have **its own new list**:
   - with no `lines`, it starts with a new empty list;
   - with a list of lines, it keeps a copy, so changing the caller's list later doesn't change the order, and adding to the order doesn't change the caller's list.

   This is Session 1's aliasing trap. Two orders must never share one list, and an empty list passed in counts as a list too.

   ```python
   >>> pad_thai = MenuItem("Pad Thai", 60)
   >>> lines = [(pad_thai, 1)]
   >>> order = Order("Nino", lines)
   >>> lines.append((pad_thai, 5))
   >>> order.lines
   [(MenuItem('Pad Thai', 60), 1)]
   ```

7. **`add(self, item, quantity=1)`** adds one line to the order. If `quantity` is less than 1, it raises `ValueError` and adds nothing.

   ```python
   >>> order = Order("Tashi")
   >>> order.add(MenuItem("Mango sticky rice", 80))
   >>> order.lines
   [(MenuItem('Mango sticky rice', 80), 1)]
   >>> order.add(MenuItem("Pad Thai", 60), 0)
   ValueError: quantity must be at least 1, got 0
   ```

8. **`total(self)`** returns what the customer pays:
   - the food cost is the sum of `item.cost(quantity)` over all the lines, so promo items count at their promo price;
   - the delivery fee is added, unless the food costs `free_delivery_from` baht or more;
   - an order with no lines costs 0.

   ```python
   >>> order = Order("Nino")
   >>> order.add(MenuItem("Pad Thai", 60), 2)
   >>> order.total()           # 120 for food, plus 30 delivery
   150
   >>> big = Order("Tashi", [(MenuItem("Khao man gai", 55), 6)])
   >>> big.total()             # 330 for food, delivery is free
   330
   ```

9. **`summary(self)`** returns one text line per order line, in order, like `"2 x Pad Thai"`. Write it as a list comprehension.

   ```python
   >>> order = Order("Tashi")
   >>> order.add(MenuItem("Pad Thai", 60), 2)
   >>> order.add(MenuItem("Mango sticky rice", 80))
   >>> order.summary()
   ['2 x Pad Thai', '1 x Mango sticky rice']
   ```

### `cheapest(options)`: duck typing

10. **`cheapest(options)`** returns the option with the smallest `total()`. If two options have the same total, the first one wins. With an empty list it returns `None`.

    An option can be **anything that has a `total()` method**, not only an `Order`. Maybe it is cheaper to take a motorbike taxi to the stall and eat there. So don't check the type of an option; just call its `total()`.

    ```python
    >>> small = Order("Aung", [(MenuItem("Som tam", 50), 1)])
    >>> big = Order("Aung", [(MenuItem("Pad Thai", 60), 3)])
    >>> cheapest([big, small]) is small
    True
    >>> cheapest([]) is None
    True
    ```

Run `python -m pytest` until every test passes. The tests you see are not all the tests: grading also runs more tests on cases these examples describe, such as the limits and the empty cases. Read each rule above carefully, and try those cases yourself.

## 5. Fill in NOTES.md

Answer the three questions in `NOTES.md`. A few honest sentences each are enough.

## 6. Commit, push, and check Actions

Commit as you go, not only at the end. When you are done:

```
git add delivery.py NOTES.md
git commit -m "Finish HW1"
git push
```

On your repository's GitHub page, open the **Actions** tab. GitHub runs the tests on every push. A green tick means the visible tests passed there too. That result is feedback for you, not your grade. Don't change the test file or the workflow file: changes to either are flagged.

## 7. Upload to Google Classroom

Upload a `.zip` of your repository and paste its link in the HW1 assignment on Google Classroom. Your GitHub repository at the deadline is the copy that is graded.
