from playwright.sync_api import sync_playwright
from datetime import datetime
import os

today = datetime.now().strftime("%Y%m%d")

os.makedirs("pdfs", exist_ok=True)

pdf_path = f"pdfs/{today}.pdf"

url = "https://www.windfinder.com/forecast/fyn_nordskov"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    )

    page = browser.new_page(
        viewport={"width": 1440, "height": 2200}
    )

    # Open page
    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=120000
    )

    # Wait for weather table to appear
    page.wait_for_timeout(10000)

    # Generate PDF
    page.pdf(
        path=pdf_path,
        format="A4",
        print_background=True,
        margin={
            "top": "10mm",
            "bottom": "10mm",
            "left": "10mm",
            "right": "10mm"
        }
    )

    browser.close()

print(f"Saved PDF: {pdf_path}")
