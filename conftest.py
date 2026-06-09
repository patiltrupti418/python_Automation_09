# =========================================================
# conftest.py
# Central Pytest Configuration & Fixtures
# =========================================================
import os
import sys
import pytest
import logging
from datetime import datetime
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utilities.config_reader import ConfigReader
from utilities.screenshot_util import ScreenshotUtil
from utilities.logger import setup_logger

setup_logger()

logger = logging.getLogger(__name__)


def pytest_addoption(parser):

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )

    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment: qa, staging, production"
    )

    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run in headless mode: true / false"
    )


def create_driver(browser_name, headless=False):

    logger.info(
        f"Creating browser: {browser_name} "
        f"(headless={headless})"
    )

    if browser_name.lower() == "chrome":

        options = ChromeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=options
        )

    elif browser_name.lower() == "firefox":

        options = FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=FirefoxService(
                GeckoDriverManager().install()
            ),
            options=options
        )

        driver.maximize_window()

    elif browser_name.lower() == "edge":

        options = EdgeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")

        driver = webdriver.Edge(
            service=EdgeService(
                EdgeChromiumDriverManager().install()
            ),
            options=options
        )

    else:
        raise ValueError(
            f"Unsupported browser: {browser_name}"
        )

    driver.implicitly_wait(10)

    driver.set_page_load_timeout(30)

    logger.info(f"Browser created: {browser_name}")

    return driver


@pytest.fixture(scope="function")
def driver(request):

    browser_name = request.config.getoption("--browser")

    env = request.config.getoption("--env")

    headless_opt = request.config.getoption("--headless")

    headless = headless_opt.lower() == "true"

    web_driver = create_driver(
        browser_name,
        headless
    )

    config = ConfigReader(env)

    base_url = config.get_base_url()

    web_driver.get(base_url)

    logger.info(f"Navigated to: {base_url}")

    yield web_driver

    logger.info("Closing browser")

    web_driver.quit()


@pytest.fixture(scope="function")
def config(request):

    env = request.config.getoption("--env")

    return ConfigReader(env)


@pytest.fixture(scope="function")
def login_page(driver):

    from pages.login_page import LoginPage

    return LoginPage(driver)


@pytest.fixture(scope="function")
def home_page(driver):

    from pages.home_page import HomePage

    return HomePage(driver)


@pytest.fixture(scope="function")
def product_page(driver):

    from pages.product_page import ProductPage

    return ProductPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):

    from pages.cart_page import CartPage

    return CartPage(driver)


@pytest.fixture(scope="function")
def checkout_page(driver):

    from pages.checkout_page import CheckoutPage

    return CheckoutPage(driver)


@pytest.fixture(scope="function")
def contact_page(driver):

    from pages.contact_page import ContactPage

    return ContactPage(driver)


@pytest.fixture(scope="function")
def logged_in_driver(driver, config):

    from pages.login_page import LoginPage

    login = LoginPage(driver)

    username = config.get_username()

    password = config.get_password()

    login.login(username, password)

    logger.info(f"Logged in as: {username}")

    yield driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = (
            item.funcargs.get("driver")
            or item.funcargs.get("logged_in_driver")
        )

        screenshot_path = None

        if driver:

            test_name = item.name

            screenshot_path = (
                ScreenshotUtil.capture_screenshot(
                    driver,
                    test_name
                )
            )

        if screenshot_path:

            extra = getattr(report, "extra", [])

            try:
                from pytest_html import extras

                extra.append(
                    extras.image(screenshot_path)
                )

            except ImportError:
                pass

            report.extra = extra

        try:
            import allure

            if screenshot_path:

                allure.attach.file(
                    screenshot_path,
                    name=f"Failure_{test_name}",
                    attachment_type=
                    allure.attachment_type.PNG
                )

        except ImportError:
            pass

        logger.error(
            f"TEST FAILED: {test_name} "
            f"- Screenshot: {screenshot_path}"
        )


def pytest_configure(config):

    dirs = [
        "reports",
        "screenshots",
        "logs",
        "allure-results"
    ]

    root = os.path.dirname(__file__)

    for d in dirs:

        os.makedirs(
            os.path.join(root, d),
            exist_ok=True
        )

    logger.info("Output directories created")


def pytest_terminal_summary(
    terminalreporter,
    exitstatus,
    config
):

    passed = len(
        terminalreporter.stats.get(
            "passed",
            []
        )
    )

    failed = len(
        terminalreporter.stats.get(
            "failed",
            []
        )
    )

    skipped = len(
        terminalreporter.stats.get(
            "skipped",
            []
        )
    )

    total = passed + failed + skipped

    logger.info("=" * 60)

    logger.info("TEST EXECUTION SUMMARY")

    logger.info(
        f"Total: {total} | "
        f"Passed: {passed} | "
        f"Failed: {failed} | "
        f"Skipped: {skipped}"
    )

    logger.info("=" * 60)