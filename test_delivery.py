import pytest

from delivery import MenuItem, Order, PromoItem, cheapest


def test_core_menu_item_stores_name_and_price():
    item = MenuItem("Pad Thai", 60)
    assert item.name == "Pad Thai"
    assert item.price == 60


def test_core_menu_item_rejects_a_price_of_zero():
    with pytest.raises(ValueError):
        MenuItem("Free water", 0)


def test_core_menu_item_repr():
    assert repr(MenuItem("Pad Thai", 60)) == "MenuItem('Pad Thai', 60)"


def test_core_menu_items_with_the_same_name_and_price_are_equal():
    assert MenuItem("Som tam", 50) == MenuItem("Som tam", 50)
    assert MenuItem("Som tam", 50) != MenuItem("Som tam", 55)
    assert MenuItem("Som tam", 50) != MenuItem("Khao soi", 50)


def test_core_promo_item_gives_every_third_one_free():
    tea = PromoItem("Thai iced tea", 40)
    assert tea.cost(2) == 80
    assert tea.cost(3) == 80


def test_core_promo_item_is_a_menu_item():
    assert isinstance(PromoItem("Thai iced tea", 40), MenuItem)


def test_core_order_total_adds_the_delivery_fee():
    order = Order("Nino")
    order.add(MenuItem("Pad Thai", 60), 2)
    assert order.total() == 150


def test_core_order_total_has_free_delivery_for_a_big_order():
    order = Order("Tashi")
    order.add(MenuItem("Khao man gai", 55), 6)
    assert order.total() == 330


def test_core_order_total_uses_the_promo_price():
    order = Order("Aung")
    order.add(PromoItem("Thai iced tea", 40), 3)
    assert order.total() == 110


def test_core_order_keeps_its_own_copy_of_the_lines():
    pad_thai = MenuItem("Pad Thai", 60)
    lines = [(pad_thai, 1)]
    order = Order("Nino", lines)
    lines.append((pad_thai, 5))
    assert order.lines == [(pad_thai, 1)]


def test_core_add_rejects_a_quantity_of_zero():
    order = Order("Nino")
    with pytest.raises(ValueError):
        order.add(MenuItem("Pad Thai", 60), 0)


def test_core_summary_lists_the_lines():
    order = Order("Tashi")
    order.add(MenuItem("Pad Thai", 60), 2)
    order.add(MenuItem("Mango sticky rice", 80))
    assert order.summary() == ["2 x Pad Thai", "1 x Mango sticky rice"]


def test_core_cheapest_picks_the_smallest_total():
    small = Order("Aung", [(MenuItem("Som tam", 50), 1)])
    big = Order("Aung", [(MenuItem("Pad Thai", 60), 3)])
    assert cheapest([big, small]) is small


def test_core_cheapest_of_nothing_is_none():
    assert cheapest([]) is None
