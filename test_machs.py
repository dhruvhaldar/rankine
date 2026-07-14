import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')
        page.fill('#machs', 'hello')
        page.evaluate("document.activeElement.blur()")
        msg = page.evaluate("document.getElementById('machs-error').innerText")
        print("Message for 'hello':", msg)

        browser.close()

run()
