import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')

        # Clear field first
        page.fill('#P0', '')

        page.type('#P0', '1')
        print("After '1':", page.evaluate("document.getElementById('P0-error').innerText"))

        page.type('#P0', '0')
        print("After '10':", page.evaluate("document.getElementById('P0-error').innerText"))

        page.fill('#P0', '0')
        print("After filling '0':", page.evaluate("document.getElementById('P0-error').innerText"))

        page.fill('#P0', '10')
        print("After filling '10':", page.evaluate("document.getElementById('P0-error').innerText"))

        browser.close()

run()
