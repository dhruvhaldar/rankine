import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')

        # Type one character at a time and check message
        page.type('#P0', '-')
        msg = page.evaluate("document.getElementById('P0-error').innerText")
        print("After '-':", msg)

        page.type('#P0', '5')
        msg = page.evaluate("document.getElementById('P0-error').innerText")
        print("After '-5':", msg)

        page.type('#P0', '0')
        msg = page.evaluate("document.getElementById('P0-error').innerText")
        print("After '-50':", msg)

        browser.close()

run()
