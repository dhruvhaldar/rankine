import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto('http://127.0.0.1:5000')

        # Add invalid event listener in browser
        page.evaluate("""
            document.querySelectorAll('input, select, textarea').forEach(input => {
                input.addEventListener('invalid', (e) => {
                    const errorMsg = document.getElementById(input.id + '-error');
                    input.setAttribute('aria-invalid', 'true');
                    if (input.validity.patternMismatch && input.title) {
                        errorMsg.textContent = input.title;
                    } else {
                        errorMsg.textContent = input.validationMessage;
                    }
                });
            });
        """)

        page.evaluate("document.getElementById('P0').value = ''")

        page.click('button[type="submit"]') # submit the form

        # screenshot
        page.screenshot(path='screenshot_invalid_event_fixed.png')
        browser.close()

run()
