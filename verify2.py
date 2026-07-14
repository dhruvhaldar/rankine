from playwright.sync_api import sync_playwright, expect

def test_invalid_event_ui(page):
    page.goto('http://127.0.0.1:5000/')

    # 1. Clear a required field completely via JS to avoid input events
    page.evaluate("document.getElementById('P0').value = '';")

    # 2. Click submit
    page.click('button[type="submit"]')

    # Wait for the native invalid event to fire and the custom UI to update
    page.wait_for_timeout(500)

    # 3. Assert that aria-invalid is true and error message is visible
    p0_input = page.locator('#P0')
    expect(p0_input).to_have_attribute('aria-invalid', 'true')

    error_msg = page.locator('#P0-error')
    expect(error_msg).to_be_visible()

    # 4. Take screenshot
    page.screenshot(path='/tmp/verification.png')

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_invalid_event_ui(page)
        finally:
            browser.close()
