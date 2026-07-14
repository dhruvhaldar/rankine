import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')
        page.fill('#P0', '-5')
        page.evaluate("document.activeElement.blur()")
        page.screenshot(path='screenshot2.png')
        msg = page.evaluate("document.getElementById('P0-error').innerText")
        print("Message for -5:", msg)

        page.fill('#P0', '0')
        page.evaluate("document.activeElement.blur()")
        msg = page.evaluate("document.getElementById('P0-error').innerText")
        print("Message for 0:", msg)

        browser.close()

run()
