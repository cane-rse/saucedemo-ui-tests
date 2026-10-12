from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.cancel_button = page.locator("[data-test='cancel']")
        self.error_message = page.locator("[data-test='error']")
        self.subtotal = page.locator("[data-test='subtotal-label']")
        self.tax = page.locator("[data-test='tax-label']")
        self.total = page.locator("[data-test='total-label']")
        self.complete_header = page.locator("[data-test='complete-header']")

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    def continue_to_overview(self) -> None:
        self.continue_button.click()

    def finish(self) -> None:
        self.finish_button.click()

    @staticmethod
    def amount(label_text: str) -> float:
        """'Item total: $39.98' -> 39.98"""
        return float(label_text.split("$")[-1])
