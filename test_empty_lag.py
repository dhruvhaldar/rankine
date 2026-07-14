import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')

        # Test backpressure
        page.fill('#back_pressure', '')
        page.type('#back_pressure', '-')
        print("BP After '-':", page.evaluate("document.getElementById('back_pressure-error').innerText"))

        page.type('#back_pressure', '5')
        print("BP After '-5':", page.evaluate("document.getElementById('back_pressure-error').innerText"))

        browser.close()

run()
