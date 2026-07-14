import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')

        # Clear field first
        page.fill('#P0', '')

        page.type('#P0', '-')
        print("After '-':", page.evaluate("document.getElementById('P0-error').innerText"))

        page.type('#P0', '5')
        print("After '-5':", page.evaluate("document.getElementById('P0-error').innerText"))

        page.keyboard.press('Backspace')
        print("After backspace (is '-'):", page.evaluate("document.getElementById('P0-error').innerText"))

        browser.close()

run()
