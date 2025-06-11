from src import scraper
if __name__ == "__main__":

  print("[1] Scraping job postings...")
  job_data = scraper.scrape_jobs()

  print("Done.")
  print(job_data)
