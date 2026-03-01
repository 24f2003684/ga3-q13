"""
GitHub Action with Playwright - Scrape table sums
Runs in CI/CD pipeline to sum all table values across multiple pages.
"""

import asyncio
from playwright.async_api import async_playwright
import sys

async def scrape_and_sum_tables():
    """
    Scrape all tables from each seed page and return total sum.
    Seed URLs: 36-45 (10 pages total)
    """
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        total_sum = 0
        base_url = "https://sanand0.github.io/tdsdata/table_sum/index.html"
        
        # Extract numbers from seeds 36 to 45
        for seed in range(36, 46):
            url = f"{base_url}?seed={seed}"
            
            try:
                await page.goto(url)
                await page.wait_for_load_state("networkidle")
                
                # Find all tables and sum their values
                tables = await page.query_selector_all("table")
                
                for table in tables:
                    # Get all td and th elements that contain numbers
                    cells = await table.query_selector_all("td, th")
                    
                    for cell in cells:
                        text = await cell.text_content()
                        text = text.strip()
                        
                        # Try to parse as number
                        try:
                            number = float(text)
                            total_sum += number
                        except ValueError:
                            # Not a number, skip
                            pass
                
                print(f"Seed {seed}: Processed successfully")
                
            except Exception as e:
                print(f"Error processing seed {seed}: {str(e)}")
        
        await browser.close()
        return total_sum

async def main():
    """Main entry point."""
    total = await scrape_and_sum_tables()
    print(f"\nTOTAL_SUM={int(total)}")
    return total

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0)
