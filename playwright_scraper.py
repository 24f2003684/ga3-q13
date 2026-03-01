"""
Playwright scraper for DataDash QA case study
Scrapes tables from Seed 36-45 pages and sums all numeric values.
Writes the total to results.txt and prints it in logs.
"""

import asyncio
from playwright.async_api import async_playwright

SEEDS = range(36, 46)
BASE_URL = "https://sanand0.github.io/tdsdata/js_table/"
OUTPUT_FILE = "results.txt"

async def scrape_and_sum_tables():
    total_sum = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for seed in SEEDS:
            url = f"{BASE_URL}?seed={seed}"
            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("networkidle")

                tables = await page.query_selector_all("table")

                seed_total = 0
                for table in tables:
                    cells = await table.query_selector_all("td, th")
                    for cell in cells:
                        text = (await cell.text_content()).strip().replace(",", "")
                        try:
                            number = float(text)
                            seed_total += number
                            total_sum += number
                        except ValueError:
                            continue

                print(f"Seed {seed} subtotal: {int(seed_total)}")

            except Exception as e:
                print(f"Error processing Seed {seed}: {e}")

        await browser.close()
    return total_sum

async def main():
    total = await scrape_and_sum_tables()
    total_int = int(total)

    # Print clearly for GitHub Action checker
    print(f"\nTOTAL_SUM={total_int}")

    # Save to results.txt for artifact upload
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"TOTAL_SUM={total_int}\n")

if __name__ == "__main__":
    asyncio.run(main())
