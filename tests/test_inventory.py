import pytest
from playwright.sync_api import expect

from data.users import PASSWORD, PROBLEM_USER


@pytest.mark.smoke
@pytest.mark.regression
def test_inventory_shows_six_products(inventory_page):
    expect(inventory_page.title).to_have_text("Products")
    expect(inventory_page.items).to_have_count(6)


@pytest.mark.regression
def test_sort_by_name_ascending(inventory_page):
    inventory_page.sort_by("az")

    names = inventory_page.product_names()
    assert names == sorted(names)


@pytest.mark.regression
def test_sort_by_name_descending(inventory_page):
    inventory_page.sort_by("za")

    names = inventory_page.product_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.regression
def test_sort_by_price_low_to_high(inventory_page):
    inventory_page.sort_by("lohi")

    prices = inventory_page.product_prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_sort_by_price_high_to_low(inventory_page):
    inventory_page.sort_by("hilo")

    prices = inventory_page.product_prices()
    assert prices == sorted(prices, reverse=True)


@pytest.mark.known_issue
@pytest.mark.xfail(reason="problem_user is a deliberately broken demo account: sorting does not work", strict=False)
def test_problem_user_can_sort_products(page, login_page, inventory_page):
    inventory_page.logout()
    login_page.login(PROBLEM_USER, PASSWORD)

    inventory_page.sort_by("za")

    names = inventory_page.product_names()
    assert names == sorted(names, reverse=True)
