import requests
from bs4 import BeautifulSoup
import json
import os

base_url = "https://www.offerzen.com"  # put the correct base URL here
results = []

headers = {
    'accept': 'application/json, text/plain, */*',
    'authorization': os.environ.get('OFFERZEN_COMPANY_LISTINGS_API_KEY')
}

# iterate over all pages
for page in range(1, 119):  # pages from 1 to 118
    url = f"{base_url}/api/company/public_profiles?page={page}"
    response = requests.get(url, headers=headers)
    
    # check if the request was successful
    if response.status_code == 200:
        data = response.json()

        if data['success']:
            for company in data['result']:
                cities = ', '.join([city['name'] for city in company['cities']])
                tech_stack = ', '.join([tech['title'] for tech in company['tech_stack']])
                perks = ', '.join([perk['title'] for perk in company['perks']])

                company['cities'] = cities
                company['tech_stack'] = tech_stack
                company['perks'] = perks

                # get additional data from the company's url
                company_url = base_url + company['url']
                company_page = requests.get(company_url)
                if company_page.status_code == 200:
                    soup = BeautifulSoup(company_page.text, 'html.parser')
                    company_info_div = soup.find('div', {'class': 'markdown-rendered'})
                    if company_info_div:
                        company['company_info'] = company_info_div.get_text()

                results.append(company)

# write the results to a json file
with open('./docs/docs/offerzen_company_listing/company_profiles.json', 'w') as f:
    json.dump(results, f)
