import time
from playwright.sync_api import sync_playwright
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')
        page.fill('#A_throat', '-5')
        page.evaluate("document.activeElement.blur()")
        msg = page.evaluate("document.getElementById('A_throat-error').innerText")
        print("Message for A_throat -5:", msg)
        browser.close()
run()
