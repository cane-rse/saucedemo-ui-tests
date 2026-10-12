from playwright.sync_api import Page

from pages.base_page import BasePage


def _slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (matches SauceDemo's data-test ids)."""
    return product_name.lower().replace(" ", "-")


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator("[data-test='title']")
        self.items = page.locator("[data-test='inventory-item']")
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.item_prices = page.locator("[data-test='inventory-item-price']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")

    def add_to_cart(self, product_name: str) -> None:
        self.page.locator(f"[data-test='add-to-cart-{_slug(product_name)}']").click()

    def remove_from_cart(self, product_name: str) -> None:
        self.page.locator(f"[data-test='remove-{_slug(product_name)}']").click()

    def sort_by(self, option_value: str) -> None:
        """option_value is one of: az, za, lohi, hilo."""
        self.sort_dropdown.select_option(option_value)

    def product_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def product_prices(self) -> list[float]:
        return [float(text.replace("$", "")) for text in self.item_prices.all_inner_texts()]
