# main.py
import os
import time
from datetime import datetime
from typing import List
from fastapi import FastAPI, Body,BackgroundTasks
from pydantic import BaseModel
import shutil

# Import your existing scripts
import website_scraping
import LLM_check



app = FastAPI()

# 1) Define a Pydantic model to parse incoming JSON
class URLList(BaseModel):
    urls: List[str]

@app.get("/")
def read_root():
    return {"message": "Hello World!"}


def cleanup_output_folder():
    folder = "./Output"
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

@app.post("/scrape_and_analyze")
def scrape_and_analyze(input_data: URLList = Body(...),background_tasks: BackgroundTasks = None):
    """
    Endpoint that receives a JSON containing URLs, scrapes each site,
    and returns an LLM-based company description for each.
    """

    # Extract the list of URLs from the request
    urls = input_data.urls

    # 2) Scrape the URLs and save to CSV (with timestamp)
    #    You can call a function from `website_scraping.py` that:
    #    - loops through each URL
    #    - scrapes the website
    #    - saves the content/HTML somewhere
    #    - returns a dictionary or list of (url, scraped_text) for further processing

    # Example: you might create a function in website_scraping.py called `scrape_urls`
    # which returns something like [(url, path_to_html_file), ...] or raw text.
    scraped_results = website_scraping.scrape_urls(urls) 
    # The above function would internally:
    #    - Start Playwright browser
    #    - For each URL, scrape and store
    #    - Write a CSV with the path "Output/<timestamp>_scraping.csv"
    #    - Return a list or dictionary that we can feed into LLM_check.py

    # 3) Analyze each scraped website with LLM_check.py
    #    The LLM_check.py calls `get_openai_response()` from LLM_call_API.py

    final_output = []
    for result in scraped_results:
        url = result["url"]
        text_content = result["plain_text"]

        # Construct the custom prompt for LLM
        # Add the scraped text or a shortened version to the prompt
        AI_role = "You are an experienced company analyst"
        custom_prompt = (
            "Your task is to write a 3-4 sentence long summary of the company "
            "for which we have scraped the website further down. "
            "Focus on what kind of services and products they are active in "
            "and to which industry the company should belong. "
            "Output only in JSON format: Company_Description:str. \n\n"
            f"Website text:\n{text_content}"
        )

        # This function is in LLM_check.py, which in turn calls get_openai_response
        company_description = LLM_check.generate_description(AI_role, custom_prompt)

        # 4) Append to final output
        final_output.append({
            "Website_URL": url,
            "Company_Description": company_description
        })
    
    # Clean Folder
    if background_tasks:
        background_tasks.add_task(cleanup_output_folder)

    # 5) Return the final JSON
    return {"results": final_output}