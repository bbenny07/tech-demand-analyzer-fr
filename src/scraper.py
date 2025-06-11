import requests
from bs4 import BeautifulSoup
import time

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
  for job in soup.find_all('tr', attrs={'data-offset': True}):
    title_tag = job.find('h2', {'itemprop': 'title'})
    company_tag = job.find('h3', {'itemprop': 'name'})
    link_tag = job.find('a', class_='preventLink')
    tags_td = job.find('td', class_='tags')
    skills = []
    if tags_td:
      skills = [tag.text.strip() for tag in tags_td.find_all('h3')]

    if not title_tag or not company_tag:
      continue
    job_data = {
        'title': title_tag.text.strip(),
        'company': company_tag.text.strip(),
        'url': f"https://remoteok.com{link_tag['href']}" if link_tag else '',
        'source': 'remoteok',
        'language': language,
        'quick_skills': skills
    }

    jobs.append(job_data)
  return jobs


ALGOLIA_APP_ID = "CSEKHVMS53"
ALGOLIA_API_KEY = "4bd8f6215d0cc52b26430765769e65a0"


def scrape_wttj(language="python", location="paris", limit=20):
  url = f"https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/*/queries"
  headers = {
      "X-Algolia-API-Key": ALGOLIA_API_KEY,
      "X-Algolia-Application-Id": ALGOLIA_APP_ID,
      "Content-Type": "application/json",
      "Referer": "https://www.welcometothejungle.com"
  }

  query_word = "développeur"  # Или data, backend, python и т.п.

  data = {
      "requests": [{
          "indexName":
          "wttj_jobs_production_fr",
          "params": (f"query={query_word}"
                     f"&filters=offices.city:Paris"
                     f"&hitsPerPage=20"
                     f"&attributesToRetrieve=%5B%22*%22%5D")
      }]
  }

  response = requests.post(url, headers=headers, json=data)
  if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    return []
  all_jobs = []
  try:
    hits = response.json()["results"][0]["hits"]
    all_jobs.extend(hits)
  except Exception as e:
    print("Error parsing JSON:", e)
    return []

  time.sleep(1)  # небольшая задержка

  print(f"[scraper] Total jobs scraped: {len(all_jobs)}")
  # print("Status code:", response.text[:20000])
  return all_jobs
  
  # jobs = response.json()["results"][0]["hits"]

  # for job in jobs:
  #   name = job.get("name", "No name")
  #   offices = job.get("offices", {})
  #   city = offices[0]["city"] if offices else "No city"
  #   organization = job.get("organization", []).get("name", "No organization")
  #   print(name, "|", city, "|", organization)

  # return []


# scrape_remoteok,
SCRAPERS = [
    scrape_wttj,
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
