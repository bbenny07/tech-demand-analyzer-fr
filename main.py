from src import scraper
from src import analyzer
from src import visualize
if __name__ == "__main__":

  print("[scraper] Scraping job postings...")
  job_data = scraper.scrape_jobs()

  print("[analyzer] Extracting skills......")
  skill_stats = analyzer.analyze_skills(job_data)

  print("[visualize] Creating visualization...")
  visualize.plot_skill_stats(skill_stats, top_n=15)

  print("Done.")
