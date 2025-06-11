import requests
from bs4 import BeautifulSoup

languages = ['python', 'java', 'c++', 'javascript', 'ruby', 'go', 'php']


def scrape_remoteok(language: str = "python") -> list:
  url = f"https://remoteok.com/remote-{language}-jobs"
  headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
      'Chrome/115.0.0.0 Safari/537.36'
  }
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
    print(
        f"Error open page https://remoteok.com/remote-{language}-jobs: status {response.status_code}"
    )
    return []
  soup = BeautifulSoup(response.text, 'html.parser')
  jobs = []
  for job in soup.find_all('tr', class_='job'):
    title_tag = job.find('h2', {'itemprop': 'title'})
    company_tag = job.find('h3', {'itemprop': 'name'})
    description_tag = job.find('div', class_='description')
    link_tag = job.find('a', class_='preventLink')

    if not title_tag or not company_tag:
      continue

    job_data = {
        'title': title_tag.text.strip(),
        'company': company_tag.text.strip(),
        'description': description_tag.text.strip() if description_tag else '',
        'url': f"https://remoteok.com{link_tag['href']}" if link_tag else '',
        'source': 'remoteok',
        'language': language,
    }

    jobs.append(job_data)

  return jobs


def scrape_wttj():
  jobs = []
  return jobs


def scrape_indeed():
  jobs = []

  return jobs


SCRAPERS = [
    scrape_remoteok,
    scrape_wttj,
    scrape_indeed,
]


def scrape_jobs():
  all_jobs = []
  for scraper_func in SCRAPERS:
    try:
      jobs = scraper_func()
      all_jobs.extend(jobs)
    except Exception as e:
      print(f"Error {scraper_func.__name__}: {e}")
  return all_jobs
