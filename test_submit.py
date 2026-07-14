import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')
        page.fill('#P0', '') # Empty the field
        page.click('button[type="submit"]') # click calculate
        page.screenshot(path='screenshot_submit.png')
        browser.close()

run()
