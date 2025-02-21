# website_scraping.py
import os
import time
import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

def sanitize_filename(url: str) -> str:
    # Example sanitize: remove special characters
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', url) + ".html"

def scrape_urls(urls):
    """
    1) Start Playwright
    2) For each URL, scrape the HTML content
    3) Save each HTML file
    4) Write all results to a CSV with timestamp
    5) Return a list of {url, plain_text} so we can feed it to LLM
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv_path = f"./Output/scraping_{timestamp}.csv"

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Folder to save HTMLs
        html_folder = "./Output/"
        os.makedirs(html_folder, exist_ok=True)

        for url in urls:
            print(f"Processing URL: {url}")
            try:
                page = context.new_page()
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(2)
                page_content = page.content()

                # Use BeautifulSoup to parse and extract plain text
                soup = BeautifulSoup(page_content, "lxml")
                plain_text = soup.get_text(separator="\n")

                # Wrap the plain text in minimal HTML
                html_content = f"<html><body><pre>{plain_text}</pre></body></html>"
                
                # Create a sanitized filename
                filename = sanitize_filename(url)
                file_path = os.path.join(html_folder, filename)

                # Save HTML file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"Saved HTML for {url} as {filename}")

                # Collect data for CSV + returning
                results.append({
                    "url": url,
                    "plain_text": plain_text,
                    "filename": filename
                })

                page.close()

            except Exception as e:
                print(f"Error processing URL {url}: {e}")

        context.close()
        browser.close()

    # Write CSV with the scraping results
    with open(output_csv_path, "w", encoding="utf-8", newline="") as csvfile:
        fieldnames = ["url", "filename"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({"url": r["url"], "filename": r["filename"]})

    return results