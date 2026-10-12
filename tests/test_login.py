import pytest
from playwright.sync_api import Page, expect

from data.users import ERRORS, LOCKED_OUT_USER, PASSWORD, STANDARD_USER


@pytest.mark.smoke
@pytest.mark.regression
def test_standard_user_can_log_in(page: Page, login_page):
    login_page.login(STANDARD_USER, PASSWORD)

    expect(page).to_have_url("/inventory.html")


@pytest.mark.regression
def test_user_can_log_out(page: Page, login_page, inventory_page):
    inventory_page.logout()

    expect(page).to_have_url("/")
    expect(login_page.login_button).to_be_visible()


@pytest.mark.negative
def test_locked_out_user_sees_error(login_page):
    login_page.login(LOCKED_OUT_USER, PASSWORD)

    expect(login_page.error_message).to_have_text(ERRORS["locked_out"])


@pytest.mark.negative
@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        ("", "", "username_required"),
        ("", PASSWORD, "username_required"),
        (STANDARD_USER, "", "password_required"),
        (STANDARD_USER, "wrong-password", "bad_credentials"),
        ("not-a-user", PASSWORD, "bad_credentials"),
    ],
    ids=["both-empty", "no-username", "no-password", "wrong-password", "unknown-user"],
)
def test_invalid_login_shows_correct_error(login_page, username, password, expected_error):
    login_page.login(username, password)

    expect(login_page.error_message).to_have_text(ERRORS[expected_error])


@pytest.mark.negative
def test_cannot_open_inventory_without_logging_in(page: Page):
    page.goto("/inventory.html")

    expect(page).to_have_url("/")
    expect(page.locator("[data-test='error']")).to_be_visible()
