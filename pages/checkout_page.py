# =========================================================
# CheckoutPage - Page Object for Checkout / Place Order
# =========================================================
# Handles: Order form, Purchase, Order confirmation
# Extends: BasePage
# =========================================================

import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """
    CheckoutPage - Handles the Place Order modal and purchase confirmation on demoblaze.com.
    """

    # =========================================================
    # LOCATORS
    # =========================================================

    # Order Form Modal
    ORDER_MODAL = (By.ID, "orderModal")
    NAME_INPUT = (By.ID, "name")
    COUNTRY_INPUT = (By.ID, "country")
    CITY_INPUT = (By.ID, "city")
    CARD_INPUT = (By.ID, "card")
    MONTH_INPUT = (By.ID, "month")
    YEAR_INPUT = (By.ID, "year")
    PURCHASE_BUTTON = (By.XPATH, "//button[text()='Purchase']")
    CLOSE_ORDER_BUTTON = (By.XPATH, "//div[@id='orderModal']//button[text()='Close']")

    # Order Confirmation
    CONFIRMATION_MODAL = (By.CSS_SELECTOR, ".sweet-alert")
    CONFIRMATION_TITLE = (By.CSS_SELECTOR, ".sweet-alert h2")
    CONFIRMATION_TEXT = (By.CSS_SELECTOR, ".sweet-alert .lead")
    CONFIRMATION_OK_BUTTON = (By.CSS_SELECTOR, ".sweet-alert .confirm")

    # =========================================================
    # ACTION METHODS
    # =========================================================

    def fill_name(self, name):
        """Enter customer name"""
        logger.info(f"Entering name: {name}")
        self.enter_text(self.NAME_INPUT, name)

    def fill_country(self, country):
        """Enter country"""
        logger.info(f"Entering country: {country}")
        self.enter_text(self.COUNTRY_INPUT, country)

    def fill_city(self, city):
        """Enter city"""
        logger.info(f"Entering city: {city}")
        self.enter_text(self.CITY_INPUT, city)

    def fill_card(self, card):
        """Enter credit card number"""
        logger.info("Entering card number")
        self.enter_text(self.CARD_INPUT, card)

    def fill_month(self, month):
        """Enter card expiry month"""
        logger.info(f"Entering month: {month}")
        self.enter_text(self.MONTH_INPUT, month)

    def fill_year(self, year):
        """Enter card expiry year"""
        logger.info(f"Entering year: {year}")
        self.enter_text(self.YEAR_INPUT, year)

    def fill_checkout_form(self, name, country, city, card, month, year):
        """
        Fill complete checkout form with customer details.
        Called after clicking 'Place Order' on Cart page.
        """

        logger.info("Filling checkout form")

        self.fill_name(name)
        self.fill_country(country)
        self.fill_city(city)
        self.fill_card(card)
        self.fill_month(month)
        self.fill_year(year)

        logger.info("Checkout form filled successfully")

    def click_purchase(self):
        """Click 'Purchase' button to complete order"""
        logger.info("Clicking Purchase button")

        self.click_element(self.PURCHASE_BUTTON)
        self.hard_wait(2)

    def complete_purchase(self, name, country, city, card, month, year):
        """
        Complete full purchase flow:
        1. Fill checkout form
        2. Click Purchase
        """

        self.fill_checkout_form(name, country, city, card, month, year)
        self.click_purchase()

        logger.info("Purchase completed")

    def close_order_modal(self):
        """Close the order modal without purchasing"""
        logger.info("Closing order modal")

        self.click_element(self.CLOSE_ORDER_BUTTON)

    # =========================================================
    # CONFIRMATION METHODS
    # =========================================================

    def get_confirmation_title(self):
        """Get order confirmation title (e.g., 'Thank you for your purchase!')"""
        logger.info("Getting confirmation title")

        return self.get_text(self.CONFIRMATION_TITLE)

    def get_confirmation_details(self):
        """Get order confirmation details text"""
        logger.info("Getting confirmation details")

        return self.get_text(self.CONFIRMATION_TEXT)

    def click_confirmation_ok(self):
        """Click OK on confirmation dialog"""
        logger.info("Clicking confirmation OK")

        self.click_element(self.CONFIRMATION_OK_BUTTON)
        self.hard_wait(1)

    def is_order_confirmed(self):
        """Check if order confirmation is displayed"""
        return self.is_element_visible(
            self.CONFIRMATION_TITLE,
            timeout=10
        )

    def is_checkout_form_displayed(self):
        """Check if checkout form modal is visible"""
        return self.is_element_visible(
            self.ORDER_MODAL,
            timeout=5
        )