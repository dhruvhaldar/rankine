import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')
        page.fill('#A_throat', '10')
        page.fill('#A_exit', '5')
        page.evaluate("document.activeElement.blur()")
        msg = page.evaluate("document.getElementById('A_exit-error').innerText")
        print("Message for A_exit 5 (throat 10):", msg)
        browser.close()

run()
