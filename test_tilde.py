import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('file://' + '/app/test_tilde.html')
        page.screenshot(path='screenshot_tilde.png')
        browser.close()

run()
