import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000')

        # Clear P0 programmatically without firing input/blur, or just by using JS?
        # Actually, let's just make P0 empty, then blur, which sets aria-invalid=true.
        # WAIT. If we load the page, P0 is valid.
        # If we remove the 'value' via JS directly to bypass event listeners,
        # or if we click submit while it's valid but another field is invalid?
        # No, if P0 is valid, and we just clear it, `input` fires.

        # Let's reproduce exactly what might happen:
        # What if a user clears the field via some native autofill or form reset?
        # Form reset fires `reset` event. Does it fire `input`? No.

        page.evaluate("document.getElementById('P0').value = ''")
        # now it's invalid, but no input/blur fired.

        page.click('button[type="submit"]') # submit the form

        # screenshot
        page.screenshot(path='screenshot_invalid_event.png')
        browser.close()

run()
