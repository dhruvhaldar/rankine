from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:5000/')

    # Empty a required field
    page.evaluate("document.getElementById('P0').value = '';")

    # Attempt to submit the form without firing input/blur events on P0
    page.click('button[type="submit"]')

    # Wait to ensure invalid event fires and error message appears
    page.wait_for_timeout(1000)
    page.screenshot(path='screenshot_after_fix.png')

    error_msg = page.locator('#P0-error').text_content()
    print("Error message text:", error_msg)

    browser.close()
