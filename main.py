import json
import requests
from bs4 import BeautifulSoup
import time as tm
from itertools import groupby

def load_config(file_name):
    # Load the config file
    with open(file_name) as f:
        return json.load(f)

def remove_duplicate_job_cards(job_list):
    job_list.sort(key=lambda x: (x['title'] , x['company']))
    job_list = [next(g) for k,g in groupby(job_list, key=lambda x: (x['title'], x['company']))]
    return job_list

def get_with_retry(url, config, retries=3, delay=1):
    # Get the URL with retries and delay
    print(f"Retrieving URL: {url}")
    for i in range(retries):
        try:
            if len(config['proxies']) > 0:
                r = requests.get(url, headers=config['headers'], proxies=config['proxies'], timeout=5)
            else:
                r = requests.get(url, headers=config['headers'], timeout=5)
            return BeautifulSoup(r.content, 'html.parser')
        except requests.exceptions.Timeout:
            print(f"Timeout occurred for URL: {url}, retrying in {delay}s...")
            tm.sleep(delay)
        except Exception as e:
            print(f"An error occurred while retrieving the URL: {url}, error: {e}")
    return None

def get_job_description(soup):
    # print(soup)
    div = soup.find('div', class_='description__text description__text--rich')
    if div:
        # Remove unwanted elements
        for element in div.find_all(['span', 'a']):
            element.decompose()

        # Replace bullet points
        for ul in div.find_all('ul'):
            for li in ul.find_all('li'):
                li.insert(0, '-')

        text = div.get_text(separator='\n').strip()
        text = text.replace('\n\n', '')
        text = text.replace('::marker', '-')
        text = text.replace('-\n', '- ')
        text = text.replace('Show less', '').replace('Show more', '')
        return text
    else:
        return "Could not find Job Description"


def transform_job_card(raw_data,config=None):
    job_list = []
    divs = raw_data.find_all('div', class_='base-card')
    for item in divs:
        title = item.find('h3').text.strip()
        company = item.find('a', class_='hidden-nested-link')
        location = item.find('span', class_='job-search-card__location')
        entity_urn = item['data-entity-urn']
        job_posting_id = entity_urn.split(':')[-1]
        job_url = 'https://www.linkedin.com/jobs/view/' + job_posting_id + '/'

        date_tag_new = item.find('time', class_='job-search-card__listdate--new')
        date_tag = item.find('time', class_='job-search-card__listdate')
        date = date_tag['datetime'] if date_tag else date_tag_new['datetime'] if date_tag_new else ''
        job_description = ''
        job = {
            'title': title,
            'company': company.text.strip().replace('\n', ' ') if company else '',
            'location': location.text.strip() if location else '',
            'date': date,
            'job_url': job_url,
            'job_description': job_description,
            'applied': 0,
            'hidden': 0,
            'interview': 0,
            'rejected': 0
        }
        job_description_raw = get_with_retry(job['job_url'], config)
        # print(job_description_raw)
        # print(get_job_description(job_description_raw))
        job["job_description"] =(get_job_description(job_description_raw))
        # print(job)
        job_list.append(job)
    return job_list

def get_job_cards(config):
    all_jobs = []
    print(config['search_queries'])
    for query in config['search_queries']:
        key_words = query['key_words']
        location = query['location']
        for page_count in range(0,config['pages_to_scrape']):
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={key_words}&location={location}&f_TPR=&f_WT={query['Remote']}&geoId=&f_TPR={config['timespan']}&start={25*page_count}"
            raw_card_data = get_with_retry(url, config)
            jobs = transform_job_card(raw_card_data, config)
            print("JOBS")
            print(jobs)
            all_jobs.extend(jobs)
    all_jobs = remove_duplicate_job_cards(all_jobs)
    return all_jobs

def main(config_file, urls):
    job_list = []
    # load_config(config_file)
    all_jobs = get_job_cards(config_file)
    print(all_jobs)

if __name__ == "__main__":
    config_file = load_config(r"./config.json")
    # print(config_file)
    main(config_file,[])


