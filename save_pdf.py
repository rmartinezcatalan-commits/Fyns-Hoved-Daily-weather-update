from playwright.sync_api import sync_playwright
from datetime import datetime
from pathlib import Path
import os

today = datetime.now().strftime("%Y%m%d")

os.makedirs("pdfs", exist_ok=True)

pdf_path = f"pdfs/{today}.pdf"

url = "https://www.windfinder.com/forecast/fyn_nordskov"

with sync_playwright() as p:
 browser = p.chromium.launch(
    headless=True,
    args=["--no-sandbox", "--disable-setuid-sandbox"]
)
    page = browser.new_page()

    page.goto(url, wait_until="networkidle")

    page.pdf(
        path=pdf_path,
        format="A4",
        print_background=True
    )

    browser.close()

print(f"Saved PDF: {pdf_path}")
