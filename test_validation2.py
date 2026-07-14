import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')
        page.type('#P0', '-5')
        page.screenshot(path='screenshot3.png')
        msg = page.evaluate("document.getElementById('P0-error').innerText")
        print("Message for -5 (typing):", msg)

        browser.close()

run()
