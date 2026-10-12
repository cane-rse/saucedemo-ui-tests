import pytest
from playwright.sync_api import expect

from data.users import BACKPACK, BIKE_LIGHT, ONESIE


@pytest.mark.smoke
@pytest.mark.regression
def test_adding_product_updates_cart_badge(inventory_page):
    inventory_page.add_to_cart(BACKPACK)

    expect(inventory_page.cart_badge).to_have_text("1")


@pytest.mark.regression
def test_badge_counts_multiple_products(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    inventory_page.add_to_cart(ONESIE)

    expect(inventory_page.cart_badge).to_have_text("3")


@pytest.mark.regression
def test_cart_lists_the_products_that_were_added(inventory_page, cart_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)

    inventory_page.open_cart()

    assert sorted(cart_page.product_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.regression
def test_removing_from_inventory_clears_badge(inventory_page):
    inventory_page.add_to_cart(BACKPACK)

    inventory_page.remove_from_cart(BACKPACK)

    expect(inventory_page.cart_badge).to_have_count(0)


@pytest.mark.regression
def test_removing_from_cart_page_removes_the_product(inventory_page, cart_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    inventory_page.open_cart()

    cart_page.remove(BACKPACK)

    assert cart_page.product_names() == [BIKE_LIGHT]
    expect(cart_page.cart_badge).to_have_text("1")


@pytest.mark.regression
def test_cart_persists_after_navigating_away(inventory_page, cart_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()

    cart_page.continue_shopping_button.click()

    expect(inventory_page.cart_badge).to_have_text("1")
