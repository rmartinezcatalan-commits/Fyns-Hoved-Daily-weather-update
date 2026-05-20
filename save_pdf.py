from playwright.sync_api import sync_playwright
from datetime import datetime
from PIL import Image
import os

today = datetime.now().strftime("%Y%m%d")

os.makedirs("output", exist_ok=True)

png_path = f"output/{today}.png"
pdf_path = f"output/{today}.pdf"

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
        viewport={"width": 1600, "height": 5000}
    )

    print("Opening page...")

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=120000
    )

    # wait for javascript rendering
    page.wait_for_timeout(15000)

    # scroll slowly to load forecast tables
    for _ in range(5):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(2000)

    # go back to top
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(3000)

    print("Taking screenshot...")

    page.screenshot(
        path=png_path,
        full_page=True
    )

    browser.close()

print("Converting PNG to PDF...")

image = Image.open(png_path)

if image.mode == "RGBA":
    image = image.convert("RGB")

image.save(pdf_path, "PDF", resolution=100.0)

print(f"Saved PDF: {pdf_path}")
