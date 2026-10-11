# SauceDemo UI Test Automation

![UI Tests](https://github.com/cane-rse/saucedemo-ui-tests/actions/workflows/ui-tests.yml/badge.svg)

End-to-end UI tests for [SauceDemo](https://www.saucedemo.com/), a practice e-commerce site built for testers. Built with Playwright and pytest using the Page Object Model, and run on Chromium and Firefox in CI.

## What's tested

| Area | Examples | File |
|------|----------|------|
| Login | Valid login, logout, locked-out user, empty and wrong credentials, direct URL access without a session | `tests/test_login.py` |
| Inventory | Product count, sort by name and price (both directions), broken sorting for `problem_user` | `tests/test_inventory.py` |
| Cart | Badge count, cart contents, remove from inventory and from cart, state kept across pages | `tests/test_cart.py` |
| Checkout | Full purchase, required-field validation, total = subtotal + tax, cancel | `tests/test_checkout.py` |

## Tech stack

Python 3.12, pytest, Playwright (pytest-playwright), pytest-html, GitHub Actions.

## Project structure

```
pages/               # Page Objects: locators and actions, no assertions
  base_page.py
  login_page.py
  inventory_page.py
  cart_page.py
  checkout_page.py
tests/               # Test cases: what is verified, written in plain steps
  conftest.py        # fixtures (login_page, logged-in inventory_page, ...)
data/users.py        # credentials, product names, expected error messages
pytest.ini           # base URL, markers, screenshot and trace settings
.github/workflows/ui-tests.yml
```

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                                   # headless
pytest --headed --slowmo 300             # watch it run
pytest --browser firefox                 # another browser
pytest -m smoke                          # critical path only
pytest --html=reports/report.html --self-contained-html
```

After a failure, screenshots and traces are saved in `reports/artifacts/`. Open a trace with:

```bash
playwright show-trace reports/artifacts/<test-folder>/trace.zip
```

## Design decisions

- **Page Object Model:** locators live in one place, so a UI change means editing one file, not twenty tests.
- **No assertions in page objects:** tests own the checks, so reading a test tells you what is being verified.
- **`data-test` locators:** SauceDemo exposes stable test ids, which are less brittle than CSS classes or text.
- **Playwright `expect`:** web-first assertions retry automatically, so there are no `sleep()` calls.
- **Independent tests:** each test starts from a fresh browser context and logs in through a fixture.
- **Failure evidence:** screenshots and traces are captured only on failure and uploaded by CI.
- **Known issues as `xfail`:** SauceDemo ships deliberately broken users such as `problem_user`. The tests document the defect without turning the build red.

## Findings

Fill this in from your own runs, one line per defect, and link each to a written bug report:

| # | User | Defect | Expected | Actual |
|---|------|--------|----------|--------|
| 1 | `problem_user` | Sorting products | List reorders | _your observation_ |
| 2 | | | | |

## Notes

SauceDemo is a public practice site. If a test fails, check whether the site changed its markup before assuming the test is wrong.
