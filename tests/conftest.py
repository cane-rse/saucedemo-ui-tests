import pytest
from playwright.sync_api import Page

from data.users import PASSWORD, STANDARD_USER
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(page: Page, login_page: LoginPage) -> InventoryPage:
    """A standard user, already logged in and sitting on the inventory page."""
    login_page.login(STANDARD_USER, PASSWORD)
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)
