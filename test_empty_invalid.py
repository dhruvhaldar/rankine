import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')
        # clear an input
        page.fill('#P0', '')
        page.evaluate("document.activeElement.blur()")
        page.screenshot(path='screenshot_empty.png')
        browser.close()

run()
