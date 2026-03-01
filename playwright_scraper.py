"""
GitHub Action Playwright scraper
Scrapes all tables from Seed 36-45 pages and sums all numeric values.
Writes the total sum to results.txt for GitHub Action artifact upload.
"""

import asyncio
from playwright.async_api import async_playwright

SEEDS = range(36, 46)
BASE_URL = "https://sanand0.github.io/tdsdata/table_sum/index.html"
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

                for table in tables:
                    cells = await table.query_selector_all("td, th")
                    for cell in cells:
                        text = (await cell.text_content()).strip()
                        text = text.replace(",", "")  # remove commas
                        try:
                            number = float(text)
                            total_sum += number
                        except ValueError:
                            continue  # skip non-numeric cells

                print(f"Seed {seed} processed successfully")

            except Exception as e:
                print(f"Error processing seed {seed}: {e}")

        await browser.close()
    return total_sum

async def main():
    total = await scrape_and_sum_tables()
    total_int = int(total)
    print(f"\nTOTAL_SUM={total_int}")

    # Write result to file for GitHub Action artifact
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"TOTAL_SUM={total_int}\n")

if __name__ == "__main__":
    asyncio.run(main())
