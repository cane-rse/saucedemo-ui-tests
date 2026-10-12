from playwright.sync_api import Page


class BasePage:
    """Behavior shared by every page: the page handle, navigation, and the header."""

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.locator("[data-test='logout-sidebar-link']")

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()
