import pytest
from playwright.sync_api import Page, expect

from data.users import BACKPACK, BIKE_LIGHT, CHECKOUT_INFO, ERRORS


@pytest.fixture
def at_checkout_form(inventory_page, cart_page, checkout_page):
    """Cart holds one product and the browser is on the checkout information form."""
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()
    cart_page.checkout()
    return checkout_page


@pytest.mark.smoke
@pytest.mark.regression
def test_complete_purchase_end_to_end(page: Page, at_checkout_form):
    at_checkout_form.fill_info(**CHECKOUT_INFO)
    at_checkout_form.continue_to_overview()
    at_checkout_form.finish()

    expect(page).to_have_url("/checkout-complete.html")
    expect(at_checkout_form.complete_header).to_have_text("Thank you for your order!")


@pytest.mark.regression
def test_order_total_equals_subtotal_plus_tax(inventory_page, cart_page, checkout_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    inventory_page.open_cart()
    cart_page.checkout()
    checkout_page.fill_info(**CHECKOUT_INFO)
    checkout_page.continue_to_overview()

    subtotal = checkout_page.amount(checkout_page.subtotal.inner_text())
    tax = checkout_page.amount(checkout_page.tax.inner_text())
    total = checkout_page.amount(checkout_page.total.inner_text())

    assert total == pytest.approx(subtotal + tax, abs=0.01)


@pytest.mark.regression
def test_cart_is_empty_after_purchase(at_checkout_form):
    at_checkout_form.fill_info(**CHECKOUT_INFO)
    at_checkout_form.continue_to_overview()
    at_checkout_form.finish()

    expect(at_checkout_form.cart_badge).to_have_count(0)


@pytest.mark.negative
@pytest.mark.parametrize(
    "missing,expected_error",
    [
        ("first_name", "first_name_required"),
        ("last_name", "last_name_required"),
        ("postal_code", "postal_code_required"),
    ],
)
def test_checkout_requires_all_fields(at_checkout_form, missing, expected_error):
    info = {**CHECKOUT_INFO, missing: ""}

    at_checkout_form.fill_info(**info)
    at_checkout_form.continue_to_overview()

    expect(at_checkout_form.error_message).to_have_text(ERRORS[expected_error])


@pytest.mark.negative
def test_cancel_returns_to_cart(page: Page, at_checkout_form):
    at_checkout_form.cancel_button.click()

    expect(page).to_have_url("/cart.html")
